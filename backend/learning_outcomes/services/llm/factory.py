import os

from .base import LLMProvider
from .openai_adapter import OpenAIAdapter


def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider == "openai":
        return OpenAIAdapter()
    return OpenAIAdapter()
