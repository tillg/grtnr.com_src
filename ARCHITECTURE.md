# Architecture Documentation

This document provides comprehensive technical architecture documentation for the grtnr.com project organized in learning order to help new engineers understand and contribute to the system.

[TOC]

## 1. Project Overview - The Big Picture

grtnr.com is a personal blog/website built with **Pelican** (Python static site generator) that transforms Markdown files into fast, secure static HTML pages. Think of it as a sophisticated content management system that generates websites without requiring databases or server-side code when visitors browse.

**Key Features:**
- **Digital Garden Navigation**: WikiLinks (`[[Page Name]]`) for interconnected content
- **Multi-Content Support**: Articles, pages, and recipes with specialized templates
- **Automatic Translation**: AI-powered translations in multiple languages
- **Adjacent Image Handling**: Automatic image copying and URL fixing
- **Code Quality**: Comprehensive linting and formatting pipeline

## 2. Static Site Generation Architecture

### Core Concept
The fundamental pattern is: **Content (Markdown) + Templates (HTML/Jinja2) + Configuration → Static HTML files**

This approach provides:
- **Security**: No database or server-side vulnerabilities
- **Performance**: Pre-generated HTML serves instantly
- **Reliability**: Simple hosting without complex infrastructure
- **Scalability**: CDN-friendly static files

### Technology Stack
- **Static Site Generator**: Pelican 4.11.0 (Python-based)
- **Language**: Python 3.12
- **Theme**: Custom "pelicanyan" theme (based on Lanyon/Poole)
- **Markdown**: Enhanced with TOC, WikiLinks, and syntax highlighting
- **Deployment**: GitHub Actions with dual-environment setup
- **Development**: Invoke task automation with livereload

### Dependencies
- **Python**: Complete list in `.devcontainer/requirements.txt`
- **Node.js**: Code quality tools (Prettier, markdownlint, jsonlint)
- **Development**: VS Code with DevContainer support

## 3. Project Structure - How It's Organized

### Main Directory Layout
```text
grtnr.com_src/
├── content/              # All website content (articles, pages, recipes)
├── plugins/              # 14 custom Python plugins extending Pelican
├── pelicanyan/           # Custom theme (templates, CSS, JS)
├── extensions/           # Translation service and tests
├── cache/                # Build caches for performance
├── output/               # Generated static site files
├── .github/workflows/    # GitHub Actions deployment
├── tests/                # Test suites
└── .devcontainer/        # Development environment config
```

### Key Configuration Files
- **pelicanconf.py**: Main Pelican configuration (218 lines)
- **tasks.py**: Invoke task automation (309 lines)
- **pyproject.toml**: Python tool configuration (Black, isort)
- **package.json**: Node.js dependencies for code quality

## 4. Content Types and Organization

### Content Structure
```text
content/
├── articles/           # Blog posts (50+ entries)
│   └── YYYY-MM-DD-slug/
│       ├── article.md
│       ├── [images...]
│       └── extensions/  # AI translations
├── pages/              # Static pages (about, contact, etc.)
│   └── slug/
│       ├── page.md
│       ├── [assets...]
│       └── extensions/  # AI translations
├── recipes/            # Cooking recipes (30+ entries)
│   └── slug/
│       ├── recipe.md
│       └── [images...]
├── static/             # Site-wide assets
│   ├── favicon files
│   ├── profile images
│   └── CSS/JS resources
└── tag_pages/          # Auto-generated tag pages
```

### Content Processing Rules
- **Articles**: Date-prefixed directories → clean URLs (date removed)
- **Pages**: Static content with simple slug URLs
- **Recipes**: Custom content type with structured data
- **Images**: Adjacent files automatically copied and URLs fixed
- **Translations**: AI-generated versions in `extensions/` subdirectories

## 5. Development Workflow - Build Process

### Primary Commands
```bash
# Development (recommended)
inv livereload    # Development server with auto-reload

# Building
inv build         # Build local version  
inv serve         # Static file server at localhost:8000
inv preview       # Production build for testing
inv clean         # Remove generated files

# Code Quality
inv check-py      # Format and lint Python files
inv check-md      # Format and lint Markdown files
inv check-json    # Format and lint JSON files
```

### Development Features
- **Live Reload**: Watches templates, content, CSS, JS, and plugin files
- **Caching**: Development builds use `CACHE_CONTENT=true` for speed
- **Auto-formatting**: On-save formatting for Python, Markdown, and JSON
- **VS Code Integration**: DevContainer with pre-configured extensions

### Setup Process
```bash
# 1. Clone and setup
git clone <repository-url>
cd grtnr.com_src

# 2. Python environment
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r .devcontainer/requirements.txt
npm install

# 4. Start development
inv livereload
```

## 6. Plugin System - The Secret Sauce

### Plugin Architecture
The system's power comes from **9 coordinated custom plugins** executing in specific order:

