#!/usr/bin/env python3
"""
Test to demonstrate the actual error in the automatic translation plugin.

This test simulates the actual Pelican build process and identifies the real error.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the plugins directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'plugins'))

def test_plugin_integration():
    """Test the actual plugin integration to find the real error"""
    
    print("🧪 Testing Plugin Integration Error")
    print("=" * 50)
    
    # Import the plugin
    try:
        from automatic_translation import TranslationGenerator
        print("✅ Successfully imported TranslationGenerator")
    except ImportError as e:
        print(f"❌ Failed to import TranslationGenerator: {e}")
        return False
    
    # Mock Pelican settings
    mock_settings = {
        'TRANSLATION_ENABLED': True,
        'TRANSLATION_TARGET_LANGUAGES': ['de', 'fr'],
        'TRANSLATION_EXCLUDE_CATEGORIES': ['recipes'],
        'TRANSLATION_EXCLUDE_PATHS': ['/pages/impressum/'],
        'TRANSLATION_MODEL': 'gpt-4',
        'TRANSLATION_CACHE_ENABLED': True,
        'TRANSLATION_MAX_RETRIES': 3,
        'TRANSLATION_TIMEOUT': 30,
        'TRANSLATION_API_KEY': 'test-key',
    }
    
    # Mock Pelican context
    mock_context = {
        'articles': [],
        'pages': []
    }
    
    # Create a temporary test article
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test_article.md"
        test_file.write_text("""---
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
""")
        
        # Create a mock article object
        mock_article = Mock()
        mock_article.title = "Test Article"
        mock_article.source_path = str(test_file)
        mock_article.category = Mock()
        mock_article.category.name = "articles"
        mock_article.metadata = {}
        
        mock_context['articles'] = [mock_article]
        
        # Mock OpenAI to avoid making real API calls
        with patch('extensions.translation_service.service.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            
            # Mock the chat completion response for language detection
            mock_detect_response = Mock()
            mock_detect_response.choices = [Mock()]
            mock_detect_response.choices[0].message.content = "en"
            
            # Mock the chat completion response for translation
            mock_translate_response = Mock()
            mock_translate_response.choices = [Mock()]
            mock_translate_response.choices[0].message.content = """---
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
                mock_detect_response,  # Third call for language detection (second language)
                mock_translate_response,  # Fourth call for translation (second language)
            ]
            
            try:
                # Try to create the translation generator
                generator = TranslationGenerator(
                    context=mock_context,
                    settings=mock_settings,
                    path="content",
                    theme="theme",
                    output_path="output"
                )
                
                print("✅ Successfully created TranslationGenerator")
                
                # Check if the translation service was initialized
                if generator.translation_service is None:
                    print("❌ Translation service was not initialized")
                    return False
                
                print("✅ Translation service initialized successfully")
                
                # Try to process the mock article
                print("\n🔍 Testing content translation:")
                
                # Mock the writer
                mock_writer = Mock()
                
                # Call generate_output to test the actual plugin logic
                generator.generate_output(mock_writer)
                
                print("✅ generate_output() completed without errors")
                
                # Check if translation files were created
                extensions_dir = test_file.parent / "extensions"
                if extensions_dir.exists():
                    translation_files = list(extensions_dir.glob("*.md"))
                    print(f"✅ Created {len(translation_files)} translation files:")
                    for file in translation_files:
                        print(f"   - {file.name}")
                        
                        # Check the content
                        content = file.read_text()
                        if "Translation:" in content:
                            print(f"   ✅ {file.name} has translation metadata")
                        else:
                            print(f"   ⚠️  {file.name} missing translation metadata")
                else:
                    print("❌ No translation files were created")
                    return False
                
                return True
                
            except Exception as e:
                print(f"❌ Plugin integration failed: {e}")
                import traceback
                traceback.print_exc()
                return False

