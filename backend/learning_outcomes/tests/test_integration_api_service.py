from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learning_outcomes.services.llm.exceptions import LLMServiceError


class CapturingProvider:
    def __init__(self, result: str) -> None:
        self.result = result
        self.received_prompt = ""

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return self.result


class FailingProvider:
    def generate(self, prompt: str) -> str:
        _ = prompt
        raise LLMServiceError("error de proveedor")


class SuggestRAEIntegrationTests(APITestCase):
    def test_integra_api_rae_service_y_prompt_builder(self) -> None:
        provider = CapturingProvider("Disenar soluciones para problemas complejos del contexto.")

        with patch(
            "learning_outcomes.services.rae_service.get_llm_provider",
            return_value=provider,
        ):
            response = self.client.post(
                reverse("sugerir-rae"),
                data={
                    "finalidad_curso": "Aplicar conocimiento disciplinar en problemas reales",
                    "concepto_principal": "modelamiento matematico",
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["rae_sugerido"],
            "Disenar soluciones para problemas complejos del contexto.",
        )
        self.assertIn("Contexto institucional obligatorio", provider.received_prompt)
        self.assertIn(
            "Finalidad del curso: Aplicar conocimiento disciplinar en problemas reales",
            provider.received_prompt,
        )
        self.assertIn("Concepto principal: modelamiento matematico", provider.received_prompt)

    def test_integra_api_y_mapea_error_llm_a_503(self) -> None:
        with patch(
            "learning_outcomes.services.rae_service.get_llm_provider",
            return_value=FailingProvider(),
        ):
            response = self.client.post(
                reverse("sugerir-rae"),
                data={
                    "finalidad_curso": "Formar competencias analiticas",
                    "concepto_principal": "simulacion",
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("Demasiados reintentos", response.data["detail"])

