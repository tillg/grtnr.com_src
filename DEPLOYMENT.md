# Deployment Guide

This guide covers how to deploy the site with automatic translation enabled.

## GitHub Actions Setup

### 1. Add Repository Secrets

Go to your repository **Settings** → **Secrets and variables** → **Actions** and add:

| Secret Name        | Description                          | Example  |
| ------------------ | ------------------------------------ | -------- |
| `OPENAI_API_KEY`   | OpenAI API key for translation service | `sk-...`  |
| `DEPLOYMENT_TOKEN` | GitHub token for deployment          | `ghp_...` |

### 2. Environment Configuration

The workflow automatically configures translation based on the branch:

#### Production (main branch)

- **Site**: grtnr.com
- **Translation**: Full (English, German, French)
- **Model**: GPT-4o
- **Excludes**: recipes only

#### Staging (feature branches)

- **Site**: test.grtnr.com
- **Translation**: Limited (German only)
- **Model**: GPT-4o
- **Excludes**: recipes, drafts

### 3. Translation Cache

The workflow caches translations to avoid re-translating unchanged content:

- Cache key includes content hash and branch
- Reduces API costs and build time
- Automatically invalidates when content changes

## Local Development

### 1. Environment Setup

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Enable Translation

Set environment variables or update `.env`:

```bash
GARTEN_TRANSLATION__ENABLED=true
TRANSLATION_TARGET_LANGUAGES=de,fr
TRANSLATION_MODEL=gpt-4o
```

### 3. Build and Test

```bash
# Full build with link checking
inv build

# Run test suite
python -m pytest tests/ -q

# Development server with auto-reload
inv livereload
```

## Translation Workflow

### Content Processing

1. **Content Discovery**: Scans all articles and pages during discover phase
2. **Language Detection**: Automatically detects source language
3. **Cache Check**: Checks for existing translations (hash-based)
4. **Translation**: Uses OpenAI API for new/changed content
5. **File Generation**: Creates translation files in `extensions/` directories

### Generated Structure

```text
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original
└── extensions/
    ├── 2025-01-01-example-EN.md   # English (if original is not English)
    ├── 2025-01-01-example-DE.md   # German
    └── 2025-01-01-example-FR.md   # French
```

### Translation Metadata

Each translation includes metadata:

```yaml
---
Translation: de
Source-Language: en
Source-File: /path/to/original.md
Source-Hash: abc123def456
Generated-Date: 2025-01-15T10:30:00
---
```

## Cost Management

### API Usage Optimization

- **Caching**: Avoids re-translating unchanged content (hash-based)
- **Staging Limits**: Test environment uses fewer languages
- **Content Exclusion**: Skip categories/paths that don't need translation
- **Rate Limiting**: Built-in delays between API calls

### Monitoring Usage

Check translation statistics in GitHub Actions logs:

```text
Translation Statistics:
Cache directory contents: 25 files
Generated translations: 120 files
```

### Cost Estimates

Approximate costs for GPT-4o:

- **Article** (~2000 chars): $0.03-0.06 per language
- **Page** (~1000 chars): $0.015-0.03 per language

Cache hit rate typically 80-90% after initial translation.

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Check repository secrets are set correctly
   - Verify secret name is exactly `OPENAI_API_KEY`

2. **Translation Failures**
   - Check OpenAI API quota and billing
   - Review rate limiting settings
   - Check workflow logs for specific errors

3. **Cache Issues**
   - Clear translations: `inv clean-translations`
   - Clear cache only: `inv clean-translations-cache`

4. **Quality Issues**
   - Review generated translations in `extensions/` directories
   - Adjust prompts in `extensions/translation_service/`

### Debug Commands

```bash
# Check configuration
python -c "
import os; import sys; sys.path.insert(0, 'extensions')
from translation_service import TranslationConfig
from dotenv import load_dotenv; load_dotenv()
config = TranslationConfig.from_environment()
print(f'Config: {config}')
"

# Health check
python -c "
import sys; sys.path.insert(0, 'extensions')
from translation_service import TranslationService, TranslationConfig
from dotenv import load_dotenv; load_dotenv()
config = TranslationConfig.from_environment()
service = TranslationService(config)
print(service.health_check())
"
```

## Security Best Practices

1. **API Keys**: Never commit API keys to code
2. **Environment Variables**: Use GitHub secrets for sensitive data
3. **Access Control**: Limit repository access to trusted collaborators
4. **Monitoring**: Review API usage regularly
5. **Rotation**: Rotate API keys periodically
