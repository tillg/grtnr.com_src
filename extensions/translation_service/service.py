"""
Translation Service Implementation

Core translation service using OpenAI's GPT API.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None
    OpenAI = None

from .config import TranslationConfig
from .cache import TranslationCache
from .prompts import TranslationPrompts
from .exceptions import (
    TranslationError,
    APIError,
    RateLimitError,
    InvalidResponseError,
    LanguageNotSupportedError,
    ConfigurationError
)


@dataclass
class TranslationResult:
    """Result of a translation operation"""
    translation: str
    source_lang: str
    target_lang: str
    cached: bool = False
    metadata: Dict[str, Any] = None
    model: str = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TranslationAPIClient:
    """Handles OpenAI API calls with retry logic"""
    
    def __init__(self, config: TranslationConfig, prompts: TranslationPrompts):
        if OpenAI is None:
            raise ConfigurationError("OpenAI package is not installed. Run: pip install openai")
        
        self.config = config
        self.prompts = prompts
        self.client = OpenAI(
            api_key=self.config.api_key,
            timeout=self.config.timeout
        )
        self.logger = logging.getLogger(__name__)
        
        # Suppress verbose HTTP logging from external libraries
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
    
    def translate(self, content: str, source_lang: str, target_lang: str) -> tuple[str, str]:
        """Make API call to OpenAI with retry logic"""
        
        prompt = self.prompts.build_translation_prompt(content, source_lang, target_lang)
        
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": self.prompts.get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4096
                )
                
                translation = response.choices[0].message.content.strip()
                
                if not translation:
                    raise InvalidResponseError("Empty translation received")
                
                # Clean up any markdown wrapper that might have been added
                translation = self._clean_markdown_wrapper(translation)
                
                # Validate translation
                validation_results = self.prompts.validate_translation_response(translation, content)
                
                if not validation_results.get('has_content', True):
                    raise InvalidResponseError("Translation validation failed: no content")
                
                # Extract model information from response
                model_info = response.model if hasattr(response, 'model') else self.config.model
                
                return translation, model_info
                
            except Exception as e:
                last_exception = e
                
                if attempt < self.config.max_retries:
                    # Handle rate limiting
                    if "rate_limit" in str(e).lower():
                        wait_time = min(2 ** attempt, 60)  # Exponential backoff, max 60 seconds
                        self.logger.warning(f"Rate limit hit, waiting {wait_time} seconds")
                        time.sleep(wait_time)
                        continue
                    
                    # Handle other API errors
                    if "api" in str(e).lower():
                        wait_time = 2 ** attempt
                        self.logger.warning(f"API error, retrying in {wait_time} seconds")
                        time.sleep(wait_time)
                        continue
                
                # Log the error for the final attempt
                self.logger.error(f"API call attempt {attempt + 1} failed: {e}")
        
        # All retries failed
        if "rate_limit" in str(last_exception).lower():
            raise RateLimitError(f"Rate limit exceeded after {self.config.max_retries} retries")
        else:
            raise APIError(f"API call failed after {self.config.max_retries} retries: {last_exception}")
    
    def detect_language(self, content: str) -> str:
        """Detect the primary language of content"""
        
        if not self.config.auto_detect_language:
            return self.config.default_source_language
        
        prompt = self.prompts.build_language_detection_prompt(content)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self.prompts.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            detected_lang = response.choices[0].message.content.strip().lower()
            
            # Clean up the response - remove any quotes or extra characters
            detected_lang = detected_lang.strip('\'"` ')
            
            # Extract just the language code if there's extra text
            for supported_lang in self.prompts.get_supported_languages():
                if supported_lang in detected_lang:
                    detected_lang = supported_lang
                    break
            
            # Validate detected language
            if self.prompts.is_language_supported(detected_lang):
                return detected_lang
            else:
                self.logger.warning(f"Detected unsupported language '{detected_lang}', using default")
                return self.config.default_source_language
                
        except Exception as e:
            self.logger.warning(f"Language detection failed: {e}, using default")
            return self.config.default_source_language
    
    def _clean_markdown_wrapper(self, content: str) -> str:
        """Remove markdown code block wrapper if present"""
        original_content = content
        content = content.strip()
        
        # Pattern: ```markdown followed by content followed by ```
        if content.startswith('```markdown'):
            # Find the closing ```
            lines = content.split('\n')
            if len(lines) > 2:
                # Look for the first closing ``` after the opening
                for i in range(len(lines) - 1, 0, -1):  # Search backwards
                    if lines[i].strip() == '```':
                        # Extract content between the markers
                        inner_content = '\n'.join(lines[1:i])
                        content = inner_content
                        self.logger.debug("Removed ```markdown wrapper from translation")
                        break
        
        # Pattern: ``` followed by content followed by ```
        elif content.startswith('```') and not content.startswith('```markdown'):
            lines = content.split('\n')
            if len(lines) > 2:
                # Look for the first closing ``` after the opening
                for i in range(len(lines) - 1, 0, -1):  # Search backwards
                    if lines[i].strip() == '```':
                        # Extract content between the markers
                        inner_content = '\n'.join(lines[1:i])
                        content = inner_content
                        self.logger.debug("Removed ``` wrapper from translation")
                        break
        
        content = content.strip()
        
        # Log if we cleaned something
        if content != original_content.strip():
            self.logger.info(f"Cleaned markdown wrapper from translation (original: {len(original_content)} chars, cleaned: {len(content)} chars)")
        
        return content


class BatchTranslationProcessor:
    """Handles batch processing of multiple translations"""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def process_batch(self, contents: List[str], source_lang: str, target_lang: str, 
                     translation_func) -> List[TranslationResult]:
        """Process multiple translations in batch"""
        
        results = []
        
        for i, content in enumerate(contents):
            self.logger.debug(f"Processing batch item {i+1}/{len(contents)}")
            
            try:
                result = translation_func(content, source_lang, target_lang)
                results.append(result)
                
                # Rate limiting
                if i < len(contents) - 1:  # Don't wait after the last item
                    time.sleep(self.config.rate_limit_delay)
                    
            except Exception as e:
                self.logger.error(f"Batch item {i+1} failed: {e}")
                # Create error result
                results.append(TranslationResult(
                    translation=f"ERROR: {str(e)}",
                    source_lang=source_lang,
                    target_lang=target_lang,
                    cached=False,
                    metadata={'error': str(e)}
                ))
        
        return results


class TranslationService:
    """AI-powered translation service using OpenAI's GPT API"""
    
    def __init__(self, config: TranslationConfig):
        """Initialize translation service with configuration"""
        
        self.config = config
        self.config.validate()
        
        # Initialize components
        self.prompts = TranslationPrompts()
        self.api_client = TranslationAPIClient(config, self.prompts)
        self.batch_processor = BatchTranslationProcessor(config)
        
        # Initialize cache if enabled
        self.cache = None
        if self.config.cache_enabled:
            self.cache = TranslationCache(
                cache_dir=self.config.cache_dir
            )
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def translate_content(self, content: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate content from source language to target language"""
        
        # Validate languages
        if not self.prompts.is_language_supported(source_lang):
            raise LanguageNotSupportedError(source_lang)
        if not self.prompts.is_language_supported(target_lang):
            raise LanguageNotSupportedError(target_lang)
        
        # Check cache first
        if self.cache:
            cached_translation = self.cache.get_cached_translation(content, target_lang)
            if cached_translation:
                self.logger.debug(f"Cache hit for {target_lang} translation")
                return TranslationResult(
                    translation=cached_translation,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    cached=True,
                    model=self.config.model  # Use configured model for cached results
                )
        
        # Perform translation via API client
        self.logger.debug(f"Translating content from {source_lang} to {target_lang}")
        
        try:
            translation, model_info = self.api_client.translate(content, source_lang, target_lang)
            
            # Cache the translation
            if self.cache:
                self.cache.cache_translation(
                    content=content,
                    target_lang=target_lang,
                    translation=translation,
                    source_lang=source_lang,
                    metadata={
                        'model': model_info,
                        'service_version': '1.0.0'
                    }
                )
            
            return TranslationResult(
                translation=translation,
                source_lang=source_lang,
                target_lang=target_lang,
                cached=False,
                model=model_info
            )
            
        except Exception as e:
            self.logger.error(f"Translation failed: {e}")
            raise
    
    def detect_language(self, content: str) -> str:
        """Detect the primary language of content"""
        return self.api_client.detect_language(content)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return self.prompts.get_supported_languages()
    
    def translate_batch(self, contents: List[str], source_lang: str, target_lang: str) -> List[TranslationResult]:
        """Translate multiple contents in batch"""
        return self.batch_processor.process_batch(contents, source_lang, target_lang, self.translate_content)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if self.cache:
            return self.cache.get_cache_stats()
        return {'cache_enabled': False}
    
    def clear_cache(self) -> None:
        """Clear translation cache"""
        if self.cache:
            self.cache.clear_cache()
            self.logger.info("Translation cache cleared")
    
    def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries"""
        if self.cache:
            removed_count = self.cache.cleanup_expired_cache()
            self.logger.debug(f"Removed {removed_count} expired cache entries")
            return removed_count
        return 0
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check of the translation service"""
        
        health_status = {
            'service': 'translation_service',
            'status': 'healthy',
            'checks': {},
            'config': {
                'model': self.config.model,
                'cache_enabled': self.config.cache_enabled,
                'target_languages': self.config.target_languages
            }
        }
        
        # Check API connectivity
        try:
            # Simple test translation
            test_result = self.translate_content("Hello", "en", "es")
            health_status['checks']['api_connectivity'] = 'pass'
        except Exception as e:
            health_status['checks']['api_connectivity'] = f'fail: {e}'
            health_status['status'] = 'unhealthy'
        
        # Check cache
        if self.cache:
            try:
                cache_stats = self.cache.get_cache_stats()
                health_status['checks']['cache'] = 'pass'
                health_status['cache_stats'] = cache_stats
            except Exception as e:
                health_status['checks']['cache'] = f'fail: {e}'
                health_status['status'] = 'unhealthy'
        
        return health_status
    
    def __repr__(self) -> str:
        """String representation of translation service"""
        return (
            f"TranslationService("
            f"model='{self.config.model}', "
            f"cache_enabled={self.config.cache_enabled}, "
            f"target_languages={len(self.config.target_languages)}"
            f")"
        )