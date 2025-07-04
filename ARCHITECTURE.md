# Architecture Documentation

This document provides comprehensive technical architecture documentation for the grtnr.com project to help new engineers understand and contribute to the system.

[TOC]

## Overview

grtnr.com is a personal website/blog built as a static site using **Pelican** (Python static site generator) with a custom theme called "pelicanyan". The site implements digital garden concepts with WikiLinks navigation and supports multiple content types: articles, pages, and recipes.

## Technology Stack

### Core Technologies

- **Static Site Generator**: Pelican 4.11.0 (Python-based)
- **Language**: Python 3.12
- **Theme**: Custom "pelicanyan" theme (based on Lanyon/Poole)
- **Markdown**: Enhanced with TOC, WikiLinks, and code highlighting
- **Deployment**: GitHub Actions with dual-environment setup
- **Development**: Invoke task automation with livereload

### Dependencies

- **Python**: See `.devcontainer/requirements.txt` for complete list
- **Node.js**: For code quality tools (Prettier, markdownlint, jsonlint)
- **Development Environment**: VS Code with DevContainer support

## Content Architecture

### Content Organization

```text
content/
├── articles/           # Blog posts with date-prefixed directories
│   └── YYYY-MM-DD-slug/
│       ├── article.md
│       └── [images...]
├── pages/             # Static pages
│   └── slug/
│       ├── page.md
│       └── [assets...]
├── recipes/           # Recipe content with special processing
│   └── slug/
│       ├── recipe.md
│       └── [images...]
├── static/           # Site-wide assets
│   ├── favicon files
│   ├── profile images
│   └── CSS/JS resources
└── tag_pages/        # Auto-generated tag pages
```

### Content Types

#### Articles

- **Location**: `content/articles/YYYY-MM-DD-slug/`
- **URL Pattern**: `/{slug}/` (date removed from URL)
- **Features**: Automatic title generation, date extraction, tag support
- **Template**: `article.html` with Giscus comments integration

#### Pages

- **Location**: `content/pages/slug/`
- **URL Pattern**: `/{slug}/`
- **Purpose**: Static content (about, impressum, todo)
- **Template**: `page.html`

#### Recipes

- **Location**: `content/recipes/slug/`
- **URL Pattern**: `/recipes/{slug}/`
- **Features**: Custom content type with structured data
- **Templates**: `recipe.html` for individual, `recipes_index.html` for listing

### URL Generation & Slug Normalization

All content types use centralized slug normalization:

- German characters: `ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`
- Consistent URL generation across articles, pages, recipes, and WikiLinks
- Date prefixes removed from article URLs for clean permalinks

## Plugin System Architecture

### Plugin Execution Order

Plugins execute in a specific order to ensure proper content processing:

```python
PLUGINS = [
    "auto_title",              # 1. Generate titles from directory names
    "recipes",                 # 2. Process recipe content type
    "set_proper_category",     # 3. Set categories from directory structure
    "filter_articles_for_index", # 4. Filter articles for index page
    "copy_adjacent_images",    # 5. Copy images and fix URLs
    "excerpt_to_summary",      # 6. Generate article summaries
    "external_links",          # 7. Process external link attributes
]
```

### Core Plugins

#### auto_title.py

- **Purpose**: Automatically generates article titles from directory names
- **Function**: Removes date prefixes, converts hyphens to spaces, capitalizes
- **Signal**: `content_object_init`

#### recipes.py

- **Purpose**: Creates recipe content type with custom URL structure
- **Pattern**: Content Adapter pattern with `RecipeAdapter` class
- **Features**: Custom URL generation, dedicated templates
- **Signal**: `get_generators`

#### copy_adjacent_images.py

- **Purpose**: Automatically copies images from content directories to output
- **Function**: Fixes relative URLs in content, maintains directory structure
- **Signal**: `finalized`

#### normalize_slugs.py

- **Purpose**: Centralized German character transliteration
- **Function**: Provides `normalize_slug()` used across plugins
- **Usage**: Articles, recipes, WikiLinks, tag pages

#### markdown_wikilinks.py

- **Purpose**: Implements `[[WikiLink]]` syntax for digital garden navigation
- **Features**:
  - Syntax: `[[Page Name]]` or `[[Page Name|Display Text]]`
  - Automatic slug conversion with German character support
  - High priority (175) execution before other markdown processing
- **Signal**: Markdown extension registration

#### set_proper_category.py

- **Purpose**: Sets article categories based on directory structure
- **Function**: Uses directory path instead of folder names for categorization
- **Signal**: `content_object_init`

### Plugin Development Patterns

