def build_rae_prompt(finalidad_curso: str, concepto_principal: str, institutional_context: str) -> str:
    bloom_verbs = "Analizar, Evaluar, Crear, Disenar, Formular, Sintetizar"
    prompt = f"""Eres un especialista en diseno curricular universitario.

Genera un unico Resultado de Aprendizaje Esperado (RAE) en espanol.

Contexto institucional recuperado:
{institutional_context}

Insumos del profesor:
- Finalidad del curso: {finalidad_curso}
- Concepto principal: {concepto_principal}

Restricciones obligatorias:
- Debe ser una sola oracion.
- Debe iniciar con un verbo de alto nivel de Bloom: {bloom_verbs}.
- Debe integrar explicitamente el contexto institucional recuperado.
- Debe ser observable y evaluable.
- Prohibido incluir explicaciones, listas, comillas o texto adicional.

Entrega solo la oracion final del RAE y nada mas.
"""
    return prompt
