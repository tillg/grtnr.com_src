"""
Pelican plugin for automatic article translation.
Integrates with the existing plugin system to provide translation capabilities.
"""

import os
import sys
from typing import List

from pelican import signals

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger
from translation_service import TranslationService, TranslationError
from file_organization import ExtensionFileManager

logger = get_logger("automatic_translation")


class AutomaticTranslationPlugin:
    """Main plugin class for automatic translation functionality."""

    def __init__(self):
        self.translation_service = None
        self.file_manager = None
        self.target_languages = []
        self.enabled = False
        self.exclude_categories = []
        self.exclude_paths = []

    def initialize(self, pelican_instance):
        """Initialize the plugin with Pelican settings."""
        settings = pelican_instance.settings

        # Check if translation is enabled
        self.enabled = settings.get('TRANSLATION_ENABLED', False)
        if not self.enabled:
            logger.info("Automatic translation is disabled")
            return

        # Get target languages from settings
        self.target_languages = settings.get('TRANSLATION_TARGET_LANGUAGES',
                                             ['de', 'fr'])
        if not self.target_languages:
            logger.warning("No target languages specified, "
                           "disabling translation")
            self.enabled = False
            return

        # Get exclusion settings
        self.exclude_categories = settings.get(
            'TRANSLATION_EXCLUDE_CATEGORIES', [])
        self.exclude_paths = settings.get('TRANSLATION_EXCLUDE_PATHS', [])

        # Initialize services
        cache_dir = settings.get('CACHE_PATH', 'cache')
        self.translation_service = TranslationService(cache_dir=cache_dir)
        self.file_manager = ExtensionFileManager(
            content_root=settings.get('PATH', 'content'))

        logger.info(f"Automatic translation initialized for languages: "
                    f"{self.target_languages}")

    def should_translate_content(self, content) -> bool:
        """Check if content should be translated."""
        if not self.enabled:
            return False

        # Skip translation files themselves to avoid recursive translation
        if hasattr(content, 'source_path'):
            source_path = content.source_path
            if '/extensions/' in source_path:
                logger.debug(f"Skipping translation file: {source_path}")
                return False

        # Check category exclusions
        if hasattr(content, 'category') and content.category:
            category_name = getattr(content.category, 'name', str(content.category))
            if category_name in self.exclude_categories:
                logger.debug(f"Skipping translation for excluded category: "
                             f"{category_name}")
                return False

        # Check path exclusions
        if hasattr(content, 'source_path'):
            source_path = content.source_path
            for exclude_path in self.exclude_paths:
                if exclude_path in source_path:
                    logger.debug(f"Skipping translation for excluded path: "
                                 f"{source_path}")
                    return False

        # Skip recipe files - they're handled separately if needed
        if hasattr(content, 'source_path') and '/recipes/' in content.source_path:
            logger.debug(f"Skipping recipe file: {content.source_path}")
            return False

        return True

    def translate_article(self, article):
        """Translate an individual article."""
        if not self.should_translate_content(article):
            return

        source_path = article.source_path
        logger.info(f"Processing article for translation: {source_path}")

        # Get the original content
        original_content = self._get_content_without_metadata(article)

        # Calculate file hash for caching
        file_hash = self.translation_service.cache.get_file_hash(source_path)

        for target_lang in self.target_languages:
            try:
                # Check if translation already exists and is current
                if self.file_manager.is_translation_current(
                        source_path, target_lang, file_hash):
                    logger.debug(f"Translation {source_path} -> {target_lang} "
                                 f"is current, skipping")
                    continue

                # Translate the content
                translated_content, source_lang = (
                    self.translation_service.translate_content(
                        original_content, source_path, target_lang))

                # Skip if source equals target language
                if source_lang == target_lang:
                    continue

                # Write the translation file
                self.file_manager.write_translation_file(
                    source_path, target_lang, translated_content,
                    source_lang, file_hash)

                logger.info(f"Created translation: {source_path} "
                            f"({source_lang} -> {target_lang})")

            except TranslationError as e:
                logger.error(f"Translation failed for {source_path} -> "
                             f"{target_lang}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error translating {source_path}: {e}")

        # Cleanup old translation files
        self.file_manager.cleanup_old_translations(source_path,
                                                   self.target_languages)

    def translate_page(self, page):
        """Translate an individual page."""
        if not self.should_translate_content(page):
            return

        source_path = page.source_path
        logger.info(f"Processing page for translation: {source_path}")

        # Get the original content
        original_content = self._get_content_without_metadata(page)

        # Calculate file hash for caching
        file_hash = self.translation_service.cache.get_file_hash(source_path)

        for target_lang in self.target_languages:
            try:
                # Check if translation already exists and is current
                if self.file_manager.is_translation_current(
                        source_path, target_lang, file_hash):
                    logger.debug(f"Translation {source_path} -> {target_lang} "
                                 f"is current, skipping")
                    continue

                # Translate the content
                translated_content, source_lang = (
                    self.translation_service.translate_content(
                        original_content, source_path, target_lang))

                # Skip if source equals target language
                if source_lang == target_lang:
                    continue

                # Write the translation file
                self.file_manager.write_translation_file(
                    source_path, target_lang, translated_content,
                    source_lang, file_hash)

                logger.info(f"Created translation: {source_path} "
                            f"({source_lang} -> {target_lang})")

            except TranslationError as e:
                logger.error(f"Translation failed for {source_path} -> "
                             f"{target_lang}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error translating {source_path}: {e}")

        # Cleanup old translation files
        self.file_manager.cleanup_old_translations(source_path,
                                                   self.target_languages)

    def _get_content_without_metadata(self, content_obj) -> str:
        """Extract content without frontmatter metadata."""
        if hasattr(content_obj, '_content'):
            # Use the processed content
            return content_obj._content
        elif hasattr(content_obj, 'source_path'):
            # Read the file and extract content after metadata
            try:
                with open(content_obj.source_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                # Skip frontmatter if present
                if file_content.startswith('---'):
                    lines = file_content.split('\n')
                    frontmatter_end = -1
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            frontmatter_end = i
                            break

                    if frontmatter_end != -1:
                        return '\n'.join(lines[frontmatter_end + 1:])

                return file_content
            except Exception as e:
                logger.error(f"Failed to read content from "
                             f"{content_obj.source_path}: {e}")
                return ""
        else:
            logger.warning("Could not extract content from object")
            return ""


# Global plugin instance
plugin_instance = AutomaticTranslationPlugin()


def pelican_init(pelican_instance):
    """Initialize the plugin when Pelican starts."""
    plugin_instance.initialize(pelican_instance)


def translate_articles(generator):
    """Process articles for translation."""
    if not plugin_instance.enabled:
        return

    logger.info("Starting automatic translation of articles")

    # Process regular articles
    if hasattr(generator, 'articles'):
        for article in generator.articles:
            plugin_instance.translate_article(article)

    # Process hidden articles
    if hasattr(generator, 'hidden_articles'):
        for article in generator.hidden_articles:
            plugin_instance.translate_article(article)

    logger.info("Finished automatic translation of articles")


def translate_pages(generator):
    """Process pages for translation."""
    if not plugin_instance.enabled:
        return

    logger.info("Starting automatic translation of pages")

    # Process regular pages
    if hasattr(generator, 'pages'):
        for page in generator.pages:
            plugin_instance.translate_page(page)

    # Process hidden pages
    if hasattr(generator, 'hidden_pages'):
        for page in generator.hidden_pages:
            plugin_instance.translate_page(page)

    logger.info("Finished automatic translation of pages")


def register():
    """Register the plugin with Pelican."""
    # Connect to initialization signal
    signals.initialized.connect(pelican_init)

    # Connect to content generation signals
    # Run after content processing but before finalization
    signals.article_generator_finalized.connect(translate_articles)
    signals.page_generator_finalized.connect(translate_pages)