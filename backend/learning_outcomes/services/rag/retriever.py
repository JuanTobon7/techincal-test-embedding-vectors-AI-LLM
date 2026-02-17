from typing import Iterable

from pgvector.django import L2Distance

from ...models import InstitutionalEmbedding
from ..embeddings.base import EmbeddingProvider


class InstitutionalRetriever:
    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self.embedding_provider = embedding_provider

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        embedding = self.embedding_provider.embed(query)
        rows = (
            InstitutionalEmbedding.objects.exclude(embedding__isnull=True)
            .order_by(L2Distance("embedding", embedding))[:top_k]
        )
        return [row.content for row in rows]

    def build_context(self, query: str, top_k: int = 3) -> str:
        chunks: Iterable[str] = self.retrieve(query, top_k=top_k)
        return "\n---\n".join([chunk for chunk in chunks if chunk.strip()])
