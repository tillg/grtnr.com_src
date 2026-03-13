# Architecture Documentation

This document provides comprehensive technical architecture documentation for the grtnr.com project organized in learning order to help new engineers understand and contribute to the system.

[TOC]

## 1. Project Overview - The Big Picture

grtnr.com is a personal blog/website built with **garten**, a custom Python static site generator that transforms Markdown files into fast, secure static HTML pages. It uses Jinja2, Python-Markdown, and Pygments in an explicit, debuggable pipeline.

**Key Features:**
- **Digital Garden Navigation**: WikiLinks (`[[Page Name]]`) for interconnected content
- **Multi-Content Support**: Articles, pages, and recipes with specialized templates
- **Automatic Translation**: AI-powered translations in multiple languages
- **Multilingual Site**: Full en/de/fr site with language switcher
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
- **Static Site Generator**: garten (custom Python pipeline)
- **Language**: Python 3.12
- **Theme**: Custom "pelicanyan" theme (based on Lanyon/Poole)
- **Markdown**: Enhanced with TOC, WikiLinks, and syntax highlighting
- **Templates**: Jinja2 with direct rendering
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
├── garten/               # Site generator package (pipeline modules)
│   ├── __init__.py
│   ├── config.py         # Config loader (reads site.json + env overrides)
│   ├── discover.py       # Phase 1: content discovery
│   ├── process.py        # Phase 2: markdown → HTML
│   ├── assemble.py       # Phase 3: site structure + multilingual
│   ├── render.py         # Phase 4: template rendering
│   ├── models.py         # Content dataclasses
│   ├── markdown_wikilinks.py  # WikiLinks markdown extension
│   └── utils.py          # Slug normalization, logging, date localization
├── content/              # All website content (articles, pages, recipes)
├── extensions/           # Translation service package
│   └── translation_service/
├── theme/pelicanyan/           # Custom theme (templates, CSS, JS)
├── tests/                # Test suites (254+ tests)
├── output/               # Generated static site files
├── .build/               # Intermediate pipeline artifacts (gitignored)
├── .github/workflows/    # GitHub Actions deployment
└── .devcontainer/        # Development environment config
```

### Key Configuration Files
- **site.json**: Site configuration
- **tasks.py**: Invoke task automation
- **pyproject.toml**: Python tool configuration (Black, isort)
- **package.json**: Node.js dependencies for code quality
- **menu_translations.json**: Menu item translations (en/de/fr)
- **tag_translations.json**: Tag name translations

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
inv build         # Build local version (includes link checking)
inv serve         # Static file server at localhost:8000
inv preview       # Production build for testing
inv clean         # Remove generated files

# Pipeline phases (for debugging)
inv discover      # Phase 1: content discovery
inv process       # Phases 1-3: discover + process
inv assemble      # Phases 1-4: discover + process + assemble
inv render        # Phases 1-5: full pipeline without link checking

# Code Quality
inv check-py      # Format and lint Python files
inv check-md      # Format and lint Markdown files
inv check-json    # Format and lint JSON files
```

### Development Features
- **Live Reload**: Watches templates, content, CSS, JS, and garten source files
- **Pipeline Artifacts**: Intermediate results in `.build/` for debugging
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

## 6. Pipeline Architecture

### Phase-Based Pipeline

The garten pipeline processes content through 4 phases, each an independent Python module with inspectable intermediate artifacts in `.build/`:

#### Phase 1: Discover (`garten/discover.py`)
- Scan content directories for `.md` files
- Parse frontmatter (title, date, tags, excerpt, etc.)
- Auto-generate titles from directory names (removes date prefixes)
- Assign categories from directory structure
- Find translation files in `extensions/` subdirectories
- **Output**: `.build/discover/manifest.json`

#### Phase 2: Process (`garten/process.py`)

- Markdown → HTML with extensions (WikiLinks, TOC, CodeHilite, Extra, Meta)
- Copy adjacent images and fix relative URLs in HTML
- Generate summaries from excerpt metadata
- External link processing (add `target="_blank"`, `rel="noopener noreferrer"`)
- Process translation files through the same pipeline
- Apply typogrify (smart quotes, proper dashes)
- **Output**: `.build/process/manifest.json` + `html/` fragments

#### Phase 3: Assemble (`garten/assemble.py`)

- Generate URLs for all content (`{slug}/`, `recipes/{slug}/`)
- Generate multilingual URLs (`/{lang}/{slug}/`)
- Prefix internal links with language codes for non-default-language content
- Build tag and category groupings per language
- Build pagination per language
- Build translated menu and language switcher data
- Filter articles for index pages
- **Output**: `.build/assemble/site.json`

