from unittest.mock import Mock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learning_outcomes.services.llm.exceptions import LLMServiceError


class SuggestRAEApiSmokeTests(APITestCase):
    def test_post_sugerir_rae_responde_200(self) -> None:
        fake_service = Mock()
        fake_service.suggest_rae.return_value = "Evaluar escenarios para justificar decisiones."

        with patch("learning_outcomes.views.RAEService", return_value=fake_service):
            response = self.client.post(
                reverse("sugerir-rae"),
                data={
                    "finalidad_curso": "Desarrollar criterio profesional",
                    "concepto_principal": "pensamiento estrategico",
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["rae_sugerido"], "Evaluar escenarios para justificar decisiones."
        )

    def test_post_sugerir_rae_payload_invalido_responde_400(self) -> None:
        response = self.client.post(
            reverse("sugerir-rae"),
            data={"finalidad_curso": "   ", "concepto_principal": "   "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("finalidad_curso", response.data)
        self.assertIn("concepto_principal", response.data)

    def test_post_sugerir_rae_si_llm_falla_responde_503(self) -> None:
        fake_service = Mock()
        fake_service.suggest_rae.side_effect = LLMServiceError("rate limit")

        with patch("learning_outcomes.views.RAEService", return_value=fake_service):
            response = self.client.post(
                reverse("sugerir-rae"),
                data={
                    "finalidad_curso": "Fortalecer competencias de investigacion",
                    "concepto_principal": "metodologia cientifica",
                },
                format="json",
            )

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("Demasiados reintentos", response.data["detail"])

