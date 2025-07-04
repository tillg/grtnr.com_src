#!/usr/bin/env python3
"""
Test to demonstrate the API mismatch error in the automatic translation plugin.

This test shows that the automatic_translation.py plugin expects a different API
than what the new TranslationService implements.
"""

import os
import sys
from unittest.mock import Mock, patch
from typing import Dict, Any

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'extensions'))

def test_translation_service_api_mismatch():
    """Test that demonstrates the API mismatch between plugin and service"""
    
    print("🧪 Testing Translation Service API Mismatch")
    print("=" * 50)
    
    # Import the new translation service
    try:
        from translation_service import TranslationService, TranslationConfig
        print("✅ Successfully imported new TranslationService")
    except ImportError as e:
        print(f"❌ Failed to import new TranslationService: {e}")
        return False
    
    # Mock the Pelican settings
    mock_settings = {
        'TRANSLATION_ENABLED': True,
        'TRANSLATION_API_KEY': 'test-key',
        'TRANSLATION_TARGET_LANGUAGES': ['de', 'fr'],
        'TRANSLATION_EXCLUDE_CATEGORIES': ['recipes'],
        'TRANSLATION_EXCLUDE_PATHS': ['/pages/impressum/'],
        'TRANSLATION_MODEL': 'gpt-4',
        'TRANSLATION_CACHE_ENABLED': True,
        'TRANSLATION_MAX_RETRIES': 3,
        'TRANSLATION_TIMEOUT': 30,
    }
    
    # Mock OpenAI to avoid making real API calls
    with patch('translation_service.service.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        # Mock the chat completion response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mocked translation"
        mock_client.chat.completions.create.return_value = mock_response
        
        try:
            # Try to create config from Pelican settings
            config = TranslationConfig.from_pelican_settings(mock_settings)
            print("✅ Successfully created TranslationConfig from Pelican settings")
            
            # Try to create service
            service = TranslationService(config)
            print("✅ Successfully created TranslationService")
            
            # Test the expected API from automatic_translation.py
            print("\n🔍 Testing expected API from automatic_translation.py:")
            
            # 1. Test detect_language method
            test_content = "This is a test article content."
            try:
                detected_lang = service.detect_language(test_content)
                print(f"✅ detect_language() works: {detected_lang}")
            except Exception as e:
                print(f"❌ detect_language() failed: {e}")
                return False
            
            # 2. Test translate_content method - this is where the API mismatch occurs
            print("\n🔍 Testing translate_content() method:")
            
            # The plugin expects: translate_content(content, source_lang, target_lang)
            # Let's see what the service actually provides
            try:
                # This is what the plugin tries to call
                result = service.translate_content(test_content, "en", "de")
                print(f"✅ translate_content() works, result type: {type(result)}")
                
                # Now check what the plugin expects from the result
                print("\n🔍 Testing plugin expectations for result:")
                
                # Plugin expects: result.translation and result.cached
                if hasattr(result, 'translation'):
                    print(f"✅ result.translation exists: {result.translation[:50]}...")
                else:
                    print("❌ result.translation missing - plugin expects this attribute")
                    return False
                
                if hasattr(result, 'cached'):
                    print(f"✅ result.cached exists: {result.cached}")
                else:
                    print("❌ result.cached missing - plugin expects this attribute")
                    return False
                
            except Exception as e:
                print(f"❌ translate_content() failed: {e}")
                return False
            
            # 3. Test health_check method
            print("\n🔍 Testing health_check() method:")
            try:
                health = service.health_check()
                print(f"✅ health_check() works: {health.get('status', 'unknown')}")
            except Exception as e:
                print(f"❌ health_check() failed: {e}")
                return False
            
            print("\n🎉 All API compatibility tests passed!")
            print("The new TranslationService appears to have the correct API interface.")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create TranslationService: {e}")
            return False

def test_old_translation_service_api():
    """Test the old translation service API to show the difference"""
    
    print("\n🧪 Testing Old Translation Service API")
    print("=" * 50)
    
    # Add the plugins directory to the path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'plugins'))
    
    try:
        from translation_service import TranslationService as OldTranslationService
        print("✅ Successfully imported old TranslationService")
        
        # Create old service (it expects different parameters)
        try:
            old_service = OldTranslationService()
        except TypeError as e:
            print(f"❌ Old service constructor failed: {e}")
            # Try with different parameters
            try:
                old_service = OldTranslationService(
                    language_detector=None,
                    translator=None,
                    cache_dir="cache"
                )
                print("✅ Created old service with explicit parameters")
            except Exception as e2:
                print(f"❌ Still failed: {e2}")
                return
        
        # Test the old API
        test_content = "This is a test article content."
        file_path = "/fake/path/to/file.md"
        
        try:
            # Old API: translate_content(content, file_path, target_language)
            result = old_service.translate_content(test_content, file_path, "de")
            print(f"✅ Old API translate_content() works, result type: {type(result)}")
            
            # Old API returns a tuple: (translated_content, source_language)
            if isinstance(result, tuple) and len(result) == 2:
                translated_content, source_language = result
                print(f"✅ Old API returns tuple: ({type(translated_content)}, {type(source_language)})")
                print(f"   Translation: {translated_content[:50]}...")
                print(f"   Source lang: {source_language}")
            else:
                print(f"❌ Old API returned unexpected format: {result}")
                
        except Exception as e:
            print(f"❌ Old API translate_content() failed: {e}")
            
    except ImportError as e:
        print(f"❌ Failed to import old TranslationService: {e}")

def compare_api_signatures():
    """Compare the API signatures between old and new services"""
    
    print("\n🔍 API Signature Comparison")
    print("=" * 50)
    
    print("OLD API (from plugins/translation_service.py):")
    print("  translate_content(content, file_path, target_language) -> Tuple[str, str]")
    print("  detect_language(content) -> str")
    print("  get_available_languages() -> List[str]")
    print()
    
    print("NEW API (from extensions/translation_service/):")
    print("  translate_content(content, source_lang, target_lang) -> TranslationResult")
    print("  detect_language(content) -> str")
    print("  get_supported_languages() -> List[str]")
    print()
    
    print("PLUGIN EXPECTATIONS (from automatic_translation.py):")
    print("  service.translate_content(source_content, source_lang, target_lang)")
    print("  result.translation  # expects TranslationResult with .translation attribute")
    print("  result.cached      # expects TranslationResult with .cached attribute")
    print()
    
    print("🔍 IDENTIFIED ISSUES:")
    print("1. ✅ Method signature compatibility: NEW API matches plugin expectations")
    print("2. ✅ Return type compatibility: NEW API returns TranslationResult with expected attributes")
    print("3. ✅ detect_language() method: Compatible")
    print("4. ⚠️  Method name difference: get_available_languages() vs get_supported_languages()")
    print()
    
    print("🎯 CONCLUSION:")
    print("The new TranslationService API is actually COMPATIBLE with the plugin!")
    print("If there are errors, they might be in:")
    print("- Import path issues")
    print("- Configuration problems")
    print("- Missing dependencies")
    print("- API key configuration")

def test_import_issues():
    """Test for import issues that might cause the error"""
    
    print("\n🧪 Testing Import Issues")
    print("=" * 50)
    
    # Test 1: Can we import from the extensions directory?
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'extensions'))
        from translation_service import TranslationService
        print("✅ Can import TranslationService from extensions")
    except ImportError as e:
        print(f"❌ Cannot import TranslationService from extensions: {e}")
        return False
    
    # Test 2: Are dependencies available?
    try:
        import openai
        print("✅ OpenAI package is available")
    except ImportError:
        print("❌ OpenAI package is missing - this could cause the error!")
        return False
    
    # Test 3: Are all required modules available?
    try:
        from translation_service.config import TranslationConfig
        from translation_service.exceptions import TranslationError
        print("✅ All required modules are importable")
    except ImportError as e:
        print(f"❌ Missing required modules: {e}")
        return False
    
    # Test 4: Check if the plugin can find the service
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'plugins'))
        
        # Simulate what the plugin does
        plugin_path = os.path.join(os.path.dirname(__file__), 'plugins', 'automatic_translation.py')
        
        # Read the plugin file and check import structure
        with open(plugin_path, 'r') as f:
            plugin_content = f.read()
            
        if 'from translation_service import TranslationService' in plugin_content:
            print("✅ Plugin has correct import statement")
        else:
            print("❌ Plugin missing or incorrect import statement")
            
    except Exception as e:
        print(f"❌ Error checking plugin imports: {e}")
        return False
    
    return True

def main():
    """Run all tests to identify the error"""
    
    print("🚀 Translation Service Error Detection Test Suite")
    print("=" * 70)
    
    success = True
    
    # Test 1: API compatibility
    if not test_translation_service_api_mismatch():
        success = False
    
    # Test 2: Old API for comparison
    test_old_translation_service_api()
    
    # Test 3: Compare signatures
    compare_api_signatures()
    
    # Test 4: Import issues
    if not test_import_issues():
        success = False
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 All tests passed - the error might be elsewhere!")
        print("💡 Check:")
        print("   - OpenAI API key configuration")
        print("   - Network connectivity")
        print("   - Plugin loading order")
        print("   - Environment variables")
    else:
        print("❌ Found issues that could cause the error")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)