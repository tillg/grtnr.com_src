"""
Translation Service Configuration

Configuration management for the translation service.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .exceptions import ConfigurationError

# Load .env file if available
try:
    from dotenv import load_dotenv

    load_dotenv()  # Loads .env from current directory or parent directories
except ImportError:
    # dotenv not available, will use environment variables only
    pass


@dataclass
class TranslationConfig:
    """Configuration for translation service"""

    # API Configuration
    api_key: str = ""
    model: str = "gpt-4o"

    # Language Configuration
    target_languages: List[str] = field(default_factory=lambda: ["de", "fr"])
    exclude_categories: List[str] = field(default_factory=lambda: ["recipes"])
    exclude_paths: List[str] = field(default_factory=lambda: ["/pages/impressum/"])

    # API Behavior
    max_retries: int = 3
    timeout: int = 120
    rate_limit_delay: int = 1  # seconds between requests
    max_concurrent_translations: int = 3  # maximum parallel translations per content
    max_concurrent_content: int = 2  # maximum content items to process in parallel

    # Language Detection
    auto_detect_language: bool = True
    default_source_language: str = "en"

    @classmethod
    def from_dotenv(cls, dotenv_path: str = None) -> "TranslationConfig":
        """Create configuration from .env file"""

        try:
            from dotenv import load_dotenv

            if dotenv_path:
                # Load specific .env file
                if not os.path.exists(dotenv_path):
                    raise ConfigurationError(f".env file not found: {dotenv_path}")
                load_dotenv(dotenv_path)
            else:
                # Load .env from current directory or parent directories
                load_dotenv()
        except ImportError:
            raise ConfigurationError(
                "python-dotenv package is required for .env file support"
            )

        return cls.from_environment()

    @classmethod
    def from_environment(cls) -> "TranslationConfig":
        """Create configuration from environment variables"""

        config = cls()

        # Required API key
        config.api_key = os.getenv("OPENAI_API_KEY", "")
        if not config.api_key:
            raise ConfigurationError("OPENAI_API_KEY environment variable is required")

        # Optional configuration
        config.model = os.getenv("TRANSLATION_MODEL", config.model)
        config.timeout = int(os.getenv("TRANSLATION_TIMEOUT", str(config.timeout)))
        config.max_retries = int(
            os.getenv("TRANSLATION_MAX_RETRIES", str(config.max_retries))
        )
        config.max_concurrent_translations = int(
            os.getenv(
                "TRANSLATION_MAX_CONCURRENT", str(config.max_concurrent_translations)
            )
        )
        config.max_concurrent_content = int(
            os.getenv(
                "TRANSLATION_MAX_CONCURRENT_CONTENT", str(config.max_concurrent_content)
            )
        )

        # Target languages from environment (comma-separated)
        target_langs = os.getenv("TRANSLATION_TARGET_LANGUAGES", "")
        if target_langs:
            config.target_languages = [lang.strip() for lang in target_langs.split(",")]

        # Exclude categories (comma-separated)
        exclude_cats = os.getenv("TRANSLATION_EXCLUDE_CATEGORIES", "")
        if exclude_cats:
            config.exclude_categories = [cat.strip() for cat in exclude_cats.split(",")]

        # Exclude paths (comma-separated)
        exclude_paths = os.getenv("TRANSLATION_EXCLUDE_PATHS", "")
        if exclude_paths:
            config.exclude_paths = [path.strip() for path in exclude_paths.split(",")]

        # Boolean flags
        config.auto_detect_language = (
            os.getenv("TRANSLATION_AUTO_DETECT", "true").lower() == "true"
        )

        return config

    @classmethod
    def from_pelican_settings(cls, settings: dict) -> "TranslationConfig":
        """Create configuration from Pelican settings"""

        config = cls()

        # API Configuration
        config.api_key = settings.get(
            "TRANSLATION_API_KEY", os.getenv("OPENAI_API_KEY", "")
        )
        if not config.api_key:
            raise ConfigurationError(
                "Translation API key not found in settings or environment"
            )

        config.model = settings.get("TRANSLATION_MODEL", config.model)

        # Language Configuration
        config.target_languages = settings.get(
            "TRANSLATION_TARGET_LANGUAGES", config.target_languages
        )
        config.exclude_categories = settings.get(
            "TRANSLATION_EXCLUDE_CATEGORIES", config.exclude_categories
        )
        config.exclude_paths = settings.get(
            "TRANSLATION_EXCLUDE_PATHS", config.exclude_paths
        )

        # API Behavior
        config.max_retries = settings.get("TRANSLATION_MAX_RETRIES", config.max_retries)
        config.timeout = settings.get("TRANSLATION_TIMEOUT", config.timeout)
        config.rate_limit_delay = settings.get(
            "TRANSLATION_RATE_LIMIT_DELAY", config.rate_limit_delay
        )
        config.max_concurrent_translations = settings.get(
            "TRANSLATION_MAX_CONCURRENT", config.max_concurrent_translations
        )
        config.max_concurrent_content = settings.get(
            "TRANSLATION_MAX_CONCURRENT_CONTENT", config.max_concurrent_content
        )

        # Language Detection
        config.auto_detect_language = settings.get(
            "TRANSLATION_AUTO_DETECT", config.auto_detect_language
        )
        config.default_source_language = settings.get(
            "TRANSLATION_DEFAULT_SOURCE_LANG", config.default_source_language
        )

        return config

    def validate(self) -> None:
        """Validate configuration"""

        if not self.api_key:
            raise ConfigurationError("API key is required")

        if not self.target_languages:
            raise ConfigurationError("At least one target language must be specified")

        if self.timeout <= 0:
            raise ConfigurationError("Timeout must be positive")

        if self.max_retries < 0:
            raise ConfigurationError("Max retries must be non-negative")

        # Validate language codes (basic check)
        valid_languages = {
            "en",
            "de",
            "fr",
            "es",
            "it",
            "pt",
            "ru",
            "ja",
            "ko",
            "zh",
            "ar",
            "hi",
            "nl",
            "sv",
            "no",
            "da",
            "fi",
        }

        for lang in self.target_languages:
            if lang not in valid_languages:
                raise ConfigurationError(f"Language '{lang}' may not be supported")

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return [
            "en",
            "de",
            "fr",
            "es",
            "it",
            "pt",
            "ru",
            "ja",
            "ko",
            "zh",
            "ar",
            "hi",
            "nl",
            "sv",
            "no",
            "da",
            "fi",
            "pl",
            "cs",
            "tr",
        ]

    def is_language_supported(self, language: str) -> bool:
        """Check if a language is supported"""
        return language in self.get_supported_languages()

    def should_exclude_category(self, category: str) -> bool:
        """Check if a category should be excluded from translation"""
        return category in self.exclude_categories

    def should_exclude_path(self, path: str) -> bool:
        """Check if a path should be excluded from translation"""
        return any(excluded_path in path for excluded_path in self.exclude_paths)

    def __repr__(self) -> str:
        """String representation of configuration"""
        # Don't include API key in representation
        return (
            f"TranslationConfig("
            f"model='{self.model}', "
            f"target_languages={self.target_languages}, "
            f"max_retries={self.max_retries}"
            f")"
        )
