# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[TOC]

## Project Overview

This is a personal website/blog built with **garten**, a custom Python static site generator using a "pelicanyan" theme. The site supports multiple content types: articles, pages, and recipes with automatic image handling, multilingual support, and WikiLinks for digital garden-style navigation.

## Temporary Files

Screenshots and other temporary files should always be saved to the `tmp/` directory in the project root. This directory is gitignored.

## Development Commands

**Primary development workflow:**

- `inv livereload` - Development server with auto-reload (recommended)
- `inv build` - Build local version (includes link checking)
- `inv serve` - Static file server at localhost:8000
- `inv preview` - Production build for testing
- `inv clean` - Remove generated files

**Garten pipeline phases (for debugging):**

- `inv discover` - Phase 1: content discovery
- `inv process` - Phases 1-2: discover + process
- `inv assemble` - Phases 1-3: discover + process + assemble
- `inv render` - Phases 1-4: full pipeline without link checking

**Setup:**

1. Use Python 3.12 with virtual environment
1. Install dependencies: `pip install -r .devcontainer/requirements.txt`

**Code Quality:**

- `inv check-py` - Format and lint Python files
- `inv check-md` - Format and lint Markdown files
- `inv check-json` - Format and lint JSON files
- `inv check-links` - Validate all links in the generated site (requires `lychee`: `brew install lychee`)

**Link Validation:**