#### Phase 4: Render (`garten/render.py`)
- Render articles, pages, recipes via Jinja2 templates
- Render paginated index pages per language
- Render tag and category pages per language
- Render sitemap.xml, robots.txt, humans.txt
- Render root redirect page (auto-detects browser language)
- Copy static assets (theme files, content static)
- Copy images to language directories
- **Output**: `output/` directory (final site)

### Key Patterns
- **Centralized utilities** in `garten/utils.py`: `normalize_slug()`, `slugify()`, `get_logger()`, `localize_date()`, `remove_all_translations()`
- **WikiLinks** as a Markdown extension (`garten/markdown_wikilinks.py`) at priority 175
- **Content Adapter pattern**: Wrapper classes (`ArticleWrapper`, `PageWrapper`, `RecipeWrapper`) bridge data dicts to template variable names

## 7. WikiLinks Feature - Digital Garden Navigation

### Implementation
**Markdown extension** (`garten/markdown_wikilinks.py`) processes WikiLinks during Markdown rendering at priority 175.

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
theme/pelicanyan/
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
```json
// site.json
{
  "translation": {
    "enabled": false,
    "target_languages": ["de", "fr"],
    "exclude_categories": ["recipes"],
    "exclude_paths": ["/pages/impressum/"]
  }
}
```

Environment override: `GARTEN_TRANSLATION__ENABLED=true`

### Translation Process
1. **Content Discovery**: Scans articles/pages during discover phase
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
- **254+ tests** covering all pipeline phases
- **Phase-isolated tests**: Each phase testable independently
- **Integration tests**: Full pipeline testing on real content
- **Spot checks**: Verify specific content rendering details
- Run tests: `python -m pytest tests/ -q`

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
4. Configure translation service
5. Run build (inv build - includes link checking)
6. Deploy to appropriate external repository
7. Configure CNAME for custom domain
```

### Deployment Features
- **Environment Variables**: `GARTEN_SITENAME` set based on branch
- **External Repository Pattern**: Source code separate from hosting
- **Automatic CNAME**: Custom domain configuration
- **Build Artifacts**: Static files only in hosting repositories
- **Translation Caching**: GitHub Actions cache for translation files

## 12. Configuration System

### site.json
The primary configuration file. Static settings live in JSON; dynamic/environment-specific values use `GARTEN_` prefixed environment variables.

**Layering (highest priority wins):**
1. Environment variables with `GARTEN_` prefix (e.g., `GARTEN_SITEURL=https://test.grtnr.com`)
2. `site.json` values

**Runtime values** like `BUILD_TIME` are computed by the config loader at startup.

**Nested key override**: Use double underscores for nested keys: `GARTEN_TRANSLATION__ENABLED=true` maps to `translation.enabled`.

### Translation Configuration Files
- **menu_translations.json**: Menu item translations (en/de/fr)
- **tag_translations.json**: Tag name translations

## 13. Advanced Features and Extensions

### Logging System
**Centralized logging with colored output:**
```python
from garten.utils import get_logger
logger = get_logger('module_name')

logger.info("Processing started")       # Green
logger.warning("Configuration issue")   # Yellow
logger.error("Failed to process")       # Red
```

### Digital Garden Features
- **WikiLinks**: Create interconnected content web
- **Tag System**: Automatic tag page generation per language
- **Cross-references**: Automatic content linking
- **Navigation**: Context-aware sidebar navigation

### Multilingual Features
- **Language-prefixed URLs**: `/de/slug/`, `/fr/slug/`
- **Root redirect**: Auto-detects browser language
- **Language switcher**: Globe button in sidebar
- **Per-language pagination**: Independent article counts per language
- **hreflang tags**: SEO-friendly alternate language links

## 14. Development Guidelines

### Adding New Content Types
1. Add dataclass fields in `garten/models.py`
2. Extend discovery in `garten/discover.py`
3. Add processing logic in `garten/process.py`
4. Generate URLs in `garten/assemble.py`
5. Create Jinja2 templates and render in `garten/render.py`

### Modifying the Pipeline
1. Each phase is an independent module — modify in isolation
2. Run phase-specific tasks (`inv discover`, `inv process`, etc.) for testing
3. Inspect intermediate artifacts in `.build/` for debugging
4. Use centralized `get_logger()` for consistent logging
5. Add tests in `tests/test_<phase>.py`

### Theme Customization
1. Modify templates in `theme/pelicanyan/templates/`
2. Update CSS in `theme/pelicanyan/static/css/`
3. Test responsive design across devices
4. Maintain accessibility standards

### Content Guidelines
- Articles use date-prefixed directory structure
- German characters automatically normalized in URLs
- Tag pages auto-generated from content tags
- WikiLinks create interconnected navigation
- Images placed adjacent to content files

This architecture creates a powerful, maintainable static site that combines the simplicity of static generation with advanced features like automatic translation, digital garden navigation, and multiple content types. The phase-based pipeline provides transparency and debuggability while maintaining clean separation of concerns.
