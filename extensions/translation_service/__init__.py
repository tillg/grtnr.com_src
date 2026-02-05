"""
Translation Service Package

Provides AI-powered automatic translation of content using OpenAI's GPT API.
"""

from .config import TranslationConfig
from .exceptions import (
    APIError,
    InvalidResponseError,
    LanguageNotSupportedError,
    RateLimitError,
    TranslationError,
)
from .service import TranslationService

__version__ = "1.0.0"
__all__ = [
    "TranslationService",
    "TranslationConfig",
    "TranslationError",
    "APIError",
    "RateLimitError",
    "InvalidResponseError",
    "LanguageNotSupportedError",
]
