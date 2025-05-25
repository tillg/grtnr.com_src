"""
Plugin to normalize slugs for all content types to ensure consistent URL generation.
This plugin processes articles and pages to apply consistent character transliteration.
"""

from pelican import signals
import unicodedata
import re


def normalize_slug(text):
    """
    Normalize text for use in URLs and file paths.
    This function provides centralized character transliteration 
    for consistent URL/path generation across the entire site.
    """
    if not text:
        return text
    
    # Common German character mappings
    char_map = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'
    }
    
    # Apply character mappings
    for char, replacement in char_map.items():
        text = text.replace(char, replacement)
    
    # Remove or replace other non-ASCII characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convert to lowercase and remove spaces/special chars (no hyphens for simple cases)
    text = text.lower()
    # Remove spaces entirely for compound words (linzer torte → linzertorte)
    text = text.replace(' ', '')
    # Remove other special characters except existing hyphens and underscores
    text = re.sub(r'[^a-zA-Z0-9\-_]', '', text)
    # Clean up multiple consecutive hyphens and leading/trailing hyphens
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    
    return text


def normalize_content_slugs(generator):
    """
    Normalize slugs for all articles and pages to ensure consistent URLs.
    This runs after content is processed but before URL generation.
    """
    # Process articles if they exist (but skip recipe files)
    if hasattr(generator, 'articles'):
        for article in generator.articles:
            if hasattr(article, 'slug') and article.slug:
                # Skip recipe files - they're handled by the recipes plugin
                if hasattr(article, 'source_path') and '/recipes/' in article.source_path:
                    continue
                article.slug = normalize_slug(article.slug)
    
    # Process hidden articles if they exist (but skip recipe files)
    if hasattr(generator, 'hidden_articles'):
        for article in generator.hidden_articles:
            if hasattr(article, 'slug') and article.slug:
                # Skip recipe files - they're handled by the recipes plugin
                if hasattr(article, 'source_path') and '/recipes/' in article.source_path:
                    continue
                article.slug = normalize_slug(article.slug)
    
    # Process pages if they exist
    if hasattr(generator, 'pages'):
        for page in generator.pages:
            if hasattr(page, 'slug') and page.slug:
                page.slug = normalize_slug(page.slug)
    
    # Process hidden pages if they exist
    if hasattr(generator, 'hidden_pages'):
        for page in generator.hidden_pages:
            if hasattr(page, 'slug') and page.slug:
                page.slug = normalize_slug(page.slug)


def register():
    """Register the plugin."""
    # Connect to generator_finalized to ensure all content is processed
    signals.article_generator_finalized.connect(normalize_content_slugs)
    signals.page_generator_finalized.connect(normalize_content_slugs)