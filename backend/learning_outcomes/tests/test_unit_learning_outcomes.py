from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import serializers

from learning_outcomes.serializers import SuggestRAESerializer
from learning_outcomes.services.llm.exceptions import LLMServiceError
from learning_outcomes.services.prompt_builder import build_rae_prompt
from learning_outcomes.services.rae_service import RAEService


class StubProvider:
    def __init__(self, response: str = "RAE sugerido") -> None:
        self.response = response
        self.last_prompt = ""

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


class FailingProvider:
    def generate(self, prompt: str) -> str:
        _ = prompt
        raise LLMServiceError("fallo proveedor")


class SuggestRAESerializerTests(SimpleTestCase):
    def test_serializer_limpia_espacios(self) -> None:
        serializer = SuggestRAESerializer(
            data={
                "finalidad_curso": "  Desarrollar pensamiento critico  ",
                "concepto_principal": "  estadistica inferencial  ",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            serializer.validated_data["finalidad_curso"], "Desarrollar pensamiento critico"
        )
        self.assertEqual(
            serializer.validated_data["concepto_principal"], "estadistica inferencial"
        )

    def test_serializer_falla_si_campos_vacios(self) -> None:
        serializer = SuggestRAESerializer(
            data={"finalidad_curso": "   ", "concepto_principal": "   "}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIsInstance(serializer.errors["finalidad_curso"][0], serializers.ErrorDetail)
        self.assertIsInstance(serializer.errors["concepto_principal"][0], serializers.ErrorDetail)


class PromptBuilderTests(SimpleTestCase):
    def test_prompt_incluye_contexto_y_datos(self) -> None:
        prompt = build_rae_prompt(
            finalidad_curso="Resolver problemas de optimizacion",
            concepto_principal="programacion lineal",
            institutional_context="Contexto institucional de prueba",
        )

        self.assertIn("Contexto institucional de prueba", prompt)
        self.assertIn("Finalidad del curso: Resolver problemas de optimizacion", prompt)
        self.assertIn("Concepto principal: programacion lineal", prompt)
        self.assertIn("Resultado de Aprendizaje Esperado", prompt)


class RAEServiceTests(SimpleTestCase):
    def test_suggest_rae_construye_prompt_y_devuelve_respuesta(self) -> None:
        provider = StubProvider(response="Analizar datos para tomar decisiones informadas.")
        service = RAEService(llm_provider=provider)

        with patch(
            "learning_outcomes.services.rae_service.get_institutional_context",
            return_value="Contexto U test",
        ):
            result = service.suggest_rae(
                finalidad_curso="Fortalecer analisis cuantitativo",
                concepto_principal="estadistica aplicada",
            )

        self.assertEqual(result, "Analizar datos para tomar decisiones informadas.")
        self.assertIn("Contexto U test", provider.last_prompt)
        self.assertIn("Finalidad del curso: Fortalecer analisis cuantitativo", provider.last_prompt)
        self.assertIn("Concepto principal: estadistica aplicada", provider.last_prompt)

    def test_suggest_rae_propaga_error_llm(self) -> None:
        service = RAEService(llm_provider=FailingProvider())

        with self.assertRaises(LLMServiceError):
            service.suggest_rae(
                finalidad_curso="Finalidad",
                concepto_principal="Concepto",
            )
