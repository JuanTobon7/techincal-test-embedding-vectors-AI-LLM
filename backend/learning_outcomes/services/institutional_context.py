contexto_institucional = (
    "Todos los RAE en la universidad deben seguir la Taxonomia de Bloom y comenzar "
    "con un verbo en infinitivo de nivel superior (ej: Analizar, Evaluar, Crear). "
    "Deben ser centrados en el estudiante y evidenciables."
)


def get_institutional_context(finalidad_curso: str, concepto_principal: str) -> str:
    _ = finalidad_curso, concepto_principal
    return contexto_institucional
