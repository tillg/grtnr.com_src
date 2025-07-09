"""
Tests for the translation service functionality.
"""

import os
import tempfile
import shutil
import sys
import unittest
from unittest.mock import Mock, patch

# Add the plugins directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins'))

from translation_service import (
    TranslationService, TranslationCache, MockLanguageDetector,
    MockTranslator, TranslationError
)
from file_organization import ExtensionFileManager


class TestMockLanguageDetector(unittest.TestCase):
    """Test the mock language detector."""

    def setUp(self):
        self.detector = MockLanguageDetector()

    def test_detect_english_default(self):
        """Test detection of English as default."""
        text = "This is an English text with some content."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "en")

    def test_detect_german(self):
        """Test detection of German text."""
        text = "Das ist ein deutscher Text mit der und die und ich bin."
        result = self.detector.detect_language(text)
        self.assertEqual(result, "de")

    def test_detect_custom_default(self):
        """Test custom default language."""
        detector = MockLanguageDetector(default_language="fr")
        text = "This is English text."
        result = detector.detect_language(text)
        self.assertEqual(result, "fr")


class TestMockTranslator(unittest.TestCase):
    """Test the mock translator."""

    def setUp(self):
        self.translator = MockTranslator()

    def test_translate_same_language(self):
        """Test translation when source equals target."""
        text = "Hello world"
        result = self.translator.translate(text, "en", "en")
        self.assertEqual(result, text)

    def test_translate_different_languages(self):
        """Test translation between different languages."""
        text = "Hello world"
        result = self.translator.translate(text, "en", "de")
        self.assertEqual(result, "[en→de] Hello world")


