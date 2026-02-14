"""
Automatic Translation Plugin for Pelican

AI-powered automatic translation plugin that creates translations of articles and pages.
"""

import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "extensions"))

try:
    from translation_service import TranslationConfig, TranslationService
    from translation_service.exceptions import TranslationError
except ImportError as e:
    # Graceful fallback if translation service is not available
    print(f"Translation service not available: {e}")
    TranslationService = None
    TranslationConfig = None
    TranslationError = Exception

from pelican import signals
from pelican.contents import Article, Page
from pelican.generators import Generator

# Import new translation utilities
from translation_utils import (
    cleanup_old_translations,
    get_translation_path,
    translate_document,
)

# Import centralized logging
try:
    from logger_config import get_logger

    logger = get_logger("automatic_translation")
except ImportError:
    import logging

    logger = logging.getLogger("automatic_translation")


class TranslationGenerator(Generator):
    """Generator for creating automatic translations"""

    def __init__(self, context, settings, path, theme, output_path):
        super().__init__(context, settings, path, theme, output_path)

        # Check if translation is enabled
        if not settings.get("TRANSLATION_ENABLED", False):
            logger.info("Automatic translation is disabled")
            self.config = None
            return

        if TranslationService is None:
            logger.error("Translation service is not available - check dependencies")
            self.config = None
            return

        try:
            # Suppress verbose HTTP logging from external libraries
            import logging

            logging.getLogger("httpx").setLevel(logging.WARNING)
            logging.getLogger("httpcore").setLevel(logging.WARNING)
            logging.getLogger("openai").setLevel(logging.WARNING)

            self.config = TranslationConfig.from_pelican_settings(settings)
            logger.info(
                f"Translation service initialized for languages: {self.config.target_languages}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
            self.config = None

    def generate_context(self):
        """Generate context for translations"""
        pass

    def generate_output(self, writer):
        """Generate translated content files"""

        if not self.config:
            return

        logger.info("Starting automatic translation generation")

        # Filter content that needs translation
        translatable_content = self._filter_translatable_content()

        if not translatable_content:
            logger.info("No content needs translation")
            return

        # Process translations using the new simplified approach
        translation_stats = self._process_translations_simplified(translatable_content)

        # Log final statistics
        self._log_translation_statistics(translation_stats)

    def _filter_translatable_content(self) -> List[Any]:
        """Filter content that needs translation and apply test limits."""

        # Get articles and pages from context
        # NOTE: This should now get all articles since we're accessing them before filtering
        articles = self.context.get("articles", [])
        pages = self.context.get("pages", [])

        logger.info(f"Found {len(articles)} articles and {len(pages)} pages in context")

        # Collect all content that needs translation
        all_content = []
        for article in articles:
            if self._should_translate_content(article):
                all_content.append(article)

        for page in pages:
            if self._should_translate_content(page):
                all_content.append(page)

        # Apply test limit if configured
        test_limit = os.environ.get("TRANSLATION_TEST_LIMIT")
        if test_limit and test_limit.isdigit():
            test_limit = int(test_limit)
            if len(all_content) > test_limit:
                all_content = all_content[:test_limit]
                logger.info(
                    f"Applied test limit: processing only {test_limit} content items out of {len(all_content)} total"
                )

        logger.info(f"Processing {len(all_content)} content items for translation")
        return all_content

    def _process_translations_simplified(
        self, content_list: List[Any]
    ) -> Dict[str, int]:
        """Process content translations using the simplified approach."""

        # Track translation statistics
        translation_stats = {"total_files_created": 0, "up_to_date": 0, "errors": 0}

        # Process each content item
        for content in content_list:
            try:
                stats = self._translate_content_simplified(content)
                if stats:
                    translation_stats["total_files_created"] += stats.get(
                        "files_created", 0
                    )
                    translation_stats["up_to_date"] += stats.get("up_to_date", 0)
            except Exception as e:
                logger.error(f"Failed to process content {content.title}: {e}")
                translation_stats["errors"] += 1

        return translation_stats

    def _log_translation_statistics(self, translation_stats: Dict[str, int]):
        """Log final translation statistics."""

        logger.info(
            f"Translation completed: {translation_stats['total_files_created']} files created, "
            f"{translation_stats['up_to_date']} up to date, "
            f"{translation_stats['errors']} errors"
        )

    def _should_translate_content(self, content) -> bool:
        """Check if content should be translated"""

        # Check if content is already a translation
        if hasattr(content, "metadata") and content.metadata.get("translation"):
            return False

        # Check excluded categories
        if hasattr(content, "category") and content.category:
            if self.config.should_exclude_category(content.category.name):
                logger.debug(
                    f"Skipping translation for excluded category: {content.category.name}"
                )
                return False

        # Check excluded paths
        content_path = getattr(content, "source_path", "")
        if self.config.should_exclude_path(content_path):
            logger.debug(f"Skipping translation for excluded path: {content_path}")
            return False

        return True

    def _translate_content_simplified(self, content):
        """Translate content to all target languages using simplified approach"""

        logger.debug(f"Translating content: {content.title}")

        # Initialize statistics
        stats = {"files_created": 0, "up_to_date": 0}

        # Get source path
        source_path = Path(getattr(content, "source_path", ""))
        if not source_path.exists():
            logger.warning(f"Source path does not exist: {source_path}")
            return stats

        # Translate to each target language
        for target_lang in self.config.target_languages:
            try:
                target_path = get_translation_path(source_path, target_lang)

                # Use the simplified translate_document function
                # Pass content.title so auto-generated titles get translated
                was_updated = translate_document(
                    source_path,
                    target_lang,
                    target_path,
                    self.settings,
                    title=content.title,
                )

                if was_updated:
                    stats["files_created"] += 1
                    logger.debug(f"Created/updated translation for {target_lang}")
                else:
                    stats["up_to_date"] += 1
                    logger.debug(
                        f"Translation for {target_lang} was already up to date"
                    )

            except Exception as e:
                logger.error(
                    f"Failed to translate {content.title} to {target_lang}: {e}"
                )

        return stats


# Old generator registration is no longer needed
# Translation now runs via signal handler to access all articles before filtering


def initialize_translation_service(sender):
    """Initialize translation service on Pelican startup"""

    settings = sender.settings

    if not settings.get("TRANSLATION_ENABLED", False):
        return

    logger.info("Initializing automatic translation service")

    try:
        # Test translation service setup
        config = TranslationConfig.from_pelican_settings(settings)
        service = TranslationService(config)

        # Run health check
        health = service.health_check()
        if health["status"] == "healthy":
            logger.info("Translation service health check passed")
        else:
            logger.warning(f"Translation service health check failed: {health}")

    except Exception as e:
        logger.error(f"Failed to initialize translation service: {e}")


def translate_all_articles(article_generator):
    """Translate all articles after they're loaded but before filtering"""

    if not article_generator.settings.get("TRANSLATION_ENABLED", False):
        logger.info("Automatic translation is disabled")
        return

    logger.info(
        f"Translation plugin running with {len(article_generator.articles)} articles"
    )

    try:
        # Create a translation generator with the full context
        translation_generator = TranslationGenerator(
            context=article_generator.context,
            settings=article_generator.settings,
            path=article_generator.path,
            theme=article_generator.theme,
            output_path=article_generator.output_path,
        )

        if translation_generator.config:
            # Override the context with ALL articles from the generator
            translation_generator.context["articles"] = article_generator.articles
            logger.info(
                f"Using all {len(article_generator.articles)} articles for translation"
            )

            # Run the translation process
            translation_generator.generate_output(None)

    except Exception as e:
        logger.error(f"Failed to run translation process: {e}")


def register():
    """Register plugin with Pelican"""
    signals.initialized.connect(initialize_translation_service)
    # Register to run after articles are loaded but before filtering
    signals.article_generator_finalized.connect(translate_all_articles)
