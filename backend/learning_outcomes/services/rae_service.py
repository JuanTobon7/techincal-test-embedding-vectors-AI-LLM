import logging

from .institutional_context import get_institutional_context
from .llm.base import LLMProvider
from .llm.exceptions import LLMServiceError
from .llm.factory import get_llm_provider
from .prompt_builder import build_rae_prompt

logger = logging.getLogger(__name__)


class RAEService:
    def __init__(self, llm_provider: LLMProvider | None = None) -> None:
        self.llm_provider = llm_provider or get_llm_provider()

    def suggest_rae(self, finalidad_curso: str, concepto_principal: str) -> str:
        institutional_context = get_institutional_context(finalidad_curso, concepto_principal)
        prompt = build_rae_prompt(
            finalidad_curso=finalidad_curso,
            concepto_principal=concepto_principal,
            institutional_context=institutional_context,
        )
        try:
            return self.llm_provider.generate(prompt)
        except LLMServiceError:
            logger.exception("LLM generation failed")
            raise
