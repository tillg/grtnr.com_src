"""
Automatic Translation Plugin for Pelican

AI-powered automatic translation plugin that creates translations of articles and pages.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

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
        
        # Get all articles and pages
        articles = self.context.get('articles', [])
        pages = self.context.get('pages', [])
        
        # Process articles
        for article in articles:
            if self._should_translate_content(article):
                self._translate_content(article)
        
        # Process pages
        for page in pages:
            if self._should_translate_content(page):
                self._translate_content(page)
        
        logger.info("Automatic translation generation completed")
    
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
        
        logger.info(f"Translating content: {content.title}")
        
        # Get source content
        source_content = self._get_source_content(content)
        if not source_content:
            logger.warning(f"Could not read source content for: {content.title}")
            return
        
        # Detect source language
        source_lang = self.translation_service.detect_language(source_content)
        logger.debug(f"Detected source language: {source_lang}")
        
        # Translate to each target language
        for target_lang in self.config.target_languages:
            if target_lang == source_lang:
                logger.debug(f"Skipping translation to same language: {target_lang}")
                continue
            
            try:
                self._create_translation(content, source_content, source_lang, target_lang)
            except Exception as e:
                logger.error(f"Failed to translate {content.title} to {target_lang}: {e}")
    
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
        
        # Get translation
        result = self.translation_service.translate_content(
            source_content, source_lang, target_lang
        )
        
        if result.cached:
            logger.debug(f"Used cached translation for {target_lang}")
        else:
            logger.info(f"Generated new translation for {target_lang}")
        
        # Create output directory structure
        output_dir = self._get_translation_output_dir(content)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create translation filename
        translation_filename = self._get_translation_filename(content, target_lang)
        output_path = output_dir / translation_filename
        
        # Add translation metadata
        translation_content = self._add_translation_metadata(
            result.translation, 
            source_lang, 
            target_lang, 
            content
        )
        
        # Write translation file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translation_content)
            
            logger.info(f"Created translation: {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to write translation file {output_path}: {e}")
    
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
                                 target_lang: str, original_content) -> str:
        """Add metadata to translation"""
        
        # Extract existing metadata if present
        lines = translation.split('\n')
        has_frontmatter = lines and lines[0].strip() == '---'
        
        # Create translation metadata
        translation_meta = [
            f"Translation: {target_lang}",
            f"Source-Language: {source_lang}",
            f"Source-File: {getattr(original_content, 'source_path', '')}",
            f"Generated-By: automatic-translation-plugin",
            f"Generated-Date: {self._get_current_timestamp()}"
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