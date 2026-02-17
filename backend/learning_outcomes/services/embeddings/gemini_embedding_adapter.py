import json
import logging
import os
from typing import Any

import httpx
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from ..llm.exceptions import LLMRetryableError, LLMServiceError
from .base import EmbeddingProvider

logger = logging.getLogger(__name__)


class GeminiEmbeddingAdapter(EmbeddingProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("AI_API_KEY", "").strip()
        self.base_url = os.getenv("AI_API_URL", "").strip().rstrip("/")
        self.model = os.getenv("AI_EMBEDDING_MODEL", "").strip()
        self.timeout_seconds = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))
        self.max_retries = int(os.getenv("AI_MAX_RETRIES", "3"))
        self.backoff_min = float(os.getenv("AI_BACKOFF_MIN", "1"))
        self.backoff_max = float(os.getenv("AI_BACKOFF_MAX", "8"))

        if not self.api_key:
            raise LLMServiceError("AI_API_KEY is not configured")
        if not self.base_url:
            raise LLMServiceError("AI_API_URL is not configured")
        if not self.model:
            raise LLMServiceError("AI_EMBEDDING_MODEL is not configured")

    def embed(self, text: str) -> list[float]:
        try:
            return self._embed_with_retry(text)
        except LLMServiceError:
            raise
        except Exception as exc:
            logger.exception("Embedding unexpected error")
            raise LLMServiceError("Embedding generation failed") from exc

    def _retrying(self) -> Retrying:
        return Retrying(
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError, LLMRetryableError)),
            wait=wait_exponential(min=self.backoff_min, max=self.backoff_max),
            stop=stop_after_attempt(self.max_retries),
            reraise=True,
        )

    def _endpoint(self) -> str:
        return f"{self.base_url}/models/{self.model}:embedContent"

    def _payload(self, text: str) -> dict[str, Any]:
        return {
            "content": {
                "parts": [{"text": text}],
            }
        }

    def _embed_with_retry(self, text: str) -> list[float]:
        for attempt in self._retrying():
            with attempt:
                params = {"key": self.api_key}
                timeout = httpx.Timeout(self.timeout_seconds)
                with httpx.Client(timeout=timeout) as client:
                    response = client.post(
                        self._endpoint(),
                        params=params,
                        headers={"Content-Type": "application/json"},
                        content=json.dumps(self._payload(text)),
                    )

                if response.status_code == 429:
                    logger.warning("Embedding rate limit")
                    raise LLMRetryableError("Embedding rate limit")

                if response.status_code >= 500:
                    logger.warning("Embedding provider error: %s", response.status_code)
                    raise LLMRetryableError("Embedding provider error")

                if response.status_code >= 400:
                    logger.error("Embedding request failed: %s", response.text)
                    raise LLMServiceError("Embedding request failed")

                data = response.json()
                values = data.get("embedding", {}).get("values")
                if not values:
                    raise LLMServiceError("Embedding response empty")
                return [float(v) for v in values]

        raise LLMServiceError("Embedding generation failed")
