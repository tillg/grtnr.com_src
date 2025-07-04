#!/usr/bin/env python3
"""
Test to demonstrate the Pelican integration error in the automatic translation plugin.

This test shows the actual issue with the plugin's integration with Pelican.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the plugins directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'plugins'))

def test_pelican_generator_requirements():
    """Test what Pelican Generator class requires"""
    
    print("🧪 Testing Pelican Generator Requirements")
    print("=" * 60)
    
    try:
        # Import Pelican's Generator class
        from pelican.generators import Generator
        print("✅ Successfully imported Pelican Generator")
        
        # Check what the Generator __init__ expects
        import inspect
        sig = inspect.signature(Generator.__init__)
        print(f"✅ Generator.__init__ signature: {sig}")
        
        # List required parameters
        required_params = []
        for param_name, param in sig.parameters.items():
            if param.default == inspect.Parameter.empty and param_name != 'self':
                required_params.append(param_name)
        
        print(f"✅ Required parameters: {required_params}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to analyze Pelican Generator: {e}")
        return False

def test_minimal_pelican_settings():
    """Test with minimal Pelican settings"""
    
    print("\n🧪 Testing Minimal Pelican Settings")
    print("=" * 60)
    
    try:
        # Create minimal Pelican settings
        minimal_settings = {
            'TRANSLATION_ENABLED': True,
            'TRANSLATION_TARGET_LANGUAGES': ['de', 'fr'],
            'TRANSLATION_EXCLUDE_CATEGORIES': ['recipes'],
            'TRANSLATION_EXCLUDE_PATHS': ['/pages/impressum/'],
            'TRANSLATION_MODEL': 'gpt-4',
            'TRANSLATION_CACHE_ENABLED': True,
            'TRANSLATION_MAX_RETRIES': 3,
            'TRANSLATION_TIMEOUT': 30,
            'TRANSLATION_API_KEY': 'test-key',
            
            # Add required Pelican settings
            'READERS': {},
            'STATIC_PATHS': [],
            'THEME': 'simple',
            'PATH': 'content',
            'CACHE_CONTENT': False,
            'CACHE_PATH': '.cache',
            'IGNORE_FILES': [],
            'DELETE_OUTPUT_DIRECTORY': False,
            'OUTPUT_SOURCES': False,
            'OUTPUT_SOURCES_EXTENSION': '.text',
            'USE_FOLDER_AS_CATEGORY': True,
            'DISPLAY_CATEGORIES_ON_MENU': True,
            'DISPLAY_PAGES_ON_MENU': True,
            'DEFAULT_CATEGORY': 'misc',
            'WITH_FUTURE_DATES': True,
            'INTRASITE_LINK_REGEX': r'[{|](?P<what>.*?)[|}]',
            'PYGMENTS_RST_OPTIONS': {},
            'SLUG_REGEX_SUBSTITUTIONS': [],
            'ARTICLE_URL': 'posts/{slug}.html',
            'ARTICLE_SAVE_AS': 'posts/{slug}.html',
            'ARTICLE_LANG_URL': 'posts/{slug}-{lang}.html',
            'ARTICLE_LANG_SAVE_AS': 'posts/{slug}-{lang}.html',
            'DRAFT_URL': 'drafts/{slug}.html',
            'DRAFT_SAVE_AS': 'drafts/{slug}.html',
            'DRAFT_LANG_URL': 'drafts/{slug}-{lang}.html',
            'DRAFT_LANG_SAVE_AS': 'drafts/{slug}-{lang}.html',
            'PAGE_URL': 'pages/{slug}.html',
            'PAGE_SAVE_AS': 'pages/{slug}.html',
            'PAGE_LANG_URL': 'pages/{slug}-{lang}.html',
            'PAGE_LANG_SAVE_AS': 'pages/{slug}-{lang}.html',
            'CATEGORY_URL': 'category/{slug}.html',
            'CATEGORY_SAVE_AS': 'category/{slug}.html',
            'TAG_URL': 'tag/{slug}.html',
            'TAG_SAVE_AS': 'tag/{slug}.html',
            'AUTHOR_URL': 'author/{slug}.html',
            'AUTHOR_SAVE_AS': 'author/{slug}.html',
            'YEAR_ARCHIVE_SAVE_AS': '',
            'MONTH_ARCHIVE_SAVE_AS': '',
            'DAY_ARCHIVE_SAVE_AS': '',
            'RELATIVE_URLS': False,
            'DEFAULT_LANG': 'en',
            'TIMEZONE': 'UTC',
            'DATE_FORMATS': {},
            'LOCALE': ('C',),
            'DEFAULT_DATE_FORMAT': '%a %d %B %Y',
            'FEED_DOMAIN': None,
            'FEED_ATOM': None,
            'FEED_RSS': None,
            'FEED_ALL_ATOM': None,
            'FEED_ALL_RSS': None,
            'CATEGORY_FEED_ATOM': None,
            'CATEGORY_FEED_RSS': None,
            'AUTHOR_FEED_ATOM': None,
            'AUTHOR_FEED_RSS': None,
            'TAG_FEED_ATOM': None,
            'TAG_FEED_RSS': None,
            'TRANSLATION_FEED_ATOM': None,
            'TRANSLATION_FEED_RSS': None,
            'FEED_MAX_ITEMS': '',
            'SITEURL': '',
            'SITENAME': 'Test Site',
            'SITESUBTITLE': '',
            'SITEDESCRIPTION': '',
            'BIO': '',
            'BANNER': '',
            'BANNER_ALL_PAGES': False,
            'BANNER_SUBTITLE': '',
            'DISPLAY_ARTICLE_INFO_ON_INDEX': False,
            'FAVICON': '',
            'FAVICON_IE': '',
            'TOUCHICON': '',
            'APPLE_TOUCH_ICON': '',
            'APPLE_TOUCH_ICON_SIZE': '',
            'SHARIFF': False,
            'SHARIFF_BACKEND_URL': '',
            'SHARIFF_LANG': 'en',
            'SHARIFF_ORIENTATION': 'horizontal',
            'SHARIFF_SERVICES': [],
            'SHARIFF_THEME': 'color',
            'SHARIFF_TWITTER_VIA': '',
            'SITELOGO': '',
            'SITELOGO_SIZE': '',
            'HIDE_SITENAME': False,
            'CUSTOM_CSS': '',
            'CUSTOM_JS': '',
            'SOCIAL': (),
            'LINKS': (),
            'MENUITEMS': (),
            'NEWEST_FIRST_ARCHIVES': True,
            'REVERSE_CATEGORY_ORDER': False,
            'DISPLAY_PAGES_ON_MENU': True,
            'DISPLAY_CATEGORIES_ON_MENU': True,
            'DOCUTIL_CSS': False,
            'TYPOGRIFY': False,
            'TYPOGRIFY_IGNORE_TAGS': [],
            'TYPOGRIFY_DASHES': 'default',
            'DIRECT_TEMPLATES': ['index', 'tags', 'categories', 'archives'],
            'PAGINATED_TEMPLATES': {
                'index': None,
                'tag': None,
                'category': None,
                'author': None,
            },
            'TEMPLATE_PAGES': {},
            'TEMPLATE_EXTENSIONS': ['.html'],
            'THEME_TEMPLATES_OVERRIDES': [],
            'CSS_FILE': 'main.css',
            'LOAD_CONTENT_CACHE': False,
            'CHECK_MODIFIED_METHOD': 'mtime',
            'CONTENT_CACHING_LAYER': 'reader',
            'GZIP_CACHE': True,
            'AUTORELOAD_IGNORE_CACHE': False,
            'WRITE_SELECTED': [],
            'FORMATTED_FIELDS': ['summary'],
            'SUMMARY_MAX_LENGTH': 50,
            'PLUGIN_PATHS': [],
            'PLUGINS': [],
            'LOG_FILTER': [],
            'MARKDOWN': {
                'extensions': ['codehilite', 'extra'],
                'extension_configs': {
                    'codehilite': {'css_class': 'highlight'},
                    'extra': {},
                },
                'output_format': 'html5',
            },
            'JINJA_ENVIRONMENT': {},
            'JINJA_FILTERS': {},
            'JINJA_GLOBALS': {},
            'JINJA_TESTS': {},
        }
        
        print(f"✅ Created minimal settings with {len(minimal_settings)} keys")
        
        # Test creating the generator with these settings
        from automatic_translation import TranslationGenerator
        
        mock_context = {'articles': [], 'pages': []}
        
        generator = TranslationGenerator(
            context=mock_context,
            settings=minimal_settings,
            path="content",
            theme="simple",
            output_path="output"
        )
        
        print("✅ Successfully created TranslationGenerator with minimal settings")
        
        if generator.translation_service:
            print("✅ Translation service initialized")
        else:
            print("❌ Translation service not initialized")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Failed with minimal settings: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plugin_duplicate_issue():
    """Test for the plugin duplicate issue"""
    
    print("\n🧪 Testing Plugin Duplicate Issue")
    print("=" * 60)
    
    # Check if there are conflicting files
    plugins_dir = Path(__file__).parent / "plugins"
    
    automatic_translation_file = plugins_dir / "automatic_translation.py"
    translation_service_file = plugins_dir / "translation_service.py"
    
    print(f"✅ automatic_translation.py exists: {automatic_translation_file.exists()}")
    print(f"✅ translation_service.py exists: {translation_service_file.exists()}")
    
    if both_exist := (automatic_translation_file.exists() and translation_service_file.exists()):
        print("❌ Both files exist - this creates a conflict!")
        print("💡 The plugin tries to import TranslationService, but there are TWO modules with that name:")
        print("   1. plugins/translation_service.py (old service)")
        print("   2. extensions/translation_service/ (new service)")
        
        # Show which one gets imported
        try:
            sys.path.insert(0, str(plugins_dir))
            from translation_service import TranslationService
            
            # Check if it's the old or new service
            import inspect
            source_file = inspect.getfile(TranslationService)
            print(f"   Currently imports from: {source_file}")
            
            # Check the API
            if hasattr(TranslationService, 'translate_content'):
                sig = inspect.signature(TranslationService.translate_content)
                print(f"   translate_content signature: {sig}")
                
                # This reveals the issue!
                params = list(sig.parameters.keys())
                if 'config' in params:
                    print("   🔍 Uses NEW service API (requires config)")
                elif 'file_path' in params:
                    print("   🔍 Uses OLD service API (requires file_path)")
                else:
                    print("   🔍 Unknown API signature")
        except Exception as e:
            print(f"   Import failed: {e}")
            
        return False
    else:
        print("✅ No file conflict detected")
        return True

def test_import_resolution():
    """Test import resolution to show the actual error"""
    
    print("\n🧪 Testing Import Resolution")
    print("=" * 60)
    
    # Show the exact import path resolution
    print("Current sys.path entries:")
    for i, path in enumerate(sys.path):
        if 'grtnr.com_src' in path:
            print(f"  {i}: {path}")
    
    # Test importing from different locations
    print("\nTesting imports from different locations:")
    
    # 1. From plugins directory
    try:
        plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
        if plugins_path not in sys.path:
            sys.path.insert(0, plugins_path)
        
        from translation_service import TranslationService as PluginService
        print("✅ Can import from plugins/ directory")
        
        # Check the signature
        import inspect
        sig = inspect.signature(PluginService.__init__)
        print(f"   __init__ signature: {sig}")
        
    except Exception as e:
        print(f"❌ Cannot import from plugins/: {e}")
    
    # 2. From extensions directory
    try:
        extensions_path = os.path.join(os.path.dirname(__file__), 'extensions')
        if extensions_path not in sys.path:
            sys.path.insert(0, extensions_path)
        
        from translation_service import TranslationService as ExtensionService
        print("✅ Can import from extensions/ directory")
        
        # Check the signature
        import inspect
        sig = inspect.signature(ExtensionService.__init__)
        print(f"   __init__ signature: {sig}")
        
    except Exception as e:
        print(f"❌ Cannot import from extensions/: {e}")
    
    # This shows the ROOT CAUSE of the error!
    print("\n🔍 ROOT CAUSE ANALYSIS:")
    print("The automatic_translation.py plugin does:")
    print("  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'extensions'))")
    print("  from translation_service import TranslationService")
    print("")
    print("But BOTH locations have a 'translation_service' module:")
    print("  1. plugins/translation_service.py (old API)")
    print("  2. extensions/translation_service/ (new API)")
    print("")
    print("Python imports the FIRST one it finds in sys.path!")
    print("If plugins/ is in sys.path before extensions/, it imports the old API.")
    print("The plugin expects the new API, causing the error.")
    
    return True

def main():
    """Run all tests to demonstrate the Pelican integration error"""
    
    print("🚀 Pelican Integration Error Detection Test Suite")
    print("=" * 80)
    
    tests = [
        ("Pelican Generator Requirements", test_pelican_generator_requirements),
        ("Minimal Pelican Settings", test_minimal_pelican_settings),
        ("Plugin Duplicate Issue", test_plugin_duplicate_issue),
        ("Import Resolution", test_import_resolution),
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
    
    print("\n" + "=" * 80)
    print("🎯 IDENTIFIED ERROR:")
    print("=" * 80)
    
    if any("Plugin Duplicate Issue" in name for name, passed in results if not passed):
        print("❌ DUPLICATE MODULE CONFLICT")
        print("The error is caused by having TWO 'translation_service' modules:")
        print("  1. plugins/translation_service.py (old API)")
        print("  2. extensions/translation_service/ (new API)")
        print("")
        print("The plugin expects the new API but may import the old one.")
        print("")
        print("🔧 SOLUTION:")
        print("Remove or rename plugins/translation_service.py to avoid the conflict.")
    else:
        print("✅ No duplicate module conflict detected")
        
    if failed_tests:
        print(f"\n❌ {len(failed_tests)} test(s) failed, indicating integration issues")
    else:
        print("\n🎉 All integration tests passed!")
    
    return len(failed_tests) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)