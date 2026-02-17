def build_rae_prompt(finalidad_curso: str, concepto_principal: str, institutional_context: str) -> str:
    bloom_verbs = "Analizar, Evaluar, Crear, Disenar, Formular, Sintetizar"
    prompt = f"""Eres un especialista en diseno curricular universitario.

Contexto institucional (obligatorio):
{institutional_context}

Insumos del profesor:
- Finalidad del curso: {finalidad_curso}
- Concepto principal: {concepto_principal}

Restricciones obligatorias:
- Entregar un unico RAE.
- Debe ser una sola oracion.
- Debe iniciar con un verbo en infinitivo de alto nivel de Bloom: {bloom_verbs}.
- Debe ser claro, medible y centrado en el estudiante.
- Prohibido incluir explicaciones, listas, comillas o texto adicional.

Entrega solo la oracion final del RAE y nada mas.
"""
    return prompt
