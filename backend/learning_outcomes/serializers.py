from rest_framework import serializers


class SuggestRAESerializer(serializers.Serializer):
    finalidad_curso = serializers.CharField(max_length=2000)
    concepto_principal = serializers.CharField(max_length=1000)

    def validate_finalidad_curso(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("La finalidad del curso no puede estar vacia.")
        return cleaned

    def validate_concepto_principal(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("El concepto principal no puede estar vacio.")
        return cleaned

