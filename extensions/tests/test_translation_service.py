#!/usr/bin/env python3

import os
import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import Mock, patch

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from translation_service import TranslationService, TranslationConfig, TranslationCache
    from translation_service.exceptions import TranslationError, APIError
except ImportError:
    # Mock classes for testing before implementation
    class TranslationService:
        def __init__(self, api_key: str, model: str = "gpt-4"):
            self.api_key = api_key
            self.model = model
            
        def translate_content(self, content: str, source_lang: str, target_lang: str) -> str:
            return f"MOCK TRANSLATION: {content[:50]}..."
            
        def detect_language(self, content: str) -> str:
            return "en"
            
        def get_supported_languages(self) -> List[str]:
            return ["en", "de", "fr", "es", "it"]
    
    class TranslationConfig:
        def __init__(self):
            self.api_key = "test-key"
            self.model = "gpt-4"
            self.target_languages = ["de", "fr", "es"]
            self.cache_enabled = True
            
    class TranslationCache:
        def __init__(self, cache_dir: str):
            self.cache_dir = cache_dir
            
        def get_cached_translation(self, content_hash: str, target_lang: str) -> Optional[str]:
            return None
            
        def cache_translation(self, content_hash: str, target_lang: str, translation: str):
            pass
    
    class TranslationError(Exception):
        pass
        
    class APIError(TranslationError):
        pass