#### Signal-Based Architecture

- Uses Pelican's signal system for plugin coordination
- Multiple signal connection points: `init`, `content_object_init`, `finalized`
- Proper execution order management through plugin sequence

#### Content Adaptation Pattern

- `RecipeAdapter` class for custom content types
- Consistent interface with articles/pages
- Template integration through adapter pattern

## Logging System

### Centralized Logging Configuration

The project uses a centralized logging system with colored output and standardized formatting:

**Key Features:**

- **Colored Output**: Different colors for each log level (INFO=green, WARNING=yellow, ERROR=red, etc.)
- **Standardized Format**: `YYYY-MM-DD HH:MM LEVEL    Message`
- **Exception Handling**: Automatic stack trace logging with `exc_info=True`
- **Multiple Loggers**: Plugin-specific loggers for better organization

### Usage in Plugins

```python
import os
import sys

# Import centralized logging
sys.path.insert(0, os.path.dirname(__file__))
from logger_config import get_logger

# Setup logger for plugin
logger = get_logger('plugin_name')

# Use logging throughout plugin
logger.info("Plugin initialized")
logger.debug("Processing content")
logger.warning("Configuration issue detected")
logger.error("Failed to process file", exc_info=True)
```

### Log Levels

- **DEBUG**: Detailed diagnostic information (hidden by default)
- **INFO**: General operational messages (green)
- **WARNING**: Warning messages for potential issues (yellow)
- **ERROR**: Error messages for failures (red)
- **CRITICAL**: Critical failures that may stop execution (magenta)

### Configuration

Logging is initialized in `pelicanconf.py` with INFO level by default:

```python
from logger_config import setup_pelican_logging
setup_pelican_logging('INFO')  # Change to 'DEBUG' for verbose output
```

## Theme Architecture (pelicanyan)

### Template Hierarchy

```text
pelicanyan/templates/
├── base.html              # Core layout with sidebar, analytics
├── index.html             # Homepage with article pagination
├── article.html           # Individual blog posts
├── recipe.html            # Structured recipe display
├── recipes_index.html     # Recipe listing page
├── page.html              # Static pages
├── sidebar.html           # Navigation and metadata
├── tag.html               # Tag-specific pages
├── tags.html              # All tags overview
└── [pagination, archives, etc.]
```

### CSS Architecture

```text
pelicanyan/static/css/
├── poole.css              # Base typography and layout
├── lanyon.css             # Sidebar navigation and responsive design
├── syntax.css             # Code syntax highlighting
├── tag_pills.css          # Tag styling components
└── styles.css             # Custom site-specific styles
```

### JavaScript Components

```text
pelicanyan/static/js/
└── giscus-comments.js     # Comment system integration
```

### Theme Features

- **Responsive Design**: Mobile-first approach with sidebar navigation
- **Syntax Highlighting**: Code blocks with proper styling
- **Comment System**: Giscus integration for article comments
- **Analytics**: Google Analytics 4 integration
- **Social Links**: GitHub, LinkedIn, X (Twitter) integration

## Digital Garden Features

### WikiLinks Implementation

- **Syntax**: `[[Page Name]]` links to `/page-name/`
- **Display Text**: `[[Page Name|Custom Text]]` shows "Custom Text"
- **Processing**: Markdown preprocessor with high priority (175)
- **Slug Conversion**: Uses centralized `normalize_slug()` function
- **Cross-Content**: Links work across articles, pages, and recipes

### Navigation Patterns

- **Interconnected Content**: WikiLinks create web of connections
- **Tag System**: Automatic tag page generation
- **Sidebar Navigation**: Context-aware navigation in sidebar
- **Breadcrumbs**: Category and date-based navigation

## Build & Development Pipeline

### Development Workflow

```bash
# Primary commands
inv livereload    # Development server with auto-reload (recommended)
inv build         # Build local version
inv serve         # Static file server at localhost:8000
inv preview       # Production build for testing
inv clean         # Remove generated files

# Code quality
inv check-py      # Format and lint Python files
inv check-md      # Format and lint Markdown files
inv check-json    # Format and lint JSON files
```

### Development Features

- **Caching**: Development builds use `CACHE_CONTENT=true` for faster regeneration
- **Live Reload**: Watches templates, content, CSS, JS, and plugin files
- **Auto-formatting**: On-save formatting for Python, Markdown, and JSON
- **VS Code Integration**: DevContainer with pre-configured extensions

### Configuration Files

#### pelicanconf.py (Development)

- Base configuration for development builds
- Plugin configuration and execution order
- Markdown extension setup
- Theme and content paths

