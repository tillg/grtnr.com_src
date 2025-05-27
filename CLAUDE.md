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
