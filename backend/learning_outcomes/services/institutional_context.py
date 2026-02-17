import logging

from .rag.retriever import InstitutionalRetriever
from .embeddings.factory import get_embedding_provider
from .llm.exceptions import LLMServiceError

logger = logging.getLogger(__name__)


def get_institutional_context(finalidad_curso: str, concepto_principal: str) -> str:
    query = f"{finalidad_curso} {concepto_principal}".strip()
    try:
        retriever = InstitutionalRetriever(get_embedding_provider())
        context = retriever.build_context(query, top_k=3)
        if context:
            return context
    except LLMServiceError:
        logger.warning("Embedding retrieval failed, using fallback context")

    return (
        "Lineamientos institucionales para redactar RAE:\n"
        "1) Iniciar con un verbo de accion medible de la taxonomia de Bloom.\n"
        "2) Expresar desempeno observable, no intenciones generales.\n"
        "3) Vincular el resultado con el concepto central del curso.\n"
        "4) Incluir condiciones o contexto de aplicacion cuando sea pertinente.\n"
        "5) Mantener una redaccion en una sola oracion, clara y evaluable."
    )