#### publishconf.py (Production)

- Production-specific overrides
- Analytics and comment system enablement
- Performance optimizations
- Sitename configuration based on environment

#### tasks.py (Invoke Tasks)

- Development workflow automation
- Code quality task automation
- Build and deployment helpers
- File watching and live reload setup

## Deployment Architecture

### Dual Environment Setup

#### Production Environment

- **Trigger**: Commits to `main` branch
- **Domain**: grtnr.com
- **Repository**: tillg/grtnr.com (external)
- **Configuration**: Full analytics and comments enabled

#### Staging Environment

- **Trigger**: Feature branch commits
- **Domain**: test.grtnr.com
- **Repository**: tillg/test.grtnr.com (external)
- **Configuration**: Test environment settings

### GitHub Actions Pipeline

```yaml
# .github/workflows/build-and-deploy.yml
Steps:
1. Checkout source code
2. Setup Python 3.12 environment
3. Install dependencies from requirements.txt
4. Run production build (inv preview)
5. Deploy to appropriate external repository
6. Configure CNAME for custom domain
```

### Deployment Features

- **Environment Variables**: `PELICAN_SITENAME` set based on branch
- **External Repository Pattern**: Source code separate from hosting
- **Automatic CNAME**: Custom domain configuration
- **Build Artifacts**: Static files only in hosting repositories

## Content Processing Flow

### Initialization Phase

1. Load configuration (pelicanconf.py)
2. Register plugins in execution order
3. Configure Markdown extensions
4. Setup theme and template paths

### Content Reading Phase

1. **auto_title**: Generate titles from directory names
2. **recipes**: Identify and process recipe content
3. **set_proper_category**: Assign categories from paths
4. Metadata extraction and validation

### Content Processing Phase

1. **Markdown Processing**: Convert content with extensions
2. **WikiLink Processing**: Convert `[[links]]` to HTML
3. **Image Processing**: Copy adjacent images, fix URLs
4. **Summary Generation**: Create excerpts for articles

### Generation Phase

1. **Template Rendering**: Apply theme templates
2. **Pagination**: Generate paginated index pages
3. **Tag Pages**: Auto-generate tag-specific pages
4. **Static Files**: Copy theme assets and static content

### Finalization Phase

1. **URL Fixing**: Ensure consistent internal links
2. **External Link Processing**: Add target attributes
3. **Validation**: Check for broken references
4. **Output Organization**: Structure final static site

## Development Environment Setup

### Requirements

- Python 3.12 with virtual environment
- Node.js for development tools
- VS Code (recommended) with DevContainer support

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd grtnr.com_src

# 2. Setup Python environment
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r .devcontainer/requirements.txt
npm install

# 4. Start development
inv livereload
```

### Code Quality Setup

- **Python**: Black (88 char), isort, flake8
- **Markdown**: Prettier, markdownlint
- **JSON**: Prettier, jsonlint
- **VS Code**: Auto-format on save, real-time linting

### DevContainer Support

- Pre-configured development environment
- Automatic extension installation
- Consistent development setup across machines

## Extending the System

### Adding New Content Types

1. Create content adapter following `RecipeAdapter` pattern
2. Add to plugin system with appropriate signals
3. Create dedicated templates in theme
4. Update URL generation and slug normalization

### Creating New Plugins

1. Follow signal-based architecture
2. Use centralized `normalize_slug()` function
3. Use centralized logging system (`from logger_config import get_logger`)
4. Consider execution order dependencies
5. Add to `PLUGINS` list in proper sequence

### Theme Customization

1. Modify templates in `pelicanyan/templates/`
2. Update CSS in `pelicanyan/static/css/`
3. Test responsive design across devices
4. Maintain accessibility standards

### Deployment Customization

1. Modify GitHub Actions workflow
2. Update environment-specific configurations
3. Consider new hosting requirements
4. Test both staging and production environments

## Monitoring & Maintenance

### Analytics

- Google Analytics 4 integration
- Comment system metrics via Giscus
- GitHub repository insights

### Performance

- Static site generation for optimal speed
- Image optimization through adjacent copying
- CSS minification in production builds
- Efficient plugin execution order

### Content Management

- Automated title generation reduces manual work
- Image copying eliminates path management
- WikiLinks provide easy cross-referencing
- Tag system enables content organization

## Translation Service Architecture

### Overview

The translation service provides AI-powered automatic translation of content into multiple languages using OpenAI's GPT API. It's designed as a standalone, independently testable service that integrates with the Pelican plugin system.

### Architecture Principles

- **Service Independence**: Complete decoupling from Pelican internals
- **API-First Design**: Clear interface contract for translation operations
- **Test-Driven Development**: Comprehensive testing with sample content
- **Secure Key Management**: Environment-based API key handling
- **Caching Strategy**: Hash-based caching to avoid redundant translations

### Core Components

#### TranslationService Class

```python
class TranslationService:
    """Main translation service interface"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize with OpenAI API configuration"""
        
    def translate_content(self, content: str, source_lang: str, target_lang: str) -> str:
        """Translate markdown content while preserving structure"""
        
    def detect_language(self, content: str) -> str:
        """Detect source language of content"""
        
    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
