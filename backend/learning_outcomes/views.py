from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SuggestRAESerializer
from .services.rae_service import RAEService
from .services.llm.exceptions import LLMServiceError


class SuggestRAEView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SuggestRAESerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = RAEService()
        try:
            rae = service.suggest_rae(
                finalidad_curso=serializer.validated_data["finalidad_curso"],
                concepto_principal=serializer.validated_data["concepto_principal"],
            )
        except LLMServiceError:
            return Response(
                {
                    "detail": (
                        "Ups, algo salio mal. Demasiados reintentos en un minuto, "
                        "por favor espera y vuelve a intentar."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"rae_sugerido": rae}, status=status.HTTP_200_OK)
