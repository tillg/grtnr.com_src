#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add extensions to path
sys.path.insert(0, "extensions")

from dotenv import load_dotenv

load_dotenv()

from translation_service import TranslationConfig, TranslationService


def translate_sample_files():
    """Translate the sample test files and show where results are saved"""

    print("🚀 Testing Sample File Translations")
    print("=" * 50)

    # Setup service
    config = TranslationConfig.from_environment()
    service = TranslationService(config)

    # Test files directory
    fixtures_dir = Path("extensions/tests/fixtures")
    output_dir = Path("extensions/tests/output")
    output_dir.mkdir(exist_ok=True)

    # Get sample files
    sample_files = ["sample_article.md", "sample_recipe.md"]

    for sample_file in sample_files:
        print(f"\n📄 Processing {sample_file}")
        print("-" * 30)

        # Read content
        sample_path = fixtures_dir / sample_file
        with open(sample_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"📝 Content length: {len(content)} characters")

        # Detect language
        source_lang = service.detect_language(content)
        print(f"🔍 Detected language: {source_lang}")

        # Translate to each target language (limit to 2 to save time/cost)
        test_languages = config.target_languages[:2]  # Just test first 2 languages

        for target_lang in test_languages:
            print(f"\n🔄 Translating to {target_lang.upper()}...")

            try:
                result = service.translate_content(
                    content=content, source_lang=source_lang, target_lang=target_lang
                )

                # Save translation
                base_name = sample_path.stem
                output_filename = f"{base_name}_{target_lang.upper()}.md"
                output_path = output_dir / output_filename

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.translation)

                print(f"✅ Saved to: {output_path}")
                print(f"📊 Cached: {result.cached}")
                print(f"📏 Translation length: {len(result.translation)} characters")

                # Show first few lines
                lines = result.translation.split("\n")
                print("📖 First few lines:")
                for i, line in enumerate(lines[:3]):
                    if line.strip():
                        print(f"   {line}")
                        if i >= 2:
                            break

            except Exception as e:
                print(f"❌ Translation failed: {e}")

    print(f"\n📁 All translations saved to: {output_dir.absolute()}")

    # Show cache stats
    print(f"\n📊 Cache Statistics:")
    stats = service.get_cache_stats()
    print(f"  Cached translations: {stats.get('total_cached_translations', 0)}")
    print(f"  Cache directory: {stats.get('cache_directory', 'Not available')}")
    print(f"  Languages: {stats.get('languages', [])}")


if __name__ == "__main__":
    translate_sample_files()
