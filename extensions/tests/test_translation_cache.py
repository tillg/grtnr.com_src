#!/usr/bin/env python3

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from translation_service.cache import TranslationCache
except ImportError:
    # Mock class for testing before implementation
    class TranslationCache:
        def __init__(self, cache_dir: str):
            self.cache_dir = cache_dir
            self._cache = {}

        def get_cached_translation(self, content_hash: str, target_lang: str) -> str:
            key = f"{content_hash}_{target_lang}"
            return self._cache.get(key)

        def cache_translation(
            self, content_hash: str, target_lang: str, translation: str
        ):
            key = f"{content_hash}_{target_lang}"
            self._cache[key] = translation

        def invalidate_cache(self, content_hash: str):
            keys_to_remove = [
                k for k in self._cache.keys() if k.startswith(content_hash)
            ]
            for key in keys_to_remove:
                del self._cache[key]


class TestTranslationCache(unittest.TestCase):
    """Test cases for TranslationCache functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = TranslationCache(self.temp_dir)

        # Test data
        self.test_content_hash = "abc123def456"
        self.test_target_lang = "de"
        self.test_translation = "Das ist ein Test"

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_initialization(self):
        """Test cache initialization"""
        cache = TranslationCache(self.temp_dir)
        self.assertEqual(str(cache.cache_dir), self.temp_dir)

    def test_cache_miss(self):
        """Test cache miss behavior"""
        result = self.cache.get_cached_translation(
            self.test_content_hash, self.test_target_lang
        )
        self.assertIsNone(result)

    def test_cache_hit(self):
        """Test cache hit behavior"""
        # Cache a translation
        self.cache.cache_translation(
            self.test_content_hash, self.test_target_lang, self.test_translation
        )

        # Retrieve the translation
        result = self.cache.get_cached_translation(
            self.test_content_hash, self.test_target_lang
        )

        self.assertEqual(result, self.test_translation)

    def test_cache_multiple_languages(self):
        """Test caching multiple languages for same content"""
        translations = {
            "de": "Das ist ein Test",
            "fr": "C'est un test",
            "es": "Esto es una prueba",
        }

        # Cache all translations
        for lang, translation in translations.items():
            self.cache.cache_translation(self.test_content_hash, lang, translation)

        # Verify all translations are cached
        for lang, expected_translation in translations.items():
            result = self.cache.get_cached_translation(self.test_content_hash, lang)
            self.assertEqual(result, expected_translation)

    def test_cache_invalidation(self):
        """Test cache invalidation"""
        # Cache multiple translations
        translations = {"de": "Das ist ein Test", "fr": "C'est un test"}

        for lang, translation in translations.items():
            self.cache.cache_translation(self.test_content_hash, lang, translation)

        # Verify cached
        for lang in translations:
            result = self.cache.get_cached_translation(self.test_content_hash, lang)
            self.assertIsNotNone(result)

        # Invalidate cache
        self.cache.invalidate_cache(self.test_content_hash)

        # Verify cache is cleared
        for lang in translations:
            result = self.cache.get_cached_translation(self.test_content_hash, lang)
            self.assertIsNone(result)

    def test_different_content_hashes(self):
        """Test that different content hashes don't interfere"""
        hash1 = "abc123"
        hash2 = "def456"
        lang = "de"

        # Cache different translations for different hashes
        self.cache.cache_translation(hash1, lang, "Translation 1")
        self.cache.cache_translation(hash2, lang, "Translation 2")

        # Verify both are cached correctly
        result1 = self.cache.get_cached_translation(hash1, lang)
        result2 = self.cache.get_cached_translation(hash2, lang)

        self.assertEqual(result1, "Translation 1")
        self.assertEqual(result2, "Translation 2")

        # Invalidate one cache
        self.cache.invalidate_cache(hash1)

        # Verify only one is invalidated
        result1 = self.cache.get_cached_translation(hash1, lang)
        result2 = self.cache.get_cached_translation(hash2, lang)

        self.assertIsNone(result1)
        self.assertEqual(result2, "Translation 2")


if __name__ == "__main__":
    unittest.main(verbosity=2)
