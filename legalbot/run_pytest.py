#!/usr/bin/env python3
"""
Pytest runner script for MyzamAI.

Provides convenient commands for running different types of tests.
"""

import subprocess
import sys
import os
import argparse
from typing import List, Optional


def run_command(command: List[str], description: str) -> bool:
    """
    Run a command and return success status.
    
    Args:
        command: Command to run
        description: Description of what's being run
        
    Returns:
        True if command succeeded, False otherwise
    """
    print(f"🚀 {description}")
    print(f"Command: {' '.join(command)}")
    print("="*60)
    
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"🚨 {description} failed with error: {e}")
        return False


def run_unit_tests(verbose: bool = False) -> bool:
    """Run unit tests."""
    command = ["python", "-m", "pytest", "tests/unit/", "-m", "unit"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running unit tests")


def run_integration_tests(verbose: bool = False) -> bool:
    """Run integration tests."""
    command = ["python", "-m", "pytest", "tests/integration/", "-m", "integration"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running integration tests")


def run_article_tests(verbose: bool = False) -> bool:
    """Run article-specific tests."""
    command = ["python", "-m", "pytest", "-m", "article"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running article tests")


def run_performance_tests(verbose: bool = False) -> bool:
    """Run performance tests."""
    command = ["python", "-m", "pytest", "-m", "performance"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running performance tests")


def run_all_tests(verbose: bool = False, coverage: bool = False) -> bool:
    """Run all tests."""
    command = ["python", "-m", "pytest", "tests/"]
    if verbose:
        command.append("-v")
    if coverage:
        command.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    return run_command(command, "Running all tests")


def run_quick_tests(verbose: bool = False) -> bool:
    """Run quick tests (exclude slow tests)."""
    command = ["python", "-m", "pytest", "tests/", "-m", "not slow"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running quick tests")


def run_slow_tests(verbose: bool = False) -> bool:
    """Run slow tests."""
    command = ["python", "-m", "pytest", "-m", "slow"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running slow tests")


def run_with_coverage(verbose: bool = False) -> bool:
    """Run tests with coverage reporting."""
    command = [
        "python", "-m", "pytest", "tests/",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term",
        "--cov-report=xml"
    ]
    if verbose:
        command.append("-v")
    return run_command(command, "Running tests with coverage")


def run_parallel_tests(verbose: bool = False, num_workers: int = 4) -> bool:
    """Run tests in parallel."""
    command = [
        "python", "-m", "pytest", "tests/",
        "-n", str(num_workers)
    ]
    if verbose:
        command.append("-v")
    return run_command(command, f"Running tests in parallel ({num_workers} workers)")


def run_benchmark_tests(verbose: bool = False) -> bool:
    """Run benchmark tests."""
    command = ["python", "-m", "pytest", "tests/", "--benchmark-only"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running benchmark tests")


def run_memory_tests(verbose: bool = False) -> bool:
    """Run memory profiling tests."""
    command = ["python", "-m", "pytest", "tests/", "--memray"]
    if verbose:
        command.append("-v")
    return run_command(command, "Running memory profiling tests")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="MyzamAI Pytest Runner")
    parser.add_argument(
        "test_type",
        choices=[
            "unit", "integration", "article", "performance", 
            "all", "quick", "slow", "coverage", "parallel", 
            "benchmark", "memory"
        ],
        help="Type of tests to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Run with coverage (for 'all' tests)"
    )
    parser.add_argument(
        "-n", "--num-workers",
        type=int,
        default=4,
        help="Number of parallel workers (for 'parallel' tests)"
    )
    
    args = parser.parse_args()
    
    print("🧪 MyzamAI Pytest Runner")
    print("="*60)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success = False
    
    if args.test_type == "unit":
        success = run_unit_tests(args.verbose)
    elif args.test_type == "integration":
        success = run_integration_tests(args.verbose)
    elif args.test_type == "article":
        success = run_article_tests(args.verbose)
    elif args.test_type == "performance":
        success = run_performance_tests(args.verbose)
    elif args.test_type == "all":
        success = run_all_tests(args.verbose, args.coverage)
    elif args.test_type == "quick":
        success = run_quick_tests(args.verbose)
    elif args.test_type == "slow":
        success = run_slow_tests(args.verbose)
    elif args.test_type == "coverage":
        success = run_with_coverage(args.verbose)
    elif args.test_type == "parallel":
        success = run_parallel_tests(args.verbose, args.num_workers)
    elif args.test_type == "benchmark":
        success = run_benchmark_tests(args.verbose)
    elif args.test_type == "memory":
        success = run_memory_tests(args.verbose)
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
