# Deployment Guide

This guide covers how to deploy the site with automatic translation enabled.

## GitHub Actions Setup

### 1. Add Repository Secrets

Go to your repository **Settings** → **Secrets and variables** → **Actions** and add:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for translation service | `sk-...` |
| `DEPLOYMENT_TOKEN` | GitHub token for deployment | `ghp_...` |

### 2. Environment Configuration

The workflow automatically configures translation based on the branch:

#### Production (main branch)
- **Site**: grtnr.com
- **Translation**: Full (German, French, Spanish)
- **Model**: GPT-4
- **Excludes**: recipes only

#### Staging (feature branches)  
- **Site**: test.grtnr.com
- **Translation**: Limited (German only)
- **Model**: GPT-4
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
TRANSLATION_ENABLED=true
TRANSLATION_TARGET_LANGUAGES=de,fr
TRANSLATION_MODEL=gpt-4
```

### 3. Test Translation

```bash
# Run quick test
python test_api.py

# Test with sample files  
python test_sample_files.py

# Full test suite
cd extensions/tests && python run_tests.py --all
```

## Translation Workflow

### Content Processing

1. **Content Discovery**: Scans all articles and pages
2. **Language Detection**: Automatically detects source language
3. **Cache Check**: Checks for existing translations
4. **Translation**: Uses OpenAI API for new/changed content
5. **File Generation**: Creates translation files in `extensions/` directories

### Generated Structure

```
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original
└── extensions/
    ├── 2025-01-01-example-DE.md   # German
    ├── 2025-01-01-example-FR.md   # French  
    └── 2025-01-01-example-ES.md   # Spanish
```

### Translation Metadata

Each translation includes metadata:
```yaml
---
Translation: de
Source-Language: en
Source-File: /path/to/original.md
Generated-By: automatic-translation-plugin
Generated-Date: 2025-01-15T10:30:00
---
```

## Cost Management

### API Usage Optimization

- **Caching**: Avoids re-translating unchanged content
- **Staging Limits**: Test environment uses fewer languages
- **Content Exclusion**: Skip categories/paths that don't need translation
- **Rate Limiting**: Built-in delays between API calls

### Monitoring Usage

Check translation statistics in GitHub Actions logs:
```
📊 Translation Statistics:
Cache directory contents: 25 files
Generated translations: 120 files
```

### Cost Estimates

Approximate costs for GPT-4:
- **Article** (~2000 chars): $0.03-0.06 per language
- **Page** (~1000 chars): $0.015-0.03 per language
- **Recipe** (~1500 chars): $0.02-0.045 per language

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
   - Clear cache: Delete `cache/translations/` directory
   - Force rebuild: Change cache key in workflow

4. **Quality Issues**
   - Run manual quality tests locally
   - Adjust prompts in `translation_service/prompts.py`
   - Review generated translations

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

## Performance Tips

1. **Selective Translation**: Use exclusion patterns for unnecessary content
2. **Branch Strategy**: Use feature branches for testing
3. **Cache Management**: Monitor cache hit rates
4. **Content Organization**: Group related content to optimize cache usage
5. **Model Selection**: Consider gpt-4-turbo for better cost/performance balance

## Future Enhancements

Planned improvements:
- Batch translation for better efficiency
- Translation quality scoring
- Custom terminology dictionaries
- Multi-model fallback strategy
- Real-time translation updates
- Web interface for translation review