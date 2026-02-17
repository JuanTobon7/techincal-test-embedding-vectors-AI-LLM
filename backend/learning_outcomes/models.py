from django.db import models
from pgvector.django import VectorField


class InstitutionalEmbedding(models.Model):
    content = models.TextField()
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "institutional_embeddings"

    def __str__(self) -> str:
        return self.content[:80]

