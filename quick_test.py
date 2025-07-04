#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add extensions to path
sys.path.insert(0, 'extensions')

from dotenv import load_dotenv
load_dotenv()

from translation_service import TranslationService, TranslationConfig

def test_simple_translations():
    """Test simple translations to verify everything works"""
    
    print("🚀 Quick Translation Test")
    print("=" * 50)
    
    # Setup service
    config = TranslationConfig.from_environment()
    service = TranslationService(config)
    
    # Test content
    test_content = """# Hello World

This is a **simple test** of the translation service.

- It has lists
- Code blocks like `print("hello")`
- And [[WikiLinks]] to other pages

## Conclusion

The service should preserve all markdown formatting."""

    print(f"📝 Original content:\n{test_content}\n")
    
    # Test each target language
    for lang in config.target_languages:
        print(f"🔄 Translating to {lang.upper()}...")
        
        try:
            result = service.translate_content(
                content=test_content,
                source_lang="en", 
                target_lang=lang
            )
            
            print(f"✅ {lang.upper()} Translation:")
            print(f"{'=' * 30}")
            print(result.translation)
            print(f"Cached: {result.cached}")
            print()
            
        except Exception as e:
            print(f"❌ Translation to {lang} failed: {e}\n")
    
    # Test cache stats
    print("📊 Cache Statistics:")
    stats = service.get_cache_stats()
    print(f"  Cached translations: {stats.get('total_cached_translations', 0)}")
    print(f"  Cache size: {stats.get('cache_size_mb', 0):.2f} MB")
    print(f"  Languages: {stats.get('languages', [])}")

if __name__ == "__main__":
    test_simple_translations()