```python
PLUGINS = [
    "auto_title",              # 1. Generate titles from directory names
    "normalize_slugs",         # 2. German character normalization (ä→ae, ß→ss)
    "recipes",                 # 3. Custom content type with RecipeAdapter
    "set_proper_category",     # 4. Category assignment from directory structure
    "filter_articles_for_index", # 5. Homepage article filtering
    "copy_adjacent_images",    # 6. Auto-copy images and fix relative URLs
    "excerpt_to_summary",      # 7. Summary generation for articles
    "external_links",          # 8. Add target="_blank" to external links
    "automatic_translation",   # 9. AI-powered translation with caching
]
```

### Key Plugin Patterns
- **Signal-Based Coordination**: Uses Pelican's signal system for plugin communication
- **Centralized Utilities**: `normalize_slug()` and logging shared across plugins
- **Content Adapter Pattern**: `RecipeAdapter` for custom content types
- **Execution Order**: Critical sequence for proper content processing

### Essential Plugins

#### auto_title.py
- **Purpose**: Generates titles from directory names
- **Function**: Removes date prefixes, converts hyphens to spaces, capitalizes
- **Example**: `2025-01-15-something-cool/` → "Something Cool"

#### copy_adjacent_images.py
- **Purpose**: Automatically handles image files
- **Function**: Copies images from content directories, fixes relative URLs
- **Benefit**: Eliminates manual image path management

#### recipes.py
- **Purpose**: Creates custom recipe content type
- **Pattern**: Content Adapter with dedicated templates
- **URL**: `/recipes/{slug}/` structure

#### normalize_slugs.py
- **Purpose**: Centralized German character handling
- **Function**: `ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`
- **Usage**: Used by articles, recipes, WikiLinks, tag pages

## 7. WikiLinks Feature - Digital Garden Navigation

### Implementation
**Dual processing approach** for robust WikiLink handling:

1. **markdown_wikilinks.py**: Markdown extension with high priority (175)
2. **wikilinks.py**: Pelican plugin for additional processing

### Syntax and Features
- **Basic**: `[[Page Name]]` → links to `/page-name/`
- **Custom Text**: `[[Page Name|Display Text]]` → shows "Display Text"
- **Cross-Content**: Works across articles, pages, and recipes
- **Normalization**: Uses centralized `normalize_slug()` for consistent URLs
- **German Support**: Handles character normalization automatically

### Benefits
- Creates interconnected navigation between content
- Enables digital garden-style content discovery
- Automatic slug conversion with proper character handling
- No manual URL management required

## 8. Theme and Templates - The Look and Feel

### pelicanyan Theme Structure
```text
pelicanyan/
├── templates/
│   ├── base.html              # Core layout with sidebar, analytics
│   ├── index.html             # Homepage with article pagination
│   ├── article.html           # Individual blog posts with comments
│   ├── recipe.html            # Structured recipe display
│   ├── recipes_index.html     # Recipe listing page
│   ├── page.html              # Static pages
│   ├── sidebar.html           # Navigation and metadata
│   ├── tag.html               # Tag-specific pages
│   └── tags.html              # All tags overview
├── static/
│   ├── css/
│   │   ├── poole.css          # Base typography and layout
│   │   ├── lanyon.css         # Sidebar navigation and responsive
│   │   ├── syntax.css         # Code syntax highlighting
│   │   ├── tag_pills.css      # Tag styling components
│   │   └── styles.css         # Custom site-specific styles
│   └── js/
│       └── giscus-comments.js # Comment system integration
```

### Theme Features
- **Responsive Design**: Mobile-first approach with sidebar navigation
- **Syntax Highlighting**: Code blocks with proper styling
- **Comment System**: Giscus integration for article comments
- **Analytics**: Google Analytics 4 integration
- **Social Links**: GitHub, LinkedIn, X (Twitter) integration

### Template Hierarchy
- **base.html**: Common layout for all pages
- **Content-specific**: Dedicated templates for articles, recipes, pages
- **Navigation**: Sidebar with context-aware elements
- **Responsive**: Mobile-optimized with collapsible sidebar

## 9. Automatic Translation System - Advanced Feature

### Overview
AI-powered translation system providing automatic multilingual content using OpenAI's GPT API.

### Architecture Components

#### TranslationService Class
```python
class TranslationService:
    def translate_content(self, content: str, source_lang: str, target_lang: str) -> str:
        """Translate markdown content while preserving structure"""
    
    def detect_language(self, content: str) -> str:
        """Detect source language of content"""
```

#### Key Features
- **Hash-based Caching**: Only re-translates when source content changes
- **File Organization**: Translations stored in `extensions/` directories
- **Markdown Preservation**: Maintains formatting, links, and structure
- **WikiLink Translation**: Translates `[[Page Name]]` appropriately

### File Structure
```text
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original content
└── extensions/
    ├── 2025-01-01-example-DE.md   # German translation
    ├── 2025-01-01-example-FR.md   # French translation
    └── 2025-01-01-example-ES.md   # Spanish translation
```

