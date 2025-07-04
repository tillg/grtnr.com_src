"""
Translation service for automatic article translation.
Provides language detection and translation capabilities with caching.
"""

import hashlib
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Tuple

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

logger = get_logger("translation_service")


class TranslationError(Exception):
    """Custom exception for translation-related errors."""

    pass


class LanguageDetector(ABC):
    """Abstract base class for language detection services."""

    @abstractmethod
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.

        Args:
            text: The text to analyze

        Returns:
            Two-letter language code (e.g., 'en', 'de', 'fr')
        """
        pass


class Translator(ABC):
    """Abstract base class for translation services."""

    @abstractmethod
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translate text from source to target language.

        Args:
            text: The text to translate
            source_language: Source language code
            target_language: Target language code

        Returns:
            Translated text
        """
        pass


class MockLanguageDetector(LanguageDetector):
    """Mock language detector for testing and development."""

    def __init__(self, default_language: str = "en"):
        self.default_language = default_language

    def detect_language(self, text: str) -> str:
        """
        Mock language detection - returns default language.
        In real implementation, this would use a service like Google Cloud
        Translation API.
        """
        # Simple heuristic: if text contains common German words, assume German
        german_indicators = [
            "der",
            "die",
            "das",
            "und",
            "ich",
            "ist",
            "ein",
            "eine",
            "mit",
        ]
        text_lower = text.lower()

        german_count = sum(1 for word in german_indicators if word in text_lower)

        if german_count > 2:
            return "de"
        return self.default_language


class MockTranslator(Translator):
    """Mock translator for testing and development."""

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        """
        Mock translation - adds prefix to indicate translation.
        In real implementation, this would use a service like Google Cloud
        Translation API.
        """
        if source_language == target_language:
            return text

        # Simple mock: just add a prefix
        return f"[{source_language}→{target_language}] {text}"


class TranslationCache:
    """Handles caching of translations using file hashes."""

    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "translation_cache.json")
        self._cache = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            try:
                import json

                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
                logger.debug(
                    f"Loaded translation cache with " f"{len(self._cache)} entries"
                )
            except Exception as e:
                logger.warning(f"Failed to load translation cache: {e}")
                self._cache = {}

    def _save_cache(self):
        """Save cache to file."""
        try:
            import json

            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved translation cache with " f"{len(self._cache)} entries")
        except Exception as e:
            logger.error(f"Failed to save translation cache: {e}")

    def get_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""

    def get_cache_key(self, file_path: str, target_language: str) -> str:
        """Generate cache key for a file and target language."""
        return f"{file_path}:{target_language}"

    def is_cached(self, file_path: str, target_language: str) -> bool:
        """Check if translation is cached and still valid."""
        cache_key = self.get_cache_key(file_path, target_language)

        if cache_key not in self._cache:
            return False

        cache_entry = self._cache[cache_key]
        current_hash = self.get_file_hash(file_path)

        return cache_entry.get("hash") == current_hash

    def get_cached_translation(
        self, file_path: str, target_language: str
    ) -> Optional[str]:
        """Get cached translation if available and valid."""
        if not self.is_cached(file_path, target_language):
            return None

        cache_key = self.get_cache_key(file_path, target_language)
        return self._cache[cache_key].get("translation")

    def cache_translation(self, file_path: str, target_language: str, translation: str):
        """Cache a translation."""
        cache_key = self.get_cache_key(file_path, target_language)
        file_hash = self.get_file_hash(file_path)

        self._cache[cache_key] = {
            "hash": file_hash,
            "translation": translation,
            "created": datetime.now().isoformat(),
        }

        self._save_cache()
        logger.debug(f"Cached translation for {file_path} -> " f"{target_language}")


class TranslationService:
    """Main translation service orchestrating language detection and
    translation."""

    def __init__(
        self,
        language_detector: Optional[LanguageDetector] = None,
        translator: Optional[Translator] = None,
        cache_dir: str = "cache",
    ):
        self.language_detector = language_detector or MockLanguageDetector()
        self.translator = translator or MockTranslator()
        self.cache = TranslationCache(cache_dir)

    def translate_content(
        self, content: str, file_path: str, target_language: str
    ) -> Tuple[str, str]:
        """
        Translate content to target language.

        Args:
            content: The content to translate
            file_path: Path to the source file (for caching)
            target_language: Target language code

        Returns:
            Tuple of (translated_content, source_language)
        """
        # Check cache first
        cached_translation = self.cache.get_cached_translation(
            file_path, target_language
        )
        if cached_translation:
            logger.info(
                f"Using cached translation for {file_path} -> " f"{target_language}"
            )
            # We still need to detect the source language for metadata
            source_language = self.language_detector.detect_language(content)
            return cached_translation, source_language

        # Detect source language
        source_language = self.language_detector.detect_language(content)
        logger.info(f"Detected language '{source_language}' for {file_path}")

        # Skip translation if source equals target
        if source_language == target_language:
            logger.info(
                f"Source language matches target language "
                f"({target_language}), skipping translation"
            )
            return content, source_language

        # Translate content
        try:
            translated_content = self.translator.translate(
                content, source_language, target_language
            )

            # Cache the translation
            self.cache.cache_translation(file_path, target_language, translated_content)

            logger.info(
                f"Translated {file_path} from {source_language} to "
                f"{target_language}"
            )
            return translated_content, source_language

        except Exception as e:
            logger.error(f"Translation failed for {file_path}: {e}")
            raise TranslationError(f"Translation failed: {e}")

    def get_available_languages(self) -> list:
        """Get list of supported languages using ISO 639-1 codes."""
        # This would be implemented based on the actual translation service
        # Using ISO 639-1 two-letter language codes
        return [
            "en",  # English
            "de",  # German
            "fr",  # French
            "es",  # Spanish
            "it",  # Italian
            "pt",  # Portuguese
            "ru",  # Russian
            "nl",  # Dutch
            "sv",  # Swedish
            "da",  # Danish
            "no",  # Norwegian
            "fi",  # Finnish
            "pl",  # Polish
            "zh",  # Chinese
            "ja",  # Japanese
            "ko",  # Korean
            "hi",  # Hindi
            "ar",  # Arabic
            "th",  # Thai
            "vi",  # Vietnamese
            "tr",  # Turkish
            "he",  # Hebrew
            "fa",  # Persian
        ]
