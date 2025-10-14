#!/usr/bin/env python3
"""
CI/CD Integration Verification Script

This script verifies that the CI/CD integration is properly configured
and all components are working correctly.
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")

def check_file_exists(file_path, description):
    """Check if a file exists and print the result."""
    if os.path.exists(file_path):
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description}: {file_path} (NOT FOUND)")
        return False

def check_yaml_syntax(file_path):
    """Check if a YAML file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        print_success(f"YAML syntax valid: {file_path}")
        return True
    except yaml.YAMLError as e:
        print_error(f"YAML syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print_error(f"Error reading {file_path}: {e}")
        return False

def check_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            compile(f.read(), file_path, 'exec')
        print_success(f"Python syntax valid: {file_path}")
        return True
    except SyntaxError as e:
        print_error(f"Python syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print_error(f"Error reading {file_path}: {e}")
        return False

def check_requirements_file(file_path):
    """Check if a requirements file exists and has content."""
    if not os.path.exists(file_path):
        print_error(f"Requirements file not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if content:
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                print_success(f"Requirements file valid: {file_path} ({len(lines)} packages)")
                return True
            else:
                print_error(f"Requirements file is empty: {file_path}")
                return False
    except Exception as e:
        print_error(f"Error reading {file_path}: {e}")
        return False

def check_test_structure():
    """Check if the test structure is properly organized."""
    print_header("Test Structure Verification")
    
    test_dirs = [
        'tests',
        'tests/unit',
        'tests/integration'
    ]
    
    test_files = [
        'tests/conftest.py',
        'tests/unit/test_parser.py',
        'tests/unit/test_matcher.py',
        'tests/unit/test_performance.py',
        'tests/integration/test_article_accuracy.py',
        'tests/integration/test_bot_integration.py'
    ]
    
    all_good = True
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir) and os.path.isdir(test_dir):
            print_success(f"Test directory exists: {test_dir}")
        else:
            print_error(f"Test directory missing: {test_dir}")
            all_good = False
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print_success(f"Test file exists: {test_file}")
            if not check_python_syntax(test_file):
                all_good = False
        else:
            print_error(f"Test file missing: {test_file}")
            all_good = False
    
    return all_good

def check_ci_cd_files():
    """Check if CI/CD files are properly configured."""
    print_header("CI/CD Configuration Verification")
    
    ci_files = [
        '.github/workflows/tests.yml',
        'pytest.ini',
        'requirements-test.txt'
    ]
    
    all_good = True
    
    for ci_file in ci_files:
        if os.path.exists(ci_file):
            print_success(f"CI/CD file exists: {ci_file}")
            
            if ci_file.endswith('.yml'):
                if not check_yaml_syntax(ci_file):
                    all_good = False
            elif ci_file.endswith('.py'):
                if not check_python_syntax(ci_file):
                    all_good = False
            elif ci_file.endswith('.txt'):
                if not check_requirements_file(ci_file):
                    all_good = False
        else:
            print_error(f"CI/CD file missing: {ci_file}")
            all_good = False
    
    return all_good

def check_workflow_content():
    """Check if the GitHub Actions workflow has the required content."""
    print_header("GitHub Actions Workflow Verification")
    
    workflow_file = '.github/workflows/tests.yml'
    if not os.path.exists(workflow_file):
        print_error(f"Workflow file not found: {workflow_file}")
        return False
    
    try:
        with open(workflow_file, 'r') as f:
            content = f.read()
        
        required_elements = [
            'name:',
            'on:',
            'push:',
            'pull_request:',
            'jobs:',
            'test:',
            'runs-on: ubuntu-latest',
            'strategy:',
            'matrix:',
            'python-version:',
            'test-type:',
            'steps:',
            'uses: actions/checkout@v4',
            'uses: actions/setup-python@v5',
            'python -m pytest',
            'coverage:',
            'performance:',
            'security:'
        ]
        
        all_good = True
        for element in required_elements:
            if element in content:
                print_success(f"Workflow contains: {element}")
            else:
                print_error(f"Workflow missing: {element}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print_error(f"Error reading workflow file: {e}")
        return False

def check_pytest_config():
    """Check if pytest configuration is valid."""
    print_header("Pytest Configuration Verification")
    
    config_file = 'pytest.ini'
    if not os.path.exists(config_file):
        print_error(f"Pytest config not found: {config_file}")
        return False
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        required_sections = [
            '[pytest]',
            'markers =',
            'integration:',
            'unit:'
        ]
        
        all_good = True
        for section in required_sections:
            if section in content:
                print_success(f"Config contains: {section}")
            else:
                print_error(f"Config missing: {section}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print_error(f"Error reading pytest config: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available."""
    print_header("Dependencies Verification")
    
    # Check if requirements files exist
    req_files = ['requirements.txt', 'requirements-test.txt']
    all_good = True
    
    for req_file in req_files:
        if not check_requirements_file(req_file):
            all_good = False
    
    # Check if pytest is available
    try:
        result = subprocess.run(['python3', '-c', 'import pytest'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("pytest is available")
        else:
            print_error("pytest is not available")
            all_good = False
    except Exception as e:
        print_error(f"Error checking pytest: {e}")
        all_good = False
    
    return all_good

def run_quick_test():
    """Run a quick test to verify everything works."""
    print_header("Quick Test Execution")
    
    try:
        # Try to run pytest with help to verify it works
        result = subprocess.run(['python3', '-m', 'pytest', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_success("pytest is working correctly")
            return True
        else:
            print_error(f"pytest failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("pytest test timed out")
        return False
    except Exception as e:
        print_error(f"Error running pytest: {e}")
        return False

def main():
    """Main verification function."""
    print_header("MyzamAI CI/CD Integration Verification")
    print_info("Verifying CI/CD integration setup...")
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print_info(f"Working directory: {os.getcwd()}")
    
    # Run all checks
    checks = [
        ("Test Structure", check_test_structure),
        ("CI/CD Files", check_ci_cd_files),
        ("Workflow Content", check_workflow_content),
        ("Pytest Config", check_pytest_config),
        ("Dependencies", check_dependencies),
        ("Quick Test", run_quick_test)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_error(f"Error in {check_name}: {e}")
            results[check_name] = False
    
    # Print summary
    print_header("Verification Summary")
    
    all_passed = True
    for check_name, passed in results.items():
        if passed:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
            all_passed = False
    
    print_header("Final Result")
    if all_passed:
        print_success("🎉 All CI/CD integration checks PASSED!")
        print_info("Your CI/CD integration is ready to use.")
        print_info("Push to GitHub to trigger the workflow.")
    else:
        print_error("❌ Some CI/CD integration checks FAILED!")
        print_info("Please fix the issues above before using CI/CD.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