### Configuration
```python
# pelicanconf.py
TRANSLATION_ENABLED = True
TRANSLATION_TARGET_LANGUAGES = ["de", "fr", "es"]
TRANSLATION_EXCLUDE_CATEGORIES = ["recipes"]
TRANSLATION_EXCLUDE_PATHS = ["/pages/impressum/"]
```

### Translation Process
1. **Content Discovery**: Scans articles/pages during generation
2. **Cache Check**: Generates content hash, checks existing translations
3. **Translation**: Sends to OpenAI API with specialized prompts
4. **File Management**: Creates translation files with metadata
5. **Caching**: Stores results for future builds

## 10. Code Quality and Testing

### Code Quality Standards
- **Python**: Black formatting (88 char), isort imports, flake8 linting
- **Markdown**: Prettier formatting, markdownlint validation
- **JSON**: Prettier formatting, jsonlint validation
- **Line Length**: 88 characters for Python, W504 ignored

### Testing Framework
- **Translation Tests**: 22 comprehensive tests covering all functionality
- **Mock Implementations**: For development without API dependencies
- **Integration Tests**: Full workflow testing
- **Manual Testing**: Quality assurance framework

### Tool Configuration
- **pyproject.toml**: Python tool settings
- **package.json**: Node.js tool dependencies
- **VS Code**: Auto-format on save, real-time linting

## 11. Deployment Pipeline - Going Live

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
# .github/workflows/publish.yml
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

## 12. Content Processing Pipeline

### Execution Flow
The system processes content through these coordinated phases:

#### 1. Initialization Phase
- Load configuration (pelicanconf.py)
- Register plugins in execution order
- Configure Markdown extensions
- Setup theme and template paths

#### 2. Content Reading Phase
- **auto_title**: Generate titles from directory names
- **recipes**: Identify and process recipe content
- **set_proper_category**: Assign categories from paths
- **normalize_slugs**: Apply German character normalization

#### 3. Content Processing Phase
- **Markdown Processing**: Convert content with extensions
- **WikiLink Processing**: Convert `[[links]]` to HTML
- **Image Processing**: Copy adjacent images, fix URLs
- **Summary Generation**: Create excerpts for articles

#### 4. Generation Phase
- **Template Rendering**: Apply theme templates
- **Pagination**: Generate paginated index pages
- **Tag Pages**: Auto-generate tag-specific pages
- **Static Files**: Copy theme assets and static content

#### 5. Finalization Phase
- **URL Fixing**: Ensure consistent internal links
- **External Link Processing**: Add target attributes
- **Translation**: Generate multilingual versions
- **Output Organization**: Structure final static site

## 13. Advanced Features and Extensions

### Logging System
**Centralized logging with colored output:**
```python
from logger_config import get_logger
logger = get_logger('plugin_name')

logger.info("Plugin initialized")     # Green
logger.warning("Configuration issue") # Yellow
logger.error("Failed to process")     # Red
```

### Digital Garden Features
- **WikiLinks**: Create interconnected content web
- **Tag System**: Automatic tag page generation
- **Cross-references**: Automatic content linking
- **Navigation**: Context-aware sidebar navigation

### Performance Optimizations
- **Caching**: Development builds with content caching
- **Image Optimization**: Automatic adjacent image handling
- **CSS Minification**: Production build optimizations
- **Plugin Efficiency**: Optimized execution order

## 14. Development Guidelines

### Adding New Content Types
1. Create content adapter following `RecipeAdapter` pattern
2. Add to plugin system with appropriate signals
3. Create dedicated templates in theme
4. Update URL generation and slug normalization

### Creating New Plugins
1. Follow signal-based architecture
2. Use centralized `normalize_slug()` function
3. Implement centralized logging
4. Consider execution order dependencies
5. Add to `PLUGINS` list in proper sequence

### Theme Customization
1. Modify templates in `pelicanyan/templates/`
2. Update CSS in `pelicanyan/static/css/`
3. Test responsive design across devices
4. Maintain accessibility standards

### Content Guidelines
- Articles use date-prefixed directory structure
- German characters automatically normalized in URLs
- Tag pages auto-generated from content tags
- WikiLinks create interconnected navigation
- Images placed adjacent to content files

## 15. Monitoring and Maintenance

### Analytics
- Google Analytics 4 integration
- Comment system metrics via Giscus
- GitHub repository insights for development

### Performance Monitoring
- Static site generation for optimal speed
- Image optimization through adjacent copying
- CSS minification in production builds
- Efficient plugin execution order

### Content Management
- Automated title generation reduces manual work
- Image copying eliminates path management
- WikiLinks provide easy cross-referencing
- Tag system enables content organization
- Translation system maintains multilingual content

This architecture creates a powerful, maintainable static site that combines the simplicity of static generation with advanced features like automatic translation, digital garden navigation, and multiple content types. The modular plugin system allows for easy extension and customization while maintaining clean separation of concerns.