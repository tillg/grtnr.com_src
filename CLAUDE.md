# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

[TOC]

## Project Overview

This is a personal website/blog built with **Pelican** (Python static site generator) using a custom theme called "pelicanyan". The site supports multiple content types: articles, pages, and recipes with automatic image handling and WikiLinks for digital garden-style navigation.

## Development Commands

**Primary development workflow:**

- `inv livereload` - Development server with auto-reload (recommended)
- `inv build` - Build local version
- `inv serve` - Static file server at localhost:8000
- `inv preview` - Production build for testing
- `inv clean` - Remove generated files

**Setup:**

1. Use Python 3.12 with virtual environment
1. Install dependencies: `pip install -r .devcontainer/requirements.txt`

**Code Quality:**

- `inv check-py` - Format and lint Python files
- `inv check-md` - Format and lint Markdown files
- `inv check-json` - Format and lint JSON files

For detailed code quality standards and tool configurations, see [CODE_GUIDELINES.md](CODE_GUIDELINES.md).

## Architecture

For detailed system architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Plugin System Architecture

The system's power comes from **8 coordinated custom plugins** that execute in specific order:

1. **auto_title** - Generates titles from directory names (removes date prefixes)
2. **normalize_slugs** - German character normalization (ä→ae, ß→ss) used across all plugins
3. **recipes** - Custom content type with RecipeAdapter pattern
4. **set_proper_category** - Category assignment from directory structure
5. **filter_articles_for_index** - Homepage article filtering
6. **copy_adjacent_images** - Auto-copy images and fix relative URLs
7. **excerpt_to_summary** - Summary generation for articles
8. **external_links** - Add target="_blank" to external links

**Key architectural patterns:**
- **Signal-based coordination** - Uses Pelican's signal system for plugin communication
- **Centralized utilities** - `normalize_slug()` and logging used across plugins
- **Content Adapter pattern** - RecipeAdapter for custom content types
- **Dual WikiLinks implementation** - Both markdown extension and plugin for robust processing

## WikiLinks Implementation

**Syntax:** `[[Page Name]]` or `[[Page Name|Display Text]]`

**Dual processing:**
- `markdown_wikilinks.py` - Markdown extension with high priority (175)
- `wikilinks.py` - Pelican plugin for additional processing

**Features:**
- Works across all content types (articles, pages, recipes)
- Uses centralized `normalize_slug()` for consistent URL generation
- Supports German character normalization

## Content Processing Pipeline

**Execution order is critical:**

1. **Initialization** - Load config, register plugins, setup logging
2. **Content Reading** - auto_title, recipes, set_proper_category
3. **Processing** - Markdown with WikiLinks, image copying, summary generation
4. **Generation** - Template rendering, pagination, tag pages
5. **Finalization** - URL fixing, external link processing, validation

## Logging System

**Centralized logging with colored output:**
- `from logger_config import get_logger`
- Format: `YYYY-MM-DD HH:MM LEVEL Message`
- Colors: INFO=green, WARNING=yellow, ERROR=red
- Use `logger.info()`, `logger.warning()`, `logger.error()`

## Deployment

GitHub Actions automated pipeline:

- **Main branch** → grtnr.com (production)
- **Feature branches** → test.grtnr.com (staging)
- Uses external repositories for hosting

## Development Notes

- **WikiLinks**: Use `[[Page Name]]` syntax to link between content
- **Images**: Place images adjacent to content files - they're auto-copied and URLs fixed
- **Recipes**: Use recipe content type for cooking content with dedicated templates
- **Caching**: Development builds use caching for faster regeneration
- **Linting**: Flake8 with 88 character line length, W504 ignored

## Content Guidelines

- Articles use date-prefixed directory structure: `YYYY-MM-DD-slug/`
- German characters are automatically normalized in URLs
- Tag pages are auto-generated from content tags
- WikiLinks create interconnected navigation between content
