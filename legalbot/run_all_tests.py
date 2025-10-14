#!/usr/bin/env python3
"""
Запуск всех тестов MyzamAI
Комплексная проверка точности и работы бота
"""

import subprocess
import sys
import os
import time
from datetime import datetime


def run_test(test_name, command, description):
    """
    Запускает тест и возвращает результат
    """
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"📝 {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name}: PASSED ({duration:.2f}s)")
            return {
                'name': test_name,
                'status': 'PASS',
                'duration': duration,
                'output': result.stdout
            }
        else:
            print(f"❌ {test_name}: FAILED ({duration:.2f}s)")
            print(f"Error: {result.stderr}")
            return {
                'name': test_name,
                'status': 'FAIL',
                'duration': duration,
                'error': result.stderr,
                'output': result.stdout
            }
    
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"🚨 {test_name}: ERROR ({duration:.2f}s)")
        print(f"Exception: {str(e)}")
        return {
            'name': test_name,
            'status': 'ERROR',
            'duration': duration,
            'error': str(e)
        }


def main():
    """
    Запускает все тесты
    """
    print("🚀 MyzamAI Comprehensive Testing Suite")
    print("="*60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all tests
    tests = [
        {
            'name': 'Simple Article Test',
            'command': 'python3 simple_test.py',
            'description': 'Базовый тест извлечения статей из файла'
        },
        {
            'name': 'Article Accuracy Test',
            'command': 'python3 tests/test_article_accuracy_simple.py',
            'description': 'Комплексный тест точности статей'
        },
        {
            'name': 'Bot Integration Test',
            'command': 'python3 tests/test_bot_integration.py',
            'description': 'Интеграционный тест работы бота'
        }
    ]
    
    # Run all tests
    results = []
    total_start_time = time.time()
    
    for test in tests:
        result = run_test(
            test['name'],
            test['command'],
            test['description']
        )
        results.append(result)
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Calculate summary
    total_tests = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')
    
    success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TESTING SUMMARY")
    print(f"{'='*60}")
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Total Duration: {total_duration:.2f} seconds")
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"🚨 Errors: {errors}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    # Detailed results
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "🚨"
        print(f"  {status_icon} {result['name']}: {result['status']} ({result['duration']:.2f}s)")
    
    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if success_rate >= 90:
        print("🎉 EXCELLENT! All tests are passing. Bot is working correctly!")
        print("✅ Ready for production deployment.")
    elif success_rate >= 70:
        print("⚠️  GOOD, but some issues remain. Consider fixing failed tests.")
        print("🔧 Review failed tests and improve implementation.")
    else:
        print("🚨 POOR! Significant issues detected. Bot needs major improvements.")
        print("🛠️  Fix critical issues before deployment.")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if failed > 0:
        print("🔧 Fix failed tests:")
        for result in results:
            if result['status'] == 'FAIL':
                print(f"   - {result['name']}: {result.get('error', 'Unknown error')}")
    
    if errors > 0:
        print("🚨 Resolve errors:")
        for result in results:
            if result['status'] == 'ERROR':
                print(f"   - {result['name']}: {result.get('error', 'Unknown error')}")
    
    if success_rate >= 90:
        print("🚀 Consider adding more comprehensive tests:")
        print("   - Performance tests under load")
        print("   - Edge case testing")
        print("   - User acceptance testing")
    
    print(f"\n📁 Test results saved to: {os.path.dirname(os.path.abspath(__file__))}")
    print("="*60)
    
    return {
        'total_tests': total_tests,
        'passed': passed,
        'failed': failed,
        'errors': errors,
        'success_rate': success_rate,
        'total_duration': total_duration,
        'results': results
    }


if __name__ == "__main__":
    try:
        results = main()
        
        # Exit with appropriate code
        if results['success_rate'] >= 90:
            sys.exit(0)  # Success
        elif results['success_rate'] >= 70:
            sys.exit(1)  # Warning
        else:
            sys.exit(2)  # Error
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n🚨 Unexpected error: {str(e)}")
        sys.exit(1)
