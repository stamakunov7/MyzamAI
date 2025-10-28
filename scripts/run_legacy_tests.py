#!/usr/bin/env python3
"""
Legacy test runner for MyzamAI.

Maintains backward compatibility with existing test scripts
while providing pytest integration.
"""

import subprocess
import sys
import os
import argparse
from typing import List, Optional


def run_legacy_test(script_name: str, description: str) -> bool:
    """
    Run a legacy test script.
    
    Args:
        script_name: Name of the script to run
        description: Description of what's being run
        
    Returns:
        True if test succeeded, False otherwise
    """
    print(f"🚀 {description}")
    print(f"Running: python3 {script_name}")
    print("="*60)
    
    try:
        result = subprocess.run(
            ["python3", script_name],
            check=True,
            capture_output=False,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"🚨 {description} failed with error: {e}")
        return False


def run_simple_test() -> bool:
    """Run simple article test."""
    return run_legacy_test("simple_test.py", "Simple Article Test")


def run_article_accuracy_test() -> bool:
    """Run article accuracy test."""
    return run_legacy_test("tests/test_article_accuracy_simple.py", "Article Accuracy Test")


def run_bot_integration_test() -> bool:
    """Run bot integration test."""
    return run_legacy_test("tests/test_bot_integration.py", "Bot Integration Test")


def run_all_legacy_tests() -> bool:
    """Run all legacy tests."""
    tests = [
        ("simple_test.py", "Simple Article Test"),
        ("tests/test_article_accuracy_simple.py", "Article Accuracy Test"),
        ("tests/test_bot_integration.py", "Bot Integration Test")
    ]
    
    results = []
    for script, description in tests:
        success = run_legacy_test(script, description)
        results.append(success)
        print()  # Add spacing between tests
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("="*60)
    print("📊 LEGACY TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {total - passed}")
    print(f"📈 Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 All legacy tests passed!")
        return True
    else:
        print("❌ Some legacy tests failed!")
        return False


def run_pytest_equivalent() -> bool:
    """Run pytest equivalent of legacy tests."""
    print("🔄 Running pytest equivalent of legacy tests...")
    
    # Run pytest with equivalent markers
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-v"],
            check=True,
            capture_output=False,
            text=True
        )
        print("✅ Pytest equivalent completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Pytest equivalent failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"🚨 Pytest equivalent failed with error: {e}")
        return False


def compare_legacy_vs_pytest() -> bool:
    """Compare legacy tests vs pytest results."""
    print("🔍 Comparing legacy tests vs pytest...")
    
    # Run legacy tests
    print("\n1. Running legacy tests...")
    legacy_success = run_all_legacy_tests()
    
    print("\n2. Running pytest equivalent...")
    pytest_success = run_pytest_equivalent()
    
    print("\n" + "="*60)
    print("📊 COMPARISON RESULTS")
    print("="*60)
    print(f"Legacy Tests: {'✅ PASSED' if legacy_success else '❌ FAILED'}")
    print(f"Pytest Tests: {'✅ PASSED' if pytest_success else '❌ FAILED'}")
    
    if legacy_success and pytest_success:
        print("🎉 Both test suites passed!")
        return True
    elif legacy_success and not pytest_success:
        print("⚠️  Legacy tests passed, but pytest failed")
        return False
    elif not legacy_success and pytest_success:
        print("⚠️  Pytest passed, but legacy tests failed")
        return False
    else:
        print("❌ Both test suites failed!")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="MyzamAI Legacy Test Runner")
    parser.add_argument(
        "test_type",
        choices=[
            "simple", "article-accuracy", "bot-integration", 
            "all", "pytest", "compare"
        ],
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    print("🧪 MyzamAI Legacy Test Runner")
    print("="*60)
    
    success = False
    
    if args.test_type == "simple":
        success = run_simple_test()
    elif args.test_type == "article-accuracy":
        success = run_article_accuracy_test()
    elif args.test_type == "bot-integration":
        success = run_bot_integration_test()
    elif args.test_type == "all":
        success = run_all_legacy_tests()
    elif args.test_type == "pytest":
        success = run_pytest_equivalent()
    elif args.test_type == "compare":
        success = compare_legacy_vs_pytest()
    
    if success:
        print("\n🎉 Tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
