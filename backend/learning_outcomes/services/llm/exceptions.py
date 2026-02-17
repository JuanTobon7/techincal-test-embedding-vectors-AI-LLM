class LLMServiceError(Exception):
    pass


class LLMRetryableError(LLMServiceError):
    pass
