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

This architecture supports a modern digital garden workflow with strong content organization, automated processing, and dual-environment deployment while maintaining the flexibility and performance of a static site generator.
