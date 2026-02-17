import os

from .base import LLMProvider
from .gemini_adapter import GeminiAdapter


def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()
    if provider == "gemini":
        return GeminiAdapter()
    return GeminiAdapter()