Link checking uses [`lychee`](https://github.com/lycheeverse/lychee) and is integrated at multiple levels:
- **Build Process**: Both `inv build` and `inv preview` include automatic link validation via lychee
- **Git Pre-commit Hook**: Prevents commits with broken links when content files are modified
- **GitHub Actions**: CI pipeline validates links as part of `inv build`
- **Production Check**: Daily scheduled workflow checks all links on the live site (grtnr.com)

Configuration is in `lychee.toml`. The system validates all links and ensures no broken images or references are deployed.

For detailed code quality standards and tool configurations, see [CODE_GUIDELINES.md](CODE_GUIDELINES.md).

## Architecture

For detailed system architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Pipeline Architecture

The site generator uses a phase-based pipeline with inspectable intermediate artifacts in `.build/`:

1. **Discover** (`garten/discover.py`) - Scan content directories, parse frontmatter, auto-title, assign categories, find translation files
2. **Process** (`garten/process.py`) - Markdown to HTML (with WikiLinks extension), copy adjacent images, generate summaries, external link processing, process translations
3. **Assemble** (`garten/assemble.py`) - Generate URLs, multilingual URL mapping, tag/category groupings, pagination, menu translations, language switcher data, article filtering
4. **Render** (`garten/render.py`) - Jinja2 template rendering for all content types, per-language pages, static file copying, image copying to language dirs

**Key architectural patterns:**
- **Phase-based pipeline** - Each phase is an independent Python module with inspectable intermediate artifacts
- **Centralized utilities** - `garten/utils.py` provides `normalize_slug()`, `get_logger()`, `localize_date()`
- **JSON configuration** - `site.json` with `GARTEN_` environment variable overrides
- **WikiLinks** - Custom markdown extension (`garten/markdown_wikilinks.py`) at priority 175

## WikiLinks Implementation

**Syntax:** `[[Page Name]]` or `[[Page Name|Display Text]]`

**Implementation:** `garten/markdown_wikilinks.py` - Markdown extension with high priority (175)

**Features:**
- Works across all content types (articles, pages, recipes)
- Uses centralized `normalize_slug()` for consistent URL generation
- Supports German character normalization

## Content Processing Pipeline

**Pipeline phases with sub-phases:**

1. **Discover** - Scan directories, parse frontmatter, auto-title from dir names, assign categories, find translation files
2. **Process** - Markdown rendering (WikiLinks, TOC, CodeHilite), image URL fixing, summary generation, external link processing, translation file processing
3. **Assemble** - URL generation, multilingual URLs, internal link prefixing, tag/category maps, pagination, menu translations, language switcher, article filtering
4. **Render** - Template rendering (articles, pages, recipes, indexes, tags), static files, image copying, root redirect page

## Configuration

Site configuration uses `site.json` with environment variable overrides:

- **`GARTEN_SITEURL`** - Override site URL (e.g., for staging)
- **`GARTEN_SITENAME`** - Override site name
- **`GARTEN_TRANSLATION__ENABLED`** - Enable/disable translation (double underscore for nested keys)

## Logging System

**Centralized logging with colored output:**
- `from garten.utils import get_logger`
- Format: `YYYY-MM-DD HH:MM LEVEL Message`
- Colors: INFO=green, WARNING=yellow, ERROR=red
- Use `logger.info()`, `logger.warning()`, `logger.error()`

## Deployment

GitHub Actions automated pipeline:

- **Main branch** → grtnr.com (production)
- **Feature branches** → test.grtnr.com (staging)
- Uses external repositories for hosting
- Environment variables: `GARTEN_SITENAME`, `GARTEN_TRANSLATION__ENABLED`

## Development Notes

- **WikiLinks**: Use `[[Page Name]]` syntax to link between content
- **Images**: Place images adjacent to content files - they're auto-copied and URLs fixed
- **Recipes**: Use recipe content type for cooking content with dedicated templates
- **Linting**: Flake8 with 88 character line length, W504 ignored

## Automatic Translation System

The site includes an AI-powered automatic translation system that creates translations of articles and pages in multiple languages.

**Features:**
- **Language Detection** - Automatically detects the source language of content
- **Hash-based Caching** - Only re-translates when source content changes
- **File Organization** - Stores translations in `extensions/` directories
- **Configuration** - Fully configurable target languages and exclusions

**File Structure:**
```text
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original content
└── extensions/
    ├── 2025-01-01-example-DE.md   # German translation
    ├── 2025-01-01-example-FR.md   # French translation
    └── 2025-01-01-example-ES.md   # Spanish translation
```

**Configuration (site.json):**
```json
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

**IMPORTANT: Never edit translation files in `extensions/` directories.** They are auto-generated at build time from the original content files. Only edit the original source `.md` file — translations will be regenerated automatically.

**Translation Files Include:**
- Source and target language metadata
- Creation timestamp and source file hash
- Full translated content with preserved formatting

**Management Commands:**

- `inv clean-translations` - Remove all translation files
- `inv clean-translations-cache` - Clear cache only (forces re-translation)

**Testing:**

- Run tests: `python -m pytest tests/ -q`
- 254+ tests covering all pipeline phases

## Writing a New Article

Each article lives in its own directory under `content/articles/` with a date-prefixed slug:

```text
content/articles/YYYY-MM-DD-slug/
├── YYYY-MM-DD-slug.md   # Article content (filename must match directory name)
└── hero.png             # Hero image (referenced in frontmatter)
```

**Required frontmatter fields:**

```yaml
---
date: YYYY-MM-DD
excerpt: One-sentence summary of the article
Tags: tag1, tag2
image: hero.png
---
```

- `date` — Publication date
- `excerpt` (or `summary`) — Short description shown in article listings
- `Tags` — Comma-separated list of tags (capitalized key)
- `image` — Hero/thumbnail image filename (file must exist in the article directory)

**Images:** Every article should have a hero image. If the user doesn't provide one, find a suitable image from the internet (e.g. a relevant icon, illustration, or logo — prefer SVG or PNG) and save it into the article's directory. Then reference it in the `image` frontmatter field.

**After creating an article**, run `inv render` to verify it builds without errors.

## Change Log

The site has a change log at `content/pages/changelog/changelog.md`. It is a human-readable timeline of user-visible changes, ordered oldest-first (newest at the bottom).

**When committing:** Review the change log and add an entry if the commit includes technical changes to the site (new features, visual changes, bug fixes that affect visitors). Do **not** add entries for new articles or content, internal refactors, CI tweaks, translation regeneration, or code-only changes.

**Format:** Group entries under `### YYYY-MM-DD` date headings. Multiple changes on the same day share one heading. Write entries as short, plain-language bullet points.

## Content Guidelines

- Articles use date-prefixed directory structure: `YYYY-MM-DD-slug/`
- German characters are automatically normalized in URLs
- Tag pages are auto-generated from content tags
- WikiLinks create interconnected navigation between content