class TranslationTestRunner:
    """Test runner for translation quality assessment"""
    
    def __init__(self, test_dir: str = None):
        self.test_dir = test_dir or os.path.dirname(__file__)
        self.fixtures_dir = os.path.join(self.test_dir, "fixtures")
        self.output_dir = os.path.join(self.test_dir, "output")
        self.expected_dir = os.path.join(self.fixtures_dir, "expected_translations")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Test configuration
        self.config = TranslationConfig()
        self.service = TranslationService(self.config)
        
    def run_sample_translations(self) -> Dict[str, Dict[str, str]]:
        """Translate sample content for human review"""
        print("🚀 Running sample translations...")
        
        results = {}
        
        # Get all sample files
        sample_files = [
            f for f in os.listdir(self.fixtures_dir) 
            if f.startswith("sample_") and f.endswith(".md")
        ]
        
        for sample_file in sample_files:
            print(f"\n📄 Processing {sample_file}")
            
            # Read sample content
            sample_path = os.path.join(self.fixtures_dir, sample_file)
            with open(sample_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Detect source language
            source_lang = self.service.detect_language(content)
            print(f"   Detected language: {source_lang}")
            
            # Translate to each target language
            translations = {}
            for target_lang in self.config.target_languages:
                print(f"   Translating to {target_lang}...")
                
                try:
                    translation = self.service.translate_content(
                        content, source_lang, target_lang
                    )
                    translations[target_lang] = translation
                    
                    # Save translation to output directory
                    output_filename = f"{sample_file.replace('.md', '')}_{target_lang.upper()}.md"
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(translation)
                    
                    print(f"   ✅ Saved to {output_filename}")
                    
                except Exception as e:
                    print(f"   ❌ Translation failed: {e}")
                    translations[target_lang] = f"ERROR: {str(e)}"
            
            results[sample_file] = translations
        
        return results
    
    def generate_comparison_report(self, results: Dict[str, Dict[str, str]]) -> str:
        """Generate side-by-side comparison report"""
        print("\n📊 Generating comparison report...")
        
        report_lines = []
        report_lines.append("# Translation Quality Assessment Report")
        report_lines.append("")
        report_lines.append("This report contains sample translations for manual review.")
        report_lines.append("")
        
        for sample_file, translations in results.items():
            report_lines.append(f"## {sample_file}")
            report_lines.append("")
            
            # Read original content
            original_path = os.path.join(self.fixtures_dir, sample_file)
            with open(original_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            report_lines.append("### Original Content")
            report_lines.append("```markdown")
            report_lines.append(original_content)
            report_lines.append("```")
            report_lines.append("")
            
            # Add translations
            for lang, translation in translations.items():
                report_lines.append(f"### Translation ({lang.upper()})")
                report_lines.append("```markdown")
                report_lines.append(translation)
                report_lines.append("```")
                report_lines.append("")
        
        # Add evaluation criteria
        report_lines.append("## Evaluation Criteria")
        report_lines.append("")
        report_lines.append("When reviewing translations, please check:")
        report_lines.append("")
        report_lines.append("1. **Markdown Structure**: Are headers, lists, and formatting preserved?")
        report_lines.append("2. **WikiLinks**: Are [[Page Name]] links properly translated?")
        report_lines.append("3. **Code Blocks**: Are code examples left untranslated?")
        report_lines.append("4. **Technical Terms**: Are technical terms handled appropriately?")
        report_lines.append("5. **Natural Language**: Does the translation read naturally?")
        report_lines.append("6. **Image Alt Text**: Are image descriptions translated?")
        report_lines.append("7. **Metadata**: Is front matter preserved untranslated?")
        report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save report
        report_path = os.path.join(self.output_dir, "translation_comparison_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Report saved to {report_path}")
        return report_path
    
    def validate_translation_quality(self, results: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
        """Run automated quality checks"""
        print("\n🔍 Running automated quality checks...")
        
        issues = {}
        
        for sample_file, translations in results.items():
            file_issues = []
            
            # Read original content
            original_path = os.path.join(self.fixtures_dir, sample_file)
            with open(original_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            for lang, translation in translations.items():
                if translation.startswith("ERROR:"):
                    file_issues.append(f"{lang}: Translation failed")
                    continue
                
                # Check for markdown structure preservation
                original_headers = original_content.count('#')
                translated_headers = translation.count('#')
                if original_headers != translated_headers:
                    file_issues.append(f"{lang}: Header count mismatch ({original_headers} vs {translated_headers})")
                
                # Check for code block preservation
                original_code_blocks = original_content.count('```')
                translated_code_blocks = translation.count('```')
                if original_code_blocks != translated_code_blocks:
                    file_issues.append(f"{lang}: Code block count mismatch ({original_code_blocks} vs {translated_code_blocks})")
                
                # Check for WikiLinks preservation
                original_wikilinks = original_content.count('[[')
                translated_wikilinks = translation.count('[[')
                if original_wikilinks != translated_wikilinks:
                    file_issues.append(f"{lang}: WikiLink count mismatch ({original_wikilinks} vs {translated_wikilinks})")
                
                # Check for image preservation
                original_images = original_content.count('![')
                translated_images = translation.count('![')
                if original_images != translated_images:
                    file_issues.append(f"{lang}: Image count mismatch ({original_images} vs {translated_images})")
            
            if file_issues:
                issues[sample_file] = file_issues
        
        # Print results
        if issues:
            print("❌ Quality issues found:")
            for file, file_issues in issues.items():
                print(f"  {file}:")
                for issue in file_issues:
                    print(f"    - {issue}")
        else:
            print("✅ No quality issues detected")
        
        return issues
    
    def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        print("🧪 Running Translation Service Test Suite")
        print("=" * 50)
        
        try:
            # Run translations
            results = self.run_sample_translations()
            
            # Generate report
            report_path = self.generate_comparison_report(results)
            
            # Run quality checks
            issues = self.validate_translation_quality(results)
            
            # Summary
            print("\n" + "=" * 50)
            print("📈 Test Suite Summary")
            print(f"✅ Translations completed: {len(results)}")
            print(f"📊 Comparison report: {report_path}")
            print(f"🔍 Quality issues: {len(issues)}")
            
            if issues:
                print("\n⚠️  Manual review recommended due to quality issues")
                return False
            else:
                print("\n🎉 All automated checks passed!")
                return True
                
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
            return False


def main():
    """Main entry point for running translation tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Translation Service Test Runner")
    parser.add_argument("--test-dir", help="Directory containing test fixtures")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = TranslationTestRunner(args.test_dir)
    
    # Run test suite
    success = runner.run_full_test_suite()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()