import os

from .base import EmbeddingProvider
from .gemini_embedding_adapter import GeminiEmbeddingAdapter


def get_embedding_provider() -> EmbeddingProvider:
    provider = os.getenv("EMBEDDING_PROVIDER", "gemini").strip().lower()
    if provider == "gemini":
        return GeminiEmbeddingAdapter()
    return GeminiEmbeddingAdapter()
