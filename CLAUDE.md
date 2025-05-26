# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

**Python Code Quality:**

- `inv format-py` - Format with Black + organize imports with isort (88 char line length)
- `inv lint-py` - Run flake8 linting 
- `inv check-py` - Format then lint (complete workflow)

For detailed code quality standards and tool configurations, see [CODE_GUIDELINES.md](CODE_GUIDELINES.md).

## Architecture

**Content Structure:**
- `content/articles/YYYY-MM-DD-slug/` - Blog posts with date-based URLs
- `content/pages/slug/` - Static pages 
- `content/recipes/slug/` - Recipe content with special templates
- Images are placed adjacent to content files and automatically copied

**Plugin System (executes in order):**
1. `auto_title` - Generates titles from directory names, removes date prefixes
2. `recipes` - Creates recipe content type with custom URL structure  
3. `set_proper_category` - Manages content categorization
4. `filter_articles_for_index` - Controls content visibility
5. `copy_adjacent_images` - Auto-copies images, fixes relative URLs
6. `excerpt_to_summary` - Creates article summaries
7. `external_links` - Processes external link handling

**Markdown Extensions:**
- TOC support with `[TOC]` marker
- WikiLinks with `[[Page Name]]` syntax via `plugins.markdown_wikilinks`
- Meta, extra, codehilite extensions enabled

**Theme:** Custom "pelicanyan" theme based on Lanyon/Poole in `pelicanyan/` directory.

## Deployment

GitHub Actions automated pipeline:

- **Main branch** → grtnr.com (production)
- **Feature branches** → test.grtnr.com (staging)
- Uses external repositories for hosting

## Development Notes

- **WikiLinks**: Use `[[Page Name]]` syntax to link between content
- **Images**: Place images adjacent to content files - they're auto-copied and URLs fixed
- **Recipes**: Use recipe content type for cooking content with dedicated templates
- **Linting**: Flake8 with 88 character line length, W504 ignored
- **German characters** are automatically normalized in URLs via normalize_slugs plugin

## Content Guidelines

- Articles use date-prefixed directory structure: `YYYY-MM-DD-slug/`
- WikiLinks create interconnected navigation between content
- Tag pages are auto-generated from content tags
- Site uses timezone Europe/Rome, supports EN/DE date formats