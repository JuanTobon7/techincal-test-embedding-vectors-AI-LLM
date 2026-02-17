def build_rae_prompt(finalidad_curso: str, concepto_principal: str, institutional_context: str) -> str:
    bloom_verbs = "Analizar, Evaluar, Crear, Diseñar, Formular, Sintetizar, Aplicar, Justificar, Comparar, Integrar"
    prompt = f"""
    Eres un especialista en diseño curricular universitario con experiencia en formulación de Planes de Desarrollo de Curso (PDC) y alineación por competencias.

    Contexto institucional obligatorio:
    {institutional_context}

    Datos del curso:
    - Finalidad del curso: {finalidad_curso}
    - Concepto principal: {concepto_principal}

    Restricciones:
    - Genera un único Resultado de Aprendizaje Esperado (RAE).
    - Debe ser una sola oración.
    - Inicia con un verbo en infinitivo de alto nivel de Bloom: {bloom_verbs}.
    - Debe ser claro, medible, centrado en el estudiante y evidenciable.
    - No incluyas explicaciones, listas, comillas ni texto adicional.
    - Mantén estrictamente la redacción académica y en tercera persona.
    - No agregues contenido fuera del contexto institucional ni ejemplos.

    Entrega:
    - Solo la oración final del RAE, nada más.
    """
    return prompt
