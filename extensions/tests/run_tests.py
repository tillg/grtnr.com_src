#!/usr/bin/env python3

import os
import sys
import unittest
from pathlib import Path

# Add the extensions directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""

    # Get the tests directory
    tests_dir = os.path.dirname(__file__)

    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover all test files
    test_files = [
        f for f in os.listdir(tests_dir) if f.startswith("test_") and f.endswith(".py")
    ]

    print(f"🔍 Discovered {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file}")

    # Load tests from each file
    for test_file in test_files:
        try:
            module_name = test_file[:-3]  # Remove .py extension
            spec = __import__(module_name)

            # Add tests to suite
            file_suite = loader.loadTestsFromModule(spec)
            suite.addTest(file_suite)

        except Exception as e:
            print(f"⚠️  Could not load {test_file}: {e}")

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_manual_translation_tests():
    """Run manual translation tests for quality assessment"""

    try:
        from test_translation_service import TranslationTestRunner

        print("🚀 Running manual translation quality tests...")

        runner = TranslationTestRunner()
        success = runner.run_full_test_suite()

        if success:
            print("\n✅ Manual translation tests completed successfully")
            print("📖 Review the generated report in extensions/tests/output/")
        else:
            print("\n⚠️  Manual translation tests completed with issues")
            print("📖 Check the generated report for details")

        return success

    except Exception as e:
        print(f"❌ Manual translation tests failed: {e}")
        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Translation Service Test Runner")
    parser.add_argument(
        "--manual", action="store_true", help="Run manual translation quality tests"
    )
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")

    args = parser.parse_args()

    success = True

    if args.all or args.unit:
        print("🧪 Running unit tests...")
        success &= discover_and_run_tests()

    if args.all or args.manual:
        print("\n🎯 Running manual translation tests...")
        success &= run_manual_translation_tests()

    if not any([args.unit, args.manual, args.all]):
        print("No test type specified. Use --help for options.")
        print("Available options:")
        print("  --unit    Run unit tests")
        print("  --manual  Run manual translation quality tests")
        print("  --all     Run all tests")
        return False

    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Check the output above.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
