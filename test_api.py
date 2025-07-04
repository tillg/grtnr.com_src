#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add extensions to path
sys.path.insert(0, 'extensions')

try:
    from dotenv import load_dotenv
    load_dotenv()
    print(f"✅ Loaded .env file")
except ImportError:
    print("❌ python-dotenv not available")

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ No API key found in environment")
    print("Environment variables:")
    for key in os.environ:
        if "OPENAI" in key or "TRANSLATION" in key:
            print(f"  {key}={os.environ[key]}")

# Test translation service
try:
    from translation_service import TranslationService, TranslationConfig
    
    print("\n🔧 Testing configuration...")
    config = TranslationConfig.from_environment()
    print(f"✅ Config loaded: {config}")
    
    print("\n🚀 Testing translation service...")
    service = TranslationService(config)
    
    # Simple test translation
    result = service.translate_content(
        content="Hello, world! This is a test.",
        source_lang="en",
        target_lang="de"
    )
    
    print(f"✅ Translation successful!")
    print(f"Original: Hello, world! This is a test.")
    print(f"German: {result.translation}")
    print(f"Cached: {result.cached}")
    
except Exception as e:
    print(f"❌ Translation test failed: {e}")
    import traceback
    traceback.print_exc()