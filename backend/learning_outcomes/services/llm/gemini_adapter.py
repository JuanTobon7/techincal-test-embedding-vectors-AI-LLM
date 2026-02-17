import json
import logging
import os
from typing import Any

import httpx
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from .base import LLMProvider
from .exceptions import LLMRetryableError, LLMServiceError

logger = logging.getLogger(__name__)


class GeminiAdapter(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("AI_API_KEY", "").strip()
        print('api key: ', self.api_key)
        self.base_url = os.getenv("AI_API_URL", "").strip().rstrip("/")
        self.model = os.getenv("AI_CHAT_MODEL", "").strip()
        self.timeout_seconds = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))
        self.max_retries = int(os.getenv("AI_MAX_RETRIES", "3"))
        self.backoff_min = float(os.getenv("AI_BACKOFF_MIN", "1"))
        self.backoff_max = float(os.getenv("AI_BACKOFF_MAX", "8"))

        if not self.api_key:
            raise LLMServiceError("AI_API_KEY is not configured")
        if not self.base_url:
            raise LLMServiceError("AI_API_URL is not configured")
        if not self.model:
            raise LLMServiceError("AI_CHAT_MODEL is not configured")

    def generate(self, prompt: str) -> str:
        try:
            return self._generate_with_retry(prompt)
        except LLMServiceError:
            raise
        except Exception as exc:
            logger.exception("LLM unexpected error")
            raise LLMServiceError("LLM generation failed") from exc

    def _retrying(self) -> Retrying:
        return Retrying(
            retry=retry_if_exception_type((httpx.TimeoutException, httpx.TransportError, LLMRetryableError)),
            wait=wait_exponential(min=self.backoff_min, max=self.backoff_max),
            stop=stop_after_attempt(self.max_retries),
            reraise=True,
        )

    def _endpoint(self) -> str:
        return f"{self.base_url}/models/{self.model}:generateContent"

    def _payload(self, prompt: str) -> dict[str, Any]:
        return {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
            },
        }

    def _generate_with_retry(self, prompt: str) -> str:
        for attempt in self._retrying():
            with attempt:
                params = {"key": self.api_key}
                timeout = httpx.Timeout(self.timeout_seconds)
                with httpx.Client(timeout=timeout) as client:
                    response = client.post(
                        self._endpoint(),
                        params=params,
                        headers={"Content-Type": "application/json"},
                        content=json.dumps(self._payload(prompt)),
                    )
                    print("response: ", response)

                if response.status_code == 429:
                    logger.warning("LLM rate limit")
                    print("apikey: ",self.api_key)
                    raise LLMRetryableError("LLM rate limit")

                if response.status_code >= 500:
                    logger.warning("LLM provider error: %s", response.status_code)
                    raise LLMRetryableError("LLM provider error")

                if response.status_code >= 400:
                    logger.error("LLM request failed: %s", response.text)
                    raise LLMServiceError("LLM request failed")

                data = response.json()
                text = _extract_text(data)
                if not text:
                    raise LLMServiceError("LLM response empty")
                return text

        raise LLMServiceError("LLM generation failed")


def _extract_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates") or []
    if not candidates:
        return ""
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    if not parts:
        return ""
    return (parts[0].get("text") or "").strip()
