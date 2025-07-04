# Translation Service

This directory contains the automatic translation service for the Pelican-based website. The service provides AI-powered translation of articles and pages using OpenAI's GPT API.

## Quick Start

1. **Setup API Key**: Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

2. **Install Dependencies**: The required packages are already in `requirements.txt`:
   ```bash
   pip install -r .devcontainer/requirements.txt
   ```

3. **Enable Translation**: Add to your `pelicanconf.py`:
   ```python
   TRANSLATION_ENABLED = True
   TRANSLATION_TARGET_LANGUAGES = ["de", "fr", "es"]
   ```

4. **Run Tests**: Test the service before using it:
   ```bash
   cd extensions/tests
   python run_tests.py --all
   ```

## Directory Structure

```
extensions/
├── translation_service/        # Core translation service
│   ├── __init__.py
│   ├── service.py             # Main TranslationService class
│   ├── cache.py               # Translation caching
│   ├── config.py              # Configuration management
│   ├── prompts.py             # Translation prompts
│   └── exceptions.py          # Custom exceptions
├── plugins/
│   └── automatic_translation.py  # Pelican plugin
├── tests/
│   ├── run_tests.py           # Test runner
│   ├── test_translation_service.py  # Manual testing framework
│   ├── test_translation_cache.py   # Unit tests
│   └── fixtures/              # Test content samples
└── README.md                  # This file
```

## Configuration

### Environment Variables (.env file)

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
TRANSLATION_MODEL=gpt-4
TRANSLATION_TARGET_LANGUAGES=de,fr,es
TRANSLATION_EXCLUDE_CATEGORIES=recipes,drafts
TRANSLATION_EXCLUDE_PATHS=/pages/impressum/,/admin/
TRANSLATION_CACHE_ENABLED=true
TRANSLATION_CACHE_DIR=./cache/translations
TRANSLATION_MAX_RETRIES=3
TRANSLATION_TIMEOUT=30
```

### Pelican Settings (pelicanconf.py)

```python
# Enable automatic translation
TRANSLATION_ENABLED = True

# Target languages (ISO 639-1 codes)
TRANSLATION_TARGET_LANGUAGES = ["de", "fr", "es"]

# Categories to exclude from translation
TRANSLATION_EXCLUDE_CATEGORIES = ["recipes", "drafts"]

# Paths to exclude from translation
TRANSLATION_EXCLUDE_PATHS = ["/pages/impressum/", "/admin/"]

# API configuration
TRANSLATION_MODEL = "gpt-4"
TRANSLATION_MAX_RETRIES = 3
TRANSLATION_TIMEOUT = 30

# Cache configuration
TRANSLATION_CACHE_ENABLED = True
TRANSLATION_CACHE_DIR = "./cache/translations"
```

## Usage

### Automatic Translation (Pelican Plugin)

Once configured, the translation service runs automatically during Pelican site generation. It will:

1. Scan all articles and pages
2. Skip excluded categories and paths
3. Detect source language automatically
4. Translate to all target languages
5. Save translations in `content/*/extensions/` directories

### Manual Translation (Standalone)

You can also use the translation service independently:

```python
from translation_service import TranslationService, TranslationConfig

# Load configuration from .env
config = TranslationConfig.from_dotenv()
service = TranslationService(config)

# Translate content
result = service.translate_content(
    content="# Hello World\n\nThis is a test.",
    source_lang="en",
    target_lang="de"
)

print(result.translation)
print(f"Cached: {result.cached}")
```

### Testing Translation Quality

Run manual translation tests to review quality:

```bash
cd extensions/tests
python run_tests.py --manual
```

This will:
- Translate sample content to all target languages
- Generate a comparison report
- Run automated quality checks
- Save results in `extensions/tests/output/`

## Generated File Structure

When translations are created, they follow this structure:

```
content/articles/2025-01-01-example/
├── 2025-01-01-example.md          # Original article
└── extensions/
    ├── 2025-01-01-example-DE.md   # German translation
    ├── 2025-01-01-example-FR.md   # French translation
    └── 2025-01-01-example-ES.md   # Spanish translation
```

Each translation file includes metadata:
```yaml
---
Translation: de
Source-Language: en
Source-File: /path/to/original.md
Generated-By: automatic-translation-plugin
Generated-Date: 2025-01-15T10:30:00
---
```

## Advanced Features

### Caching

The service uses content-based hashing for intelligent caching:
- Translations are cached based on content hash
- Cache automatically invalidates when content changes
- Separate cache entries for each target language
- Configurable TTL (default: 30 days)

### Language Detection

Automatic source language detection:
- Uses GPT to detect the primary language
- Falls back to configured default (usually 'en')
- Can be disabled to use fixed source language

### Error Handling

Robust error handling with retry logic:
- Exponential backoff for rate limits
- Graceful degradation on API failures
- Detailed logging for debugging
- Site generation continues even if translation fails

### Quality Validation

Automated quality checks:
- Markdown structure preservation
- WikiLinks format validation
- Code block preservation
- Image alt-text handling
- Reasonable translation length

## Supported Languages

The service supports these language codes:
- `en` - English
- `de` - German  
- `fr` - French
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese
- `ar` - Arabic
- `hi` - Hindi
- `nl` - Dutch
- `sv` - Swedish
- `no` - Norwegian
- `da` - Danish
- `fi` - Finnish
- `pl` - Polish
- `cs` - Czech
- `tr` - Turkish

## Performance Tips

1. **Use Caching**: Keep `TRANSLATION_CACHE_ENABLED=true` for faster rebuilds
2. **Rate Limiting**: Adjust `TRANSLATION_RATE_LIMIT_DELAY` if hitting API limits
3. **Exclude Content**: Use exclude settings to skip unnecessary translations
4. **Model Selection**: Use `gpt-4-turbo` for better performance vs. quality balance

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Check your `.env` file exists and contains `OPENAI_API_KEY`
   - Ensure `.env` is in the project root directory

2. **Rate Limit Errors**
   - Increase `TRANSLATION_RATE_LIMIT_DELAY`
   - Reduce batch size by excluding some content
   - Check your OpenAI API usage limits

3. **Translation Quality Issues**
   - Run manual tests: `python run_tests.py --manual`
   - Review the generated comparison report
   - Adjust prompts in `translation_service/prompts.py`

4. **Cache Problems**
   - Clear cache: `rm -rf cache/translations/*`
   - Disable cache temporarily: `TRANSLATION_CACHE_ENABLED=false`
   - Check cache directory permissions

### Health Check

Run a health check to verify service configuration:

```python
from translation_service import TranslationService, TranslationConfig

config = TranslationConfig.from_dotenv()
service = TranslationService(config)
health = service.health_check()
print(health)
```

### Logging

Enable debug logging for detailed information:

```python
# In pelicanconf.py
from logger_config import setup_pelican_logging
setup_pelican_logging('DEBUG')
```

## Contributing

To contribute to the translation service:

1. **Add Tests**: Create tests in `extensions/tests/`
2. **Update Documentation**: Keep README and architecture docs current
3. **Test Quality**: Run the full test suite before submitting changes
4. **Follow Patterns**: Use existing code patterns and logging

## Security

- API keys are never logged or stored in code
- Cache files contain no sensitive information
- Use environment variables or `.env` files for configuration
- Never commit `.env` files to version control

## License

This translation service is part of the grtnr.com project and follows the same licensing terms.