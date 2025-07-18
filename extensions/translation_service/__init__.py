"""
Translation Service Package

Provides AI-powered automatic translation of content using OpenAI's GPT API.
"""

from .service import TranslationService
from .config import TranslationConfig
from .exceptions import (
    TranslationError,
    APIError,
    RateLimitError,
    InvalidResponseError,
    LanguageNotSupportedError
)

__version__ = "1.0.0"
__all__ = [
    "TranslationService",
    "TranslationConfig", 
    "TranslationError",
    "APIError",
    "RateLimitError",
    "InvalidResponseError",
    "LanguageNotSupportedError"
]