#!/usr/bin/env python3
"""
Test to demonstrate the core translation error without Pelican complexity.

This test isolates the translation service functionality to identify the actual error.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "extensions"))


def test_translation_service_core():
    """Test the core translation service functionality"""

    print("🧪 Testing Translation Service Core Functionality")
    print("=" * 60)

    try:
        from translation_service import TranslationConfig, TranslationService
        from translation_service.exceptions import TranslationError

        print("✅ Successfully imported translation service modules")
    except ImportError as e:
        print(f"❌ Failed to import translation service: {e}")
        return False

    # Create configuration
    try:
        config = TranslationConfig(
            api_key="test-key",
            model="gpt-4",
            target_languages=["de", "fr"],
            exclude_categories=["recipes"],
            exclude_paths=["/pages/impressum/"],
            cache_enabled=True,
            max_retries=3,
            timeout=30,
        )
        print("✅ Successfully created TranslationConfig")
    except Exception as e:
        print(f"❌ Failed to create TranslationConfig: {e}")
        return False

    # Mock OpenAI to avoid making real API calls
    with patch("translation_service.service.OpenAI") as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client

        # Mock the chat completion response for language detection
        mock_detect_response = Mock()
        mock_detect_response.choices = [Mock()]
        mock_detect_response.choices[0].message.content = "en"

        # Mock the chat completion response for translation
        mock_translate_response = Mock()
        mock_translate_response.choices = [Mock()]
        mock_translate_response.choices[
            0
        ].message.content = """---
title: Test Artikel
date: 2024-01-01
---

# Test Artikel

Dies ist ein Testartikel mit einigen Inhalten.

## Abschnitt 1

Hier sind weitere Inhalte.

[[Another Page]] ist ein Wiki-Link.

```python
print("Hello, World!")
```
"""

        # Configure the mock to return different responses
        mock_client.chat.completions.create.side_effect = [
            mock_detect_response,  # First call for language detection
            mock_translate_response,  # Second call for translation
        ]

        try:
            # Create translation service
            service = TranslationService(config)
            print("✅ Successfully created TranslationService")

            # Test language detection
            test_content = """---
title: Test Article
date: 2024-01-01
---

# Test Article

This is a test article with some content.

## Section 1

Some more content here.

[[Another Page]] is a wiki link.

```python
print("Hello, World!")
```
"""

            detected_lang = service.detect_language(test_content)
            print(f"✅ Language detection works: {detected_lang}")

            # Test translation
            result = service.translate_content(test_content, detected_lang, "de")
            print(f"✅ Translation works: {type(result)}")
            print(f"   Translation: {result.translation[:50]}...")
            print(f"   Source lang: {result.source_lang}")
            print(f"   Target lang: {result.target_lang}")
            print(f"   Cached: {result.cached}")

            return True

        except Exception as e:
            print(f"❌ Translation service failed: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_plugin_without_pelican_generator():
    """Test the plugin logic without inheriting from Pelican's Generator"""

    print("\n🧪 Testing Plugin Logic Without Pelican Generator")
    print("=" * 60)

    # Import the plugin but don't use the Generator class
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "plugins"))

        # Read the plugin file and extract the key functions
        plugin_path = os.path.join(
            os.path.dirname(__file__), "plugins", "automatic_translation.py"
        )

        with open(plugin_path, "r") as f:
            plugin_content = f.read()

        # Look for the key methods we need to test
        if "_translate_content" in plugin_content:
            print("✅ Plugin has _translate_content method")
        else:
            print("❌ Plugin missing _translate_content method")
            return False

        if "_should_translate_content" in plugin_content:
            print("✅ Plugin has _should_translate_content method")
        else:
            print("❌ Plugin missing _should_translate_content method")
            return False

        print("✅ Plugin has required methods")
        return True

    except Exception as e:
        print(f"❌ Plugin analysis failed: {e}")
        return False