def test_config_api_key_issue():
    """Test for API key configuration issues"""
    
    print("\n🧪 Testing API Key Configuration")
    print("=" * 50)
    
    # Test without API key
    mock_settings_no_key = {
        'TRANSLATION_ENABLED': True,
        'TRANSLATION_TARGET_LANGUAGES': ['de', 'fr'],
        'TRANSLATION_EXCLUDE_CATEGORIES': ['recipes'],
        'TRANSLATION_EXCLUDE_PATHS': ['/pages/impressum/'],
        'TRANSLATION_MODEL': 'gpt-4',
        'TRANSLATION_CACHE_ENABLED': True,
        'TRANSLATION_MAX_RETRIES': 3,
        'TRANSLATION_TIMEOUT': 30,
        # No API key!
    }
    
    # Mock Pelican context
    mock_context = {'articles': [], 'pages': []}
    
    try:
        from automatic_translation import TranslationGenerator
        
        # This should fail due to missing API key
        generator = TranslationGenerator(
            context=mock_context,
            settings=mock_settings_no_key,
            path="content",
            theme="theme",
            output_path="output"
        )
        
        if generator.translation_service is None:
            print("✅ Generator correctly failed to initialize without API key")
            return True
        else:
            print("❌ Generator should have failed without API key")
            return False
            
    except Exception as e:
        print(f"✅ Correctly failed with missing API key: {e}")
        return True

def test_import_path_issue():
    """Test for import path issues"""
    
    print("\n🧪 Testing Import Path Issues")
    print("=" * 50)
    
    # Test the actual import path from the plugin
    try:
        # Add the extensions directory to the path (same as plugin does)
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'extensions'))
        
        from translation_service import TranslationService, TranslationConfig
        from translation_service.exceptions import TranslationError
        
        print("✅ All imports successful - no import path issues")
        return True
        
    except ImportError as e:
        print(f"❌ Import path issue found: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    
    print("\n🧪 Testing Environment Variables")
    print("=" * 50)
    
    # Check if OPENAI_API_KEY is set
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        print(f"✅ OPENAI_API_KEY is set: {api_key[:10]}...")
    else:
        print("❌ OPENAI_API_KEY is not set in environment")
        print("💡 This could cause the translation service to fail")
        return False
    
    # Check translation-related environment variables
    translation_vars = [
        'TRANSLATION_ENABLED',
        'TRANSLATION_TARGET_LANGUAGES',
        'TRANSLATION_EXCLUDE_CATEGORIES',
        'TRANSLATION_EXCLUDE_PATHS',
        'TRANSLATION_MODEL',
        'TRANSLATION_CACHE_ENABLED',
        'TRANSLATION_MAX_RETRIES',
        'TRANSLATION_TIMEOUT',
    ]
    
    for var in translation_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} = {value}")
        else:
            print(f"⚠️  {var} not set (using default)")
    
    return True

def test_plugin_loading_order():
    """Test plugin loading order issues"""
    
    print("\n🧪 Testing Plugin Loading Order")
    print("=" * 50)
    
    # Check if there are multiple translation plugins
    plugins_dir = Path(__file__).parent / "plugins"
    translation_plugins = []
    
    for plugin_file in plugins_dir.glob("*translation*.py"):
        translation_plugins.append(plugin_file.name)
    
    if len(translation_plugins) > 1:
        print("❌ Multiple translation plugins found:")
        for plugin in translation_plugins:
            print(f"   - {plugin}")
        print("💡 This could cause conflicts")
        return False
    else:
        print(f"✅ Single translation plugin found: {translation_plugins[0] if translation_plugins else 'none'}")
        return True

def main():
    """Run all tests to identify the actual error"""
    
    print("🚀 Actual Translation Error Detection Test Suite")
    print("=" * 70)
    
    tests = [
        ("Plugin Integration", test_plugin_integration),
        ("API Key Configuration", test_config_api_key_issue),
        ("Import Path Issues", test_import_path_issue),
        ("Environment Variables", test_environment_variables),
        ("Plugin Loading Order", test_plugin_loading_order),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    failed_tests = [name for name, passed in results if not passed]
    
    if failed_tests:
        print(f"\n❌ {len(failed_tests)} test(s) failed:")
        for test in failed_tests:
            print(f"   - {test}")
        print("\n💡 These failures indicate the likely source of the error")
    else:
        print("\n🎉 All tests passed!")
        print("💡 The error might be in the actual build process or configuration")
    
    return len(failed_tests) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)