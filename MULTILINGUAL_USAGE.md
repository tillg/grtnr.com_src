# Multilingual Site Usage

This document explains how to use the multilingual site functionality that has been implemented.

## Overview

The multilingual site feature adds language switching capabilities to the existing static site. It builds upon the automatic translation system to provide a user-friendly way to switch between languages.

## Current Implementation Status

### ✅ Implemented Features

1. **Language Switcher in Sidebar**: Each article and page now shows language switching links
2. **Template Integration**: Language-aware templates with proper hreflang attributes
3. **SEO Support**: Basic hreflang tag structure for search engines
4. **CSS Styling**: Language switcher styling integrated with the existing theme

### 🚧 Partially Implemented

1. **URL Structure**: Basic language URLs are generated but full multilingual site structure is not yet built
2. **Translation Integration**: Plugin recognizes existing translations but doesn't yet generate separate language versions

### ❌ Not Yet Implemented

1. **Full Multilingual Site Structure**: Complete `/{lang}/` directory structure
2. **Language Selection Landing Page**: Root page for language selection
3. **Cross-Language Content Mapping**: Proper translation file integration
4. **Client-Side Language Detection**: Automatic language detection and redirection

## How to Enable

### 1. Environment Variables

Set the following environment variables:

```bash
# Enable multilingual functionality
export MULTILINGUAL_ENABLED=true

# Set supported languages (comma-separated)
export MULTILINGUAL_LANGUAGES=en,de,fr

# Set default language
export MULTILINGUAL_DEFAULT_LANG=en
```

### 2. Build the Site

```bash
# Development build with multilingual enabled
MULTILINGUAL_ENABLED=true inv build

# Production build with multilingual enabled  
MULTILINGUAL_ENABLED=true inv preview
```

## Current Functionality

### Language Switcher

When multilingual is enabled, each article and page will show a language switcher in the sidebar with:

- Links to other language versions
- Proper language names (English, Deutsch, Français)
- hreflang attributes for SEO
- Responsive styling

### URL Generation

Currently generates basic language URLs:
- Original: `/setting-up-a-mac/`
- German: `/de/setting-up-a-mac/`
- French: `/fr/setting-up-a-mac/`

## Translation Files

The system recognizes existing translation files in the `extensions/` directories:

```
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original content
└── extensions/
    ├── 2025-01-01-example-DE.md   # German translation
    ├── 2025-01-01-example-FR.md   # French translation
    └── 2025-01-01-example-ES.md   # Spanish translation
```

## Configuration

The multilingual plugin is configured in `pelicanconf.py`:

```python
# Multilingual site settings
MULTILINGUAL_ENABLED = os.environ.get("MULTILINGUAL_ENABLED", "false").lower() == "true"
MULTILINGUAL_LANGUAGES = os.environ.get("MULTILINGUAL_LANGUAGES", "en,de,fr").split(",")
MULTILINGUAL_DEFAULT_LANG = os.environ.get("MULTILINGUAL_DEFAULT_LANG", "en")
```

## Next Steps for Full Implementation

To complete the multilingual site functionality:

1. **Implement Full Site Generation**: Complete the `MultilingualSiteGenerator` to create separate language directories
2. **Add Language Selection Page**: Create root language selection page with auto-detection
3. **Improve URL Mapping**: Better translation slug handling and URL generation
4. **Add Client-Side Features**: Language preference persistence and detection
5. **Test and Refine**: Comprehensive testing and bug fixes

## Testing

To test the current implementation:

1. Enable multilingual mode: `MULTILINGUAL_ENABLED=true`
2. Build the site: `inv build`
3. Open any article page and check the sidebar for language switcher
4. Verify language links are present with proper hreflang attributes

## Known Issues

1. Generated language URLs may not point to actual content yet
2. Language switcher only appears when content has language_links attribute
3. Full multilingual site structure not yet generated

## Architecture

The implementation consists of:

- `plugins/multilingual_site.py`: Main multilingual plugin
- Enhanced templates with language-aware features
- CSS styling for language switcher
- Configuration integration in `pelicanconf.py`

For detailed architecture information, see `ARCHITECTURE.md` sections on "Multilingual Site Architecture".