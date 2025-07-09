"""
Automatic Translation Plugin for Pelican

AI-powered automatic translation plugin that creates translations of articles and pages.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'extensions'))

try:
    from translation_service import TranslationService, TranslationConfig
    from translation_service.exceptions import TranslationError
except ImportError as e:
    # Graceful fallback if translation service is not available
    print(f"Translation service not available: {e}")
    TranslationService = None
    TranslationConfig = None
    TranslationError = Exception

from pelican import signals
from pelican.generators import Generator
from pelican.contents import Article, Page

# Import centralized logging
try:
    from logger_config import get_logger
    logger = get_logger('automatic_translation')
except ImportError:
    import logging
    logger = logging.getLogger('automatic_translation')


class TranslationGenerator(Generator):
    """Generator for creating automatic translations"""
    
    def __init__(self, context, settings, path, theme, output_path):
        super().__init__(context, settings, path, theme, output_path)
        
        # Initialize translation service
        self.translation_service = None
        self.config = None
        
        # Check if translation is enabled
        if not settings.get('TRANSLATION_ENABLED', False):
            logger.info("Automatic translation is disabled")
            return
        
        if TranslationService is None:
            logger.error("Translation service is not available - check dependencies")
            return
        
        try:
            # Suppress verbose HTTP logging from external libraries
            import logging
            logging.getLogger("httpx").setLevel(logging.WARNING)
            logging.getLogger("httpcore").setLevel(logging.WARNING)
            logging.getLogger("openai").setLevel(logging.WARNING)
            
            self.config = TranslationConfig.from_pelican_settings(settings)
            self.translation_service = TranslationService(self.config)
            logger.info(f"Translation service initialized for languages: {self.config.target_languages}")
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
    
    def generate_context(self):
        """Generate context for translations"""
        pass
    
    def generate_output(self, writer):
        """Generate translated content files"""
        
        if not self.translation_service:
            return
        
        logger.info("Starting automatic translation generation")
        
        # Filter content that needs translation
        translatable_content = self._filter_translatable_content()
        
        if not translatable_content:
            logger.info("No content needs translation")
            return
        
        # Process translations in parallel
        translation_stats = self._process_translations_batch(translatable_content)
        
        # Log final statistics
        self._log_translation_statistics(translation_stats)

    def _filter_translatable_content(self) -> List[Any]:
        """Filter content that needs translation and apply test limits."""
        
        # Get all articles and pages
        articles = self.context.get('articles', [])
        pages = self.context.get('pages', [])
        
        # Collect all content that needs translation
        all_content = []
        for article in articles:
            if self._should_translate_content(article):
                all_content.append(article)
        
        for page in pages:
            if self._should_translate_content(page):
                all_content.append(page)
        
        # Apply test limit if configured
        test_limit = os.environ.get('TRANSLATION_TEST_LIMIT')
        if test_limit and test_limit.isdigit():
            test_limit = int(test_limit)
            if len(all_content) > test_limit:
                all_content = all_content[:test_limit]
                logger.info(f"Applied test limit: processing only {test_limit} content items out of {len(articles) + len(pages)} total")
        
        logger.info(f"Processing {len(all_content)} content items for translation")
        return all_content

    def _process_translations_batch(self, content_list: List[Any]) -> Dict[str, int]:
        """Process content translations in parallel and return statistics."""
        
        # Process content in parallel (limit to avoid overwhelming the API)
        max_content_workers = min(len(content_list), self.config.max_concurrent_content)
        logger.debug(f"Using {max_content_workers} parallel workers for content processing")
        
        # Track translation statistics
        translation_stats = {
            'total_files_created': 0,
            'cache_hits': 0,
            'new_translations': 0,
            'errors': 0
        }
        
        with ThreadPoolExecutor(max_workers=max_content_workers) as executor:
            # Submit all content translation tasks
            futures = [executor.submit(self._translate_content, content) for content in content_list]
            
            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    stats = future.result()
                    if stats:
                        translation_stats['total_files_created'] += stats.get('files_created', 0)
                        translation_stats['cache_hits'] += stats.get('cache_hits', 0)
                        translation_stats['new_translations'] += stats.get('new_translations', 0)
                except Exception as e:
                    logger.error(f"Failed to process content: {e}")
                    translation_stats['errors'] += 1
        
        return translation_stats

    def _log_translation_statistics(self, translation_stats: Dict[str, int]):
        """Log final translation statistics."""
        
        logger.info(f"Translation completed: {translation_stats['total_files_created']} files created, "
                   f"{translation_stats['cache_hits']} cached, {translation_stats['new_translations']} new translations, "
                   f"{translation_stats['errors']} errors")
    
    def _should_translate_content(self, content) -> bool:
        """Check if content should be translated"""
        
        # Check if content is already a translation
        if hasattr(content, 'metadata') and content.metadata.get('translation_source'):
            return False
        
        # Check excluded categories
        if hasattr(content, 'category') and content.category:
            if self.config.should_exclude_category(content.category.name):
                logger.debug(f"Skipping translation for excluded category: {content.category.name}")
                return False
        
        # Check excluded paths
        content_path = getattr(content, 'source_path', '')
        if self.config.should_exclude_path(content_path):
            logger.debug(f"Skipping translation for excluded path: {content_path}")
            return False
        
        return True
    
    def _translate_content(self, content):
        """Translate content to all target languages"""
        
        logger.debug(f"Translating content: {content.title}")
        
        # Initialize statistics
        stats = {
            'files_created': 0,
            'cache_hits': 0,
            'new_translations': 0
        }
        
        # Get source content
        source_content = self._get_source_content(content)
        if not source_content:
            logger.warning(f"Could not read source content for: {content.title}")
            return stats
        
        # Detect source language
        source_lang = self.translation_service.detect_language(source_content)
        logger.debug(f"Detected source language: {source_lang}")
        
        # Translate to each target language in parallel
        target_languages = [lang for lang in self.config.target_languages if lang != source_lang]
        
        if not target_languages:
            logger.debug("No target languages to translate to")
            return stats
        
        # Use parallel processing for multiple languages
        max_workers = min(len(target_languages), self.config.max_concurrent_translations)
        logger.debug(f"Translating '{content.title}' to {len(target_languages)} languages using {max_workers} parallel workers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all translation tasks
            future_to_lang = {
                executor.submit(self._create_translation, content, source_content, source_lang, target_lang): target_lang
                for target_lang in target_languages
            }
            
            # Process completed translations
            for future in as_completed(future_to_lang):
                target_lang = future_to_lang[future]
                try:
                    translation_stats = future.result()  # This will raise any exception that occurred
                    if translation_stats:
                        stats['files_created'] += translation_stats.get('files_created', 0)
                        stats['cache_hits'] += translation_stats.get('cache_hits', 0)
                        stats['new_translations'] += translation_stats.get('new_translations', 0)
                    logger.debug(f"Completed translation to {target_lang}")
                except Exception as e:
                    logger.error(f"Failed to translate {content.title} to {target_lang}: {e}")
        
        return stats
    
    def _get_source_content(self, content) -> str:
        """Read source content from file"""
        
        source_path = getattr(content, 'source_path', None)
        if not source_path:
            return ""
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read source file {source_path}: {e}")
            return ""
    
    def _create_translation(self, content, source_content: str, source_lang: str, target_lang: str):
        """Create a translation file"""
        
        # Initialize statistics
        stats = {
            'files_created': 0,
            'cache_hits': 0,
            'new_translations': 0
        }
        
        # Get translation
        result = self.translation_service.translate_content(
            source_content, source_lang, target_lang
        )
        
        if result.cached:
            logger.debug(f"Used cached translation for {target_lang}")
            stats['cache_hits'] += 1
        else:
            logger.debug(f"Generated new translation for {target_lang}")
            stats['new_translations'] += 1
        
        # Create output directory structure
        output_dir = self._get_translation_output_dir(content)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create translation filename
        translation_filename = self._get_translation_filename(content, target_lang)
        output_path = output_dir / translation_filename
        
        # Clean markdown wrapper from translation before adding metadata
        cleaned_translation = self._clean_markdown_wrapper(result.translation)
        
        # Add translation metadata
        translation_content = self._add_translation_metadata(
            cleaned_translation, 
            source_lang, 
            target_lang, 
            content,
            result.model
        )
        
        # Write translation file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translation_content)
            
            logger.debug(f"Created translation: {output_path}")
            stats['files_created'] += 1
            
        except Exception as e:
            logger.error(f"Failed to write translation file {output_path}: {e}")
        
        return stats
    
    def _get_translation_output_dir(self, content) -> Path:
        """Get output directory for translations"""
        
        source_path = Path(getattr(content, 'source_path', ''))
        source_dir = source_path.parent
        
        # Create extensions directory within the content directory
        return source_dir / 'extensions'
    
    def _get_translation_filename(self, content, target_lang: str) -> str:
        """Get filename for translation"""
        
        source_path = Path(getattr(content, 'source_path', ''))
        base_name = source_path.stem
        
        # Add language suffix
        return f"{base_name}-{target_lang.upper()}.md"
    
    def _add_translation_metadata(self, translation: str, source_lang: str, 
                                 target_lang: str, original_content, model_name: str = None) -> str:
        """Add metadata to translation"""
        
        # Extract existing metadata if present
        lines = translation.split('\n')
        has_frontmatter = lines and lines[0].strip() == '---'
        
        # Use provided model name or fall back to config
        if not model_name:
            model_name = self.config.model if self.config else 'unknown'
        
        # Create translation metadata
        translation_meta = [
            f"Translation: {target_lang}",
            f"Source-Language: {source_lang}",
            f"Translator: {model_name}",
            f"Translate-Date: {self._get_current_timestamp()}",
            f"Source-File: {getattr(original_content, 'source_path', '')}",
            f"Generated-By: automatic-translation-plugin"
        ]
        
        if has_frontmatter:
            # Insert metadata into existing frontmatter
            end_marker = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_marker = i
                    break
            
            if end_marker:
                # Insert translation metadata before the closing ---
                lines[end_marker:end_marker] = translation_meta
            else:
                # Malformed frontmatter, add at the end
                lines.extend(['---'] + translation_meta + ['---'])
        else:
            # Add frontmatter with translation metadata
            lines = ['---'] + translation_meta + ['---', ''] + lines
        
        return '\n'.join(lines)
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _clean_markdown_wrapper(self, content: str) -> str:
        """Remove markdown code block wrapper if present"""
        original_content = content
        content = content.strip()
        
        # Pattern: ```markdown followed by content followed by ```
        if content.startswith('```markdown'):
            # Find the closing ```
            lines = content.split('\n')
            if len(lines) > 2:
                # Look for the first closing ``` after the opening
                for i in range(len(lines) - 1, 0, -1):  # Search backwards
                    if lines[i].strip() == '```':
                        # Extract content between the markers
                        inner_content = '\n'.join(lines[1:i])
                        content = inner_content
                        logger.debug("Removed ```markdown wrapper from translation")
                        break
        
        # Pattern: ``` followed by content followed by ```
        elif content.startswith('```') and not content.startswith('```markdown'):
            lines = content.split('\n')
            if len(lines) > 2:
                # Look for the first closing ``` after the opening
                for i in range(len(lines) - 1, 0, -1):  # Search backwards
                    if lines[i].strip() == '```':
                        # Extract content between the markers
                        inner_content = '\n'.join(lines[1:i])
                        content = inner_content
                        logger.debug("Removed ``` wrapper from translation")
                        break
        
        content = content.strip()
        
        # Log if we cleaned something
        if content != original_content.strip():
            logger.info(f"Cleaned markdown wrapper from translation (original: {len(original_content)} chars, cleaned: {len(content)} chars)")
        
        return content


def get_generators(pelican_object):
    """Register the translation generator"""
    if pelican_object.settings.get('TRANSLATION_ENABLED', False):
        return TranslationGenerator
    return None


def initialize_translation_service(sender):
    """Initialize translation service on Pelican startup"""
    
    settings = sender.settings
    
    if not settings.get('TRANSLATION_ENABLED', False):
        return
    
    logger.info("Initializing automatic translation service")
    
    try:
        # Test translation service setup
        config = TranslationConfig.from_pelican_settings(settings)
        service = TranslationService(config)
        
        # Run health check
        health = service.health_check()
        if health['status'] == 'healthy':
            logger.info("Translation service health check passed")
        else:
            logger.warning(f"Translation service health check failed: {health}")
            
    except Exception as e:
        logger.error(f"Failed to initialize translation service: {e}")


def register():
    """Register plugin with Pelican"""
    signals.initialized.connect(initialize_translation_service)
    signals.get_generators.connect(get_generators)