```

#### Translation Cache

```python
class TranslationCache:
    """Content hash-based caching system"""
    
    def __init__(self, cache_dir: str):
        """Initialize cache directory"""
        
    def get_cached_translation(self, content_hash: str, target_lang: str) -> Optional[str]:
        """Retrieve cached translation if available"""
        
    def cache_translation(self, content_hash: str, target_lang: str, translation: str):
        """Store translation in cache"""
        
    def invalidate_cache(self, content_hash: str):
        """Remove cached translations for specific content"""
```

#### Configuration Management

```python
class TranslationConfig:
    """Configuration management for translation service"""
    
    api_key: str                    # OpenAI API key from environment
    model: str                      # GPT model (default: gpt-4)
    target_languages: List[str]     # Target language codes
    exclude_categories: List[str]   # Categories to skip
    exclude_paths: List[str]        # Paths to skip
    cache_enabled: bool             # Enable caching (default: True)
    max_retries: int               # API retry attempts (default: 3)
    timeout: int                   # Request timeout in seconds (default: 30)
```

### Integration Architecture

#### Plugin Integration

The translation service integrates with Pelican through the `automatic_translation` plugin:

```python
# plugins/automatic_translation.py
from translation_service import TranslationService, TranslationConfig

def translate_content(generators):
    """Pelican plugin entry point"""
    config = TranslationConfig.from_pelican_settings(generators[0].settings)
    service = TranslationService(config)
    
    for generator in generators:
        for article in generator.articles:
            service.process_article(article)
```

#### File Organization

```text
extensions/
├── translation_service/
│   ├── __init__.py
│   ├── service.py              # Core TranslationService
│   ├── cache.py                # TranslationCache implementation
│   ├── config.py               # Configuration management
│   ├── prompts.py              # Translation prompts
│   └── exceptions.py           # Custom exceptions
├── tests/
│   ├── test_translation_service.py
│   ├── test_cache.py
│   ├── test_config.py
│   └── fixtures/
│       ├── sample_article.md
│       ├── sample_recipe.md
│       └── expected_translations/
└── plugins/
    └── automatic_translation.py   # Pelican plugin
```

### Translation Process Flow

#### 1. Content Discovery

1. Plugin scans all articles/pages during generation
2. Filters content based on configuration (excluded categories/paths)
3. Detects source language of each piece of content
4. Determines target languages for translation

#### 2. Cache Check

1. Generates content hash (SHA-256 of markdown content)
2. Checks cache for existing translations
3. Skips translation if cached version exists and is current
4. Proceeds to translation if cache miss or content changed

#### 3. Translation Execution

1. Constructs translation prompt with context
2. Sends request to OpenAI API with retry logic
3. Validates response structure and content
4. Caches successful translation with metadata

#### 4. File Management

1. Creates `extensions/` directory structure
2. Writes translated content with proper metadata
3. Maintains original file structure and naming
4. Updates cache with new translation hash

### Translation Prompt Engineering

#### Core Prompt Structure

```text
You are a professional translator specializing in technical content and markdown documents.

TASK: Translate the following markdown content from {source_lang} to {target_lang}.

REQUIREMENTS:
1. Preserve ALL markdown formatting (headers, links, code blocks, lists, etc.)
2. Maintain WikiLinks syntax: [[Page Name]] -> [[Translated Page Name]]
3. Keep code blocks and technical terms untranslated unless they are comments
4. Translate alt text in images: ![description](image.jpg) -> ![translated description](image.jpg)
5. Preserve metadata sections (front matter) untranslated
6. Maintain the tone and style appropriate for technical/blog content
7. Use native language conventions for the target language

CONTENT:
{content}

TRANSLATION:
```

#### Language-Specific Adaptations

- **German**: Formal vs. informal tone detection
- **French**: Proper accent handling and Canadian vs. European variations
- **Spanish**: Regional variations and technical term handling
- **Italian**: Formal register for technical content

### API Key Management

#### Environment Variables

Configuration can be provided via environment variables or `.env` files:

```bash
# .env file (recommended for development)
OPENAI_API_KEY=sk-...

