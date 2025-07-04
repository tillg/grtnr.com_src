"""
Multilingual Site Plugin for Pelican

This plugin creates a multilingual website structure by:
1. Generating language-specific versions of all content
2. Creating proper URL structures for each language
3. Providing language switching functionality
4. Adding SEO-friendly hreflang tags
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pelican import signals
from pelican.generators import Generator
from pelican.contents import Article, Page
from pelican.writers import Writer

# Import centralized logging
try:
    from logger_config import get_logger
    logger = get_logger('multilingual_site')
except ImportError:
    import logging
    logger = logging.getLogger('multilingual_site')

# Import normalize_slug function
from normalize_slugs import normalize_slug


class StaticURLGenerator:
    """Generates static URLs for all languages during build"""
    
    def __init__(self, default_lang='en', supported_langs=None):
        if supported_langs is None:
            supported_langs = ['en', 'de', 'fr']
        self.default_lang = default_lang
        self.supported_langs = supported_langs
    
    def generate_language_urls(self, content_slug: str, translations: Dict[str, str]) -> Dict[str, str]:
        """Generate URLs for all language versions of content"""
        urls = {}
        for lang in self.supported_langs:
            if lang in translations:
                translated_slug = translations[lang]
                urls[lang] = f"/{lang}/{translated_slug}/"
            else:
                # Fallback to default language slug
                urls[lang] = f"/{lang}/{content_slug}/"
        return urls
    
    def get_canonical_url(self, content_slug: str, lang: str) -> str:
        """Get canonical URL for SEO purposes"""
        return f"/{lang}/{content_slug}/"


class MultilingualContentProcessor:
    """Transforms content for multilingual output"""
    
    def __init__(self, settings):
        self.settings = settings
        self.default_lang = settings.get('DEFAULT_LANG', 'en')
        self.supported_langs = settings.get('MULTILINGUAL_LANGUAGES', ['en', 'de', 'fr'])
        self.url_generator = StaticURLGenerator(self.default_lang, self.supported_langs)
    
    def process_articles(self, articles: List[Article]) -> Dict[str, List[Article]]:
        """Process articles for each language"""
        processed_articles = {lang: [] for lang in self.supported_langs}
        
        for article in articles:
            # Skip translation files themselves
            if self._is_translation_file(article):
                continue
            
            # Process original content
            original_lang = self._detect_content_language(article)
            processed_articles[original_lang].append(article)
            
            # Add language-specific metadata
            article.lang = original_lang
            article.multilingual_urls = self._get_multilingual_urls(article)
            
            # Process translations
            translations = self._find_translations(article)
            for lang, translated_content in translations.items():
                if lang != original_lang:
                    translated_article = self._create_translated_article(article, translated_content, lang)
                    processed_articles[lang].append(translated_article)
        
        return processed_articles
    
    def process_pages(self, pages: List[Page]) -> Dict[str, List[Page]]:
        """Process pages for each language"""
        processed_pages = {lang: [] for lang in self.supported_langs}
        
        for page in pages:
            # Skip translation files themselves
            if self._is_translation_file(page):
                continue
            
            # Process original content
            original_lang = self._detect_content_language(page)
            processed_pages[original_lang].append(page)
            
            # Add language-specific metadata
            page.lang = original_lang
            page.multilingual_urls = self._get_multilingual_urls(page)
            
            # Process translations
            translations = self._find_translations(page)
            for lang, translated_content in translations.items():
                if lang != original_lang:
                    translated_page = self._create_translated_page(page, translated_content, lang)
                    processed_pages[lang].append(translated_page)
        
        return processed_pages
    
    def _is_translation_file(self, content) -> bool:
        """Check if content is a translation file"""
        source_path = getattr(content, 'source_path', '')
        return '/extensions/' in source_path
    
    def _detect_content_language(self, content) -> str:
        """Detect the language of content"""
        # For now, assume all original content is in default language
        # This could be enhanced with actual language detection
        return self.default_lang
    
    def _find_translations(self, content) -> Dict[str, str]:
        """Find translation files for given content"""
        translations = {}
        
        source_path = Path(getattr(content, 'source_path', ''))
        if not source_path.exists():
            return translations
        
        # Look for translations in extensions directory
        extensions_dir = source_path.parent / 'extensions'
        if not extensions_dir.exists():
            return translations
        
        base_name = source_path.stem
        
        # Find translation files
        for lang in self.supported_langs:
            if lang == self.default_lang:
                continue
            
            translation_file = extensions_dir / f"{base_name}-{lang.upper()}.md"
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        translations[lang] = f.read()
                except Exception as e:
                    logger.error(f"Failed to read translation file {translation_file}: {e}")
        
        return translations
    
    def _get_multilingual_urls(self, content) -> Dict[str, str]:
        """Get multilingual URLs for content"""
        content_slug = getattr(content, 'slug', '')
        translations = self._find_translations(content)
        
        # Create a mapping of language to translated slugs
        translated_slugs = {}
        for lang in self.supported_langs:
            if lang in translations:
                # Extract slug from translation metadata if available
                translated_slugs[lang] = self._extract_translated_slug(translations[lang], content_slug)
            else:
                translated_slugs[lang] = content_slug
        
        return self.url_generator.generate_language_urls(content_slug, translated_slugs)
    
    def _extract_translated_slug(self, translation_content: str, fallback_slug: str) -> str:
        """Extract or generate translated slug from content"""
        # For now, use the original slug
        # This could be enhanced to translate slugs as well
        return fallback_slug
    
    def _create_translated_article(self, original_article: Article, translation_content: str, lang: str) -> Article:
        """Create a translated article object"""
        # Parse the translation content
        metadata, content = self._parse_translation_content(translation_content)
        
        # Create new article with translated content
        translated_article = Article(
            content=content,
            metadata=metadata,
            source_path=original_article.source_path,
            context=original_article._context
        )
        
        # Set language-specific attributes
        translated_article.lang = lang
        translated_article.original_article = original_article
        translated_article.multilingual_urls = original_article.multilingual_urls
        
        # Update URLs for this language
        translated_article.save_as = f"{lang}/{translated_article.slug}/index.html"
        translated_article.url = f"/{lang}/{translated_article.slug}/"
        
        return translated_article
    
    def _create_translated_page(self, original_page: Page, translation_content: str, lang: str) -> Page:
        """Create a translated page object"""
        # Parse the translation content
        metadata, content = self._parse_translation_content(translation_content)
        
        # Create new page with translated content
        translated_page = Page(
            content=content,
            metadata=metadata,
            source_path=original_page.source_path,
            context=original_page._context
        )
        
        # Set language-specific attributes
        translated_page.lang = lang
        translated_page.original_page = original_page
        translated_page.multilingual_urls = original_page.multilingual_urls
        
        # Update URLs for this language
        translated_page.save_as = f"{lang}/{translated_page.slug}/index.html"
        translated_page.url = f"/{lang}/{translated_page.slug}/"
        
        return translated_page
    
    def _parse_translation_content(self, content: str) -> Tuple[Dict, str]:
        """Parse translation content into metadata and body"""
        lines = content.split('\n')
        metadata = {}
        body_start = 0
        
        # Check for frontmatter
        if lines and lines[0].strip() == '---':
            body_start = 1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    body_start = i + 1
                    break
                
                # Parse metadata
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        body = '\n'.join(lines[body_start:])
        return metadata, body


class LanguageSwitcher:
    """Language switching UI component"""
    
    def __init__(self, supported_langs=None):
        if supported_langs is None:
            supported_langs = ['en', 'de', 'fr']
        self.supported_langs = supported_langs
        self.lang_names = {
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'es': 'Español',
            'it': 'Italiano'
        }
    
    def generate_language_links(self, current_url: str, current_lang: str) -> List[Dict]:
        """Generate language switching links"""
        links = []
        
        for lang in self.supported_langs:
            if lang == current_lang:
                continue
            
            # Generate equivalent URL in target language
            equivalent_url = self.get_equivalent_url(current_url, lang)
            
            links.append({
                'code': lang,
                'name': self.lang_names.get(lang, lang.upper()),
                'url': equivalent_url
            })
        
        return links
    
    def get_equivalent_url(self, url: str, target_lang: str) -> str:
        """Find equivalent URL in target language"""
        # Simple implementation - replace language code in URL
        # This could be enhanced with actual URL mapping
        
        # Remove leading/trailing slashes
        url = url.strip('/')
        
        # Split URL parts
        parts = url.split('/')
        
        # If URL starts with language code, replace it
        if parts and parts[0] in self.supported_langs:
            parts[0] = target_lang
        else:
            # Add language code at the beginning
            parts = [target_lang] + parts
        
        return '/' + '/'.join(parts) + '/'


class MultilingualSiteGenerator(Generator):
    """Generator for multilingual site functionality"""
    
    def __init__(self, context, settings, path, theme, output_path):
        super().__init__(context, settings, path, theme, output_path)
        
        # Check if multilingual is enabled
        if not settings.get('MULTILINGUAL_ENABLED', False):
            logger.info("Multilingual site is disabled")
            return
        
        self.content_processor = MultilingualContentProcessor(settings)
        self.language_switcher = LanguageSwitcher(settings.get('MULTILINGUAL_LANGUAGES', ['en', 'de', 'fr']))
        
        logger.info(f"Multilingual site generator initialized for languages: {self.content_processor.supported_langs}")
    
    def generate_context(self):
        """Generate context for multilingual site"""
        if not self.settings.get('MULTILINGUAL_ENABLED', False):
            return
        
        # Add language switcher to context
        self.context['language_switcher'] = self.language_switcher
        self.context['multilingual_languages'] = self.content_processor.supported_langs
        self.context['default_language'] = self.content_processor.default_lang
    
    def generate_output(self, writer):
        """Generate multilingual site output"""
        if not self.settings.get('MULTILINGUAL_ENABLED', False):
            return
        
        logger.info("Starting multilingual site generation")
        
        # Process articles
        articles = self.context.get('articles', [])
        processed_articles = self.content_processor.process_articles(articles)
        
        # Process pages
        pages = self.context.get('pages', [])
        processed_pages = self.content_processor.process_pages(pages)
        
        # Generate language-specific versions
        for lang in self.content_processor.supported_langs:
            self._generate_language_version(writer, lang, processed_articles[lang], processed_pages[lang])
        
        # Generate language selection page
        self._generate_language_selection_page(writer)
        
        logger.info("Multilingual site generation completed")
    
    def _generate_language_version(self, writer, lang: str, articles: List[Article], pages: List[Page]):
        """Generate content for a specific language"""
        logger.info(f"Generating content for language: {lang}")
        
        # Update context for this language
        lang_context = self.context.copy()
        lang_context['articles'] = articles
        lang_context['pages'] = pages
        lang_context['LANG'] = lang
        lang_context['current_language'] = lang
        
        # Generate articles for this language
        for article in articles:
            writer.write_file(
                article.save_as,
                self.get_template('article'),
                lang_context,
                article=article,
                category=getattr(article, 'category', None),
                override_output=self.output_path
            )
        
        # Generate pages for this language
        for page in pages:
            writer.write_file(
                page.save_as,
                self.get_template('page'),
                lang_context,
                page=page,
                override_output=self.output_path
            )
        
        # Generate language-specific index
        self._generate_language_index(writer, lang, articles, lang_context)
    
    def _generate_language_index(self, writer, lang: str, articles: List[Article], context: Dict):
        """Generate index page for a specific language"""
        index_save_as = f"{lang}/index.html"
        
        writer.write_file(
            index_save_as,
            self.get_template('index'),
            context,
            articles=articles,
            override_output=self.output_path
        )
    
    def _generate_language_selection_page(self, writer):
        """Generate root language selection page"""
        context = self.context.copy()
        context['supported_languages'] = self.content_processor.supported_langs
        context['language_names'] = self.language_switcher.lang_names
        
        writer.write_file(
            'index.html',
            self.get_template('language_selection'),
            context,
            override_output=self.output_path
        )


def get_generators(pelican_object):
    """Register the multilingual site generator"""
    # Disable the complex generator for now, just use the content enhancement
    return None


def enhance_content_with_multilingual_data(content_generator):
    """Enhance content objects with multilingual data"""
    settings = content_generator.settings
    
    if not settings.get('MULTILINGUAL_ENABLED', False):
        return
    
    supported_langs = settings.get('MULTILINGUAL_LANGUAGES', ['en', 'de', 'fr'])
    default_lang = settings.get('MULTILINGUAL_DEFAULT_LANG', 'en')
    
    logger.info(f"Enhancing content with multilingual data for languages: {supported_langs}")
    
    # Simple language switcher that generates basic links
    def generate_simple_language_links(content_url, current_lang):
        links = []
        for lang in supported_langs:
            if lang != current_lang:
                # Simple URL replacement - this is a basic implementation
                if content_url.startswith('/'):
                    lang_url = f"/{lang}{content_url}"
                else:
                    lang_url = f"/{lang}/{content_url}"
                links.append({
                    'code': lang,
                    'name': {
                        'en': 'English',
                        'de': 'Deutsch', 
                        'fr': 'Français',
                        'es': 'Español',
                        'it': 'Italiano'
                    }.get(lang, lang.upper()),
                    'url': lang_url
                })
        return links
    
    # Process articles
    if hasattr(content_generator, 'articles'):
        for article in content_generator.articles:
            try:
                article.multilingual_urls = {}
                article.language_links = generate_simple_language_links(
                    getattr(article, 'url', ''), default_lang
                )
                logger.debug(f"Enhanced article: {article.title}")
            except Exception as e:
                logger.warning(f"Failed to enhance article {getattr(article, 'title', 'unknown')} with multilingual data: {e}")
                article.multilingual_urls = {}
                article.language_links = []
    
    # Process pages
    if hasattr(content_generator, 'pages'):
        for page in content_generator.pages:
            try:
                page.multilingual_urls = {}
                page.language_links = generate_simple_language_links(
                    getattr(page, 'url', ''), default_lang
                )
                logger.debug(f"Enhanced page: {page.title}")
            except Exception as e:
                logger.warning(f"Failed to enhance page {getattr(page, 'title', 'unknown')} with multilingual data: {e}")
                page.multilingual_urls = {}
                page.language_links = []


def register():
    """Register plugin with Pelican"""
    signals.get_generators.connect(get_generators)
    signals.article_generator_finalized.connect(enhance_content_with_multilingual_data)
    signals.page_generator_finalized.connect(enhance_content_with_multilingual_data)