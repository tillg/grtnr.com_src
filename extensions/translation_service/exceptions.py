"""
Translation Service Exceptions

Custom exceptions for the translation service.
"""


class TranslationError(Exception):
    """Base exception for translation errors"""
    pass


class APIError(TranslationError):
    """OpenAI API communication errors"""
    
    def __init__(self, message: str, status_code: int = None, response: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class RateLimitError(TranslationError):
    """API rate limiting errors"""
    
    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message)
        self.retry_after = retry_after


class InvalidResponseError(TranslationError):
    """Invalid API response format"""
    
    def __init__(self, message: str, response: str = None):
        super().__init__(message)
        self.response = response


class LanguageNotSupportedError(TranslationError):
    """Unsupported language codes"""
    
    def __init__(self, language: str):
        super().__init__(f"Language '{language}' is not supported")
        self.language = language


class CacheError(TranslationError):
    """Cache operation errors"""
    pass


class ConfigurationError(TranslationError):
    """Configuration errors"""
    pass