# Optional configuration
TRANSLATION_MODEL=gpt-4           # Default model
TRANSLATION_CACHE_DIR=./cache     # Cache directory
TRANSLATION_MAX_RETRIES=3         # API retry attempts
TRANSLATION_TIMEOUT=30            # Request timeout
TRANSLATION_TARGET_LANGUAGES=de,fr,es  # Comma-separated language codes
TRANSLATION_EXCLUDE_CATEGORIES=recipes,drafts  # Categories to skip
TRANSLATION_EXCLUDE_PATHS=/pages/impressum/,/admin/  # Paths to skip
TRANSLATION_CACHE_ENABLED=true    # Enable caching
TRANSLATION_AUTO_DETECT=true      # Auto-detect source language
```

#### .env File Support

The translation service uses `python-dotenv` to automatically load configuration from `.env` files:

```python
# Automatic .env loading
from dotenv import load_dotenv
load_dotenv()  # Loads .env from current directory or parent directories

# Configuration priority (highest to lowest):
# 1. Environment variables
# 2. .env file in current directory
# 3. .env file in parent directories
# 4. Default values
```

#### Security Considerations

- API keys stored in environment variables or `.env` files only
- `.env` files should be added to `.gitignore`
- No hardcoded secrets in source code
- Cache files contain no sensitive information
- Secure handling of API responses
- Support for multiple `.env` files (development, staging, production)

### Testing Strategy

#### Unit Tests

```python
class TestTranslationService:
    def test_translate_simple_content(self):
        """Test basic translation functionality"""
        
    def test_preserve_markdown_structure(self):
        """Test that markdown formatting is preserved"""
        
    def test_handle_wikilinks(self):
        """Test WikiLinks translation"""
        
    def test_cache_functionality(self):
        """Test caching behavior"""
        
    def test_error_handling(self):
        """Test API error scenarios"""
```

#### Integration Tests

```python
class TestTranslationIntegration:
    def test_full_article_translation(self):
        """Test complete article translation workflow"""
        
    def test_pelican_plugin_integration(self):
        """Test plugin integration with Pelican"""
        
    def test_file_output_structure(self):
        """Test correct file generation"""
```

#### Manual Testing Framework

```python
class TranslationTestRunner:
    """Manual testing framework for translation quality"""
    
    def run_sample_translations(self):
        """Translate sample content for human review"""
        
    def generate_comparison_report(self):
        """Generate side-by-side comparison for review"""
        
    def validate_translation_quality(self):
        """Run automated quality checks"""
```

### Performance Considerations

#### API Rate Limiting

- Implement exponential backoff for retries
- Batch requests when possible
- Monitor API usage quotas
- Graceful degradation on rate limits

#### Caching Strategy

- Content-based hashing for cache keys
- Separate cache per target language
- Cache invalidation on content changes
- Configurable cache TTL

#### Memory Management

- Stream processing for large content
- Lazy loading of translations
- Cleanup of temporary files
- Memory-efficient caching

### Error Handling

#### API Errors

```python
class TranslationError(Exception):
    """Base exception for translation errors"""

class APIError(TranslationError):
    """OpenAI API communication errors"""

class RateLimitError(TranslationError):
    """API rate limiting errors"""

class InvalidResponseError(TranslationError):
    """Invalid API response format"""

class LanguageNotSupportedError(TranslationError):
    """Unsupported language codes"""
```

#### Graceful Degradation

- Continue site generation if translation fails
- Log errors without stopping build process
- Provide fallback behavior for missing translations
- Clear error messages for debugging

### Monitoring and Logging

#### Metrics Collection

- Translation request counts
- API response times
- Cache hit/miss ratios
- Error rates by type
- Language pair success rates

#### Logging Strategy

```python
logger = get_logger('translation_service')

logger.info(f"Translating {len(articles)} articles to {target_lang}")
logger.debug(f"Cache hit for {content_hash}")
logger.warning(f"API rate limit reached, retrying in {delay}s")
logger.error(f"Translation failed: {error}", exc_info=True)
```

### Future Enhancements

#### Advanced Features

- Batch translation for improved efficiency
- Translation quality scoring
- Custom terminology dictionaries
- Multi-model fallback strategy
- Real-time translation updates

#### Integration Improvements

- CLI commands for translation management
- Web interface for translation review
- Integration with translation management systems
- Automated quality assessment

This architecture supports a modern digital garden workflow with strong content organization, automated processing, and dual-environment deployment while maintaining the flexibility and performance of a static site generator.