class TestTranslationCache(unittest.TestCase):
    """Test the translation cache functionality."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cache = TranslationCache(cache_dir=self.test_dir)
        
        # Create a test file
        self.test_file = os.path.join(self.test_dir, "test.md")
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("# Test Content\nThis is test content.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_file_hash(self):
        """Test file hash calculation."""
        hash1 = self.cache.get_file_hash(self.test_file)
        self.assertTrue(len(hash1) == 64)  # SHA-256 hash length
        
        # Hash should be consistent
        hash2 = self.cache.get_file_hash(self.test_file)
        self.assertEqual(hash1, hash2)

    def test_cache_key_generation(self):
        """Test cache key generation."""
        key = self.cache.get_cache_key("/path/to/file.md", "de")
        self.assertEqual(key, "/path/to/file.md:de")

    def test_cache_translation(self):
        """Test caching and retrieving translations."""
        file_path = self.test_file
        target_language = "de"
        translation = "Translated content"
        
        # Cache should be empty initially
        self.assertFalse(self.cache.is_cached(file_path, target_language))
        self.assertIsNone(self.cache.get_cached_translation(file_path, target_language))
        
        # Cache the translation
        self.cache.cache_translation(file_path, target_language, translation)
        
        # Should now be cached
        self.assertTrue(self.cache.is_cached(file_path, target_language))
        cached_translation = self.cache.get_cached_translation(file_path, target_language)
        self.assertEqual(cached_translation, translation)

    def test_cache_invalidation_on_file_change(self):
        """Test that cache is invalidated when file changes."""
        file_path = self.test_file
        target_language = "de"
        translation = "Translated content"
        
        # Cache the translation
        self.cache.cache_translation(file_path, target_language, translation)
        self.assertTrue(self.cache.is_cached(file_path, target_language))
        
        # Modify the file
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write("\nAdditional content.")
        
        # Cache should be invalidated
        self.assertFalse(self.cache.is_cached(file_path, target_language))


class TestTranslationService(unittest.TestCase):
    """Test the main translation service."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.service = TranslationService(cache_dir=self.test_dir)
        
        # Create a test file
        self.test_file = os.path.join(self.test_dir, "test.md")
        self.test_content = "This is test content for translation."
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(self.test_content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_translate_content_same_language(self):
        """Test translation when source equals target language."""
        translated, source_lang = self.service.translate_content(
            self.test_content, self.test_file, "en")
        
        self.assertEqual(translated, self.test_content)
        self.assertEqual(source_lang, "en")

    def test_translate_content_different_languages(self):
        """Test translation between different languages."""
        translated, source_lang = self.service.translate_content(
            self.test_content, self.test_file, "de")
        
        self.assertTrue(translated.startswith("[en→de]"))
        self.assertEqual(source_lang, "en")

    def test_caching_functionality(self):
        """Test that caching works correctly."""
        # First translation
        translated1, _ = self.service.translate_content(
            self.test_content, self.test_file, "de")
        
        # Second translation should use cache
        with patch.object(self.service.translator, 'translate') as mock_translate:
            translated2, _ = self.service.translate_content(
                self.test_content, self.test_file, "de")
            
            # Translator should not be called due to caching
            mock_translate.assert_not_called()
            self.assertEqual(translated1, translated2)

    def test_get_available_languages(self):
        """Test getting available languages."""
        languages = self.service.get_available_languages()
        self.assertIsInstance(languages, list)
        self.assertIn("en", languages)
        self.assertIn("de", languages)


class TestExtensionFileManager(unittest.TestCase):
    """Test the extension file manager."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.manager = ExtensionFileManager(content_root=self.test_dir)
        
        # Create a test content structure
        self.article_dir = os.path.join(self.test_dir, "articles", "2025-01-01-test-article")
        os.makedirs(self.article_dir, exist_ok=True)
        
        self.test_file = os.path.join(self.article_dir, "2025-01-01-test-article.md")
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("---\ntitle: Test Article\n---\n\nThis is test content.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_extensions_dir(self):
        """Test getting extensions directory path."""
        extensions_dir = self.manager.get_extensions_dir(self.test_file)
        expected = os.path.join(self.article_dir, "extensions")
        self.assertEqual(extensions_dir, expected)

    def test_ensure_extensions_dir(self):
        """Test creating extensions directory."""
        extensions_dir = self.manager.ensure_extensions_dir(self.test_file)
        self.assertTrue(os.path.exists(extensions_dir))
        self.assertTrue(os.path.isdir(extensions_dir))

    def test_get_base_filename(self):
        """Test getting base filename."""
        base_filename = self.manager.get_base_filename(self.test_file)
        self.assertEqual(base_filename, "2025-01-01-test-article")

    def test_get_translation_filename(self):
        """Test generating translation filename."""
        filename = self.manager.get_translation_filename(self.test_file, "de")
        self.assertEqual(filename, "2025-01-01-test-article-DE.md")

    def test_write_translation_file(self):
        """Test writing translation file."""
        translated_content = "Das ist Testinhalt."
        file_hash = "test_hash_123"
        
        self.manager.write_translation_file(
            self.test_file, "de", translated_content, "en", file_hash)
        
        # Check that file was created
        translation_path = self.manager.get_translation_file_path(self.test_file, "de")
        self.assertTrue(os.path.exists(translation_path))
        
        # Check file content
        with open(translation_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("source-language: en", content)
        self.assertIn("target-language: de", content)
        self.assertIn("hash-on-last-created: test_hash_123", content)
        self.assertIn(translated_content, content)

    def test_get_existing_translations(self):
        """Test getting list of existing translations."""
        # Initially no translations
        translations = self.manager.get_existing_translations(self.test_file)
        self.assertEqual(translations, [])
        
        # Create some translation files
        self.manager.write_translation_file(
            self.test_file, "de", "German content", "en", "hash1")
        self.manager.write_translation_file(
            self.test_file, "fr", "French content", "en", "hash2")
        
        # Should find both translations
        translations = self.manager.get_existing_translations(self.test_file)
        self.assertIn("de", translations)
        self.assertIn("fr", translations)
        self.assertEqual(len(translations), 2)

    def test_is_translation_current(self):
        """Test checking if translation is current."""
        file_hash = "current_hash"
        
        # Create translation file
        self.manager.write_translation_file(
            self.test_file, "de", "German content", "en", file_hash)
        
        # Should be current with same hash
        self.assertTrue(self.manager.is_translation_current(
            self.test_file, "de", file_hash))
        
        # Should not be current with different hash
        self.assertFalse(self.manager.is_translation_current(
            self.test_file, "de", "different_hash"))

    def test_cleanup_old_translations(self):
        """Test cleanup of old translation files."""
        # Create multiple translation files
        self.manager.write_translation_file(
            self.test_file, "de", "German", "en", "hash1")
        self.manager.write_translation_file(
            self.test_file, "fr", "French", "en", "hash2")
        self.manager.write_translation_file(
            self.test_file, "it", "Italian", "en", "hash3")
        
        # Cleanup, keeping only German and French
        self.manager.cleanup_old_translations(self.test_file, ["de", "fr"])
        
        # Check which files remain
        translations = self.manager.get_existing_translations(self.test_file)
        self.assertIn("de", translations)
        self.assertIn("fr", translations)
        self.assertNotIn("it", translations)


class TestTranslationServiceErrors(unittest.TestCase):
    """Test error handling in translation service."""

    def test_translation_error_handling(self):
        """Test handling of translation errors."""
        # Create a translator that always raises an exception
        class FailingTranslator:
            def translate(self, text, source_lang, target_lang):
                raise Exception("Translation service unavailable")
        
        service = TranslationService(translator=FailingTranslator())
        
        with self.assertRaises(TranslationError):
            service.translate_content("test content", "/fake/path", "de")


if __name__ == '__main__':
    unittest.main()