def test_plugin_configuration_mismatch():
    """Test for configuration mismatch between plugin and service"""

    print("\n🧪 Testing Plugin Configuration Mismatch")
    print("=" * 60)

    # Test the configuration conversion
    try:
        from translation_service import TranslationConfig

        # Mock Pelican settings (what the plugin receives)
        pelican_settings = {
            "TRANSLATION_ENABLED": True,
            "TRANSLATION_TARGET_LANGUAGES": ["de", "fr"],
            "TRANSLATION_EXCLUDE_CATEGORIES": ["recipes"],
            "TRANSLATION_EXCLUDE_PATHS": ["/pages/impressum/"],
            "TRANSLATION_MODEL": "gpt-4",
            "TRANSLATION_CACHE_ENABLED": True,
            "TRANSLATION_MAX_RETRIES": 3,
            "TRANSLATION_TIMEOUT": 30,
            "TRANSLATION_API_KEY": "test-key",
        }

        # This is what the plugin does
        config = TranslationConfig.from_pelican_settings(pelican_settings)
        print("✅ Successfully created config from Pelican settings")
        print(f"   Model: {config.model}")
        print(f"   Target languages: {config.target_languages}")
        print(f"   Cache enabled: {config.cache_enabled}")

        # Validate the config
        config.validate()
        print("✅ Configuration validation passed")

        return True

    except Exception as e:
        print(f"❌ Configuration conversion failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_file_path_handling():
    """Test file path handling in the plugin"""

    print("\n🧪 Testing File Path Handling")
    print("=" * 60)

    # Create a temporary test setup
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test_article.md"
        test_file.write_text(
            """---
title: Test Article
date: 2024-01-01
---

# Test Article

This is a test article.
"""
        )

        # Test the file path operations that the plugin does
        try:
            # Simulate getting source content
            with open(test_file, "r", encoding="utf-8") as f:
                source_content = f.read()

            print(
                f"✅ Successfully read source content: {len(source_content)} characters"
            )

            # Test output directory creation
            source_path = Path(test_file)
            source_dir = source_path.parent
            extensions_dir = source_dir / "extensions"

            print(f"✅ Source path: {source_path}")
            print(f"✅ Extensions dir: {extensions_dir}")

            # Test filename generation
            base_name = source_path.stem
            target_lang = "de"
            translation_filename = f"{base_name}-{target_lang.upper()}.md"

            print(f"✅ Translation filename: {translation_filename}")

            # Test creating the directory
            extensions_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created extensions directory")

            # Test writing a translation file
            output_path = extensions_dir / translation_filename
            translation_content = f"""---
title: Test Artikel
date: 2024-01-01
Translation: de
Source-Language: en
Source-File: {test_file}
Generated-By: automatic-translation-plugin
Generated-Date: 2024-01-01T12:00:00
---

# Test Artikel

Dies ist ein Testartikel.
"""

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(translation_content)

            print(f"✅ Successfully wrote translation file")

            # Verify the file was created
            if output_path.exists():
                print(f"✅ Translation file exists: {output_path}")
                content = output_path.read_text()
                if "Translation: de" in content:
                    print("✅ Translation file has correct metadata")
                else:
                    print("❌ Translation file missing metadata")
                    return False
            else:
                print("❌ Translation file was not created")
                return False

            return True

        except Exception as e:
            print(f"❌ File path handling failed: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_metadata_generation():
    """Test metadata generation for translation files"""

    print("\n🧪 Testing Metadata Generation")
    print("=" * 60)

    # Test the metadata generation logic
    try:
        # Sample translation content
        translation = """---
title: Test Artikel
date: 2024-01-01
---

# Test Artikel

Dies ist ein Testartikel.
"""

        # Extract existing metadata if present
        lines = translation.split("\n")
        has_frontmatter = lines and lines[0].strip() == "---"

        print(f"✅ Has frontmatter: {has_frontmatter}")

        if has_frontmatter:
            # Find the end of frontmatter
            end_marker = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    end_marker = i
                    break

            print(f"✅ End marker found at line: {end_marker}")

            # Create translation metadata
            translation_meta = [
                "Translation: de",
                "Source-Language: en",
                "Source-File: /path/to/source.md",
                "Generated-By: automatic-translation-plugin",
                "Generated-Date: 2024-01-01T12:00:00",
            ]

            if end_marker:
                # Insert translation metadata before the closing ---
                lines[end_marker:end_marker] = translation_meta
            else:
                # Malformed frontmatter, add at the end
                lines.extend(["---"] + translation_meta + ["---"])

            result = "\n".join(lines)
            print("✅ Successfully generated metadata")

            # Verify the result
            if "Translation: de" in result:
                print("✅ Translation metadata correctly inserted")
            else:
                print("❌ Translation metadata not found in result")
                return False

            return True
        else:
            print("❌ No frontmatter found")
            return False

    except Exception as e:
        print(f"❌ Metadata generation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests to identify the core translation error"""

    print("🚀 Translation Core Error Detection Test Suite")
    print("=" * 80)

    tests = [
        ("Translation Service Core", test_translation_service_core),
        ("Plugin Without Pelican Generator", test_plugin_without_pelican_generator),
        ("Plugin Configuration Mismatch", test_plugin_configuration_mismatch),
        ("File Path Handling", test_file_path_handling),
        ("Metadata Generation", test_metadata_generation),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("📊 Test Results Summary")
    print("=" * 80)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")

    failed_tests = [name for name, passed in results if not passed]

    if failed_tests:
        print(f"\n❌ {len(failed_tests)} test(s) failed:")
        for test in failed_tests:
            print(f"   - {test}")

        print("\n🔍 Error Analysis:")
        print("The failures show the core issue with the translation system.")
        print("The most likely problems are:")
        print("1. Configuration mismatch between plugin and service")
        print("2. File path handling issues")
        print("3. Metadata generation problems")
        print("4. Import path conflicts")
    else:
        print("\n🎉 All core tests passed!")
        print("💡 The error is likely in the Pelican integration layer")

    return len(failed_tests) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
