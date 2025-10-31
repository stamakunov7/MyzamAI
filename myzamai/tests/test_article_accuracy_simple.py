"""
Упрощенный тест точности статей без зависимостей
"""

import os
import re
import json
from datetime import datetime


class SimpleArticleTester:
    """
    Простой тестер точности статей
    """
    
    def __init__(self, data_file_path: str):
        """
        Initialize tester
        
        Args:
            data_file_path: Path to civil_code_chunks.txt
        """
        self.data_file_path = data_file_path
        self.test_results = []
    
    def test_article_retrieval(self, article_numbers: list):
        """
        Тестирует извлечение статей из файла
        
        Args:
            article_numbers: Список номеров статей для тестирования
        """
        print(f"🔍 Testing article retrieval for {len(article_numbers)} articles...")
        
        # Read the data file
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ Data file not found: {self.data_file_path}")
            return
        
        # Test each article
        for article_num in article_numbers:
            print(f"\n📚 Testing Article {article_num}:")
            
            # Find all lines containing the article
            lines = content.split('\n')
            matches = []
            
            for i, line in enumerate(lines):
                if f"Статья {article_num}:" in line:
                    matches.append((i, line))
            
            if not matches:
                print(f"   ❌ Article {article_num}: NOT FOUND")
                self.test_results.append({
                    'article': article_num,
                    'status': 'NOT_FOUND',
                    'message': 'Article not found in database',
                    'matches': 0
                })
                continue
            
            # Check each match for correctness
            correct_matches = 0
            wrong_matches = 0
            
            for line_num, line in matches:
                if line.strip().startswith(f"Статья {article_num}:"):
                    correct_matches += 1
                    print(f"   ✅ Line {line_num}: CORRECT")
                else:
                    wrong_matches += 1
                    # Extract actual article number
                    match = re.search(r'Статья (\d+):', line)
                    actual_article = match.group(1) if match else "Unknown"
                    print(f"   ❌ Line {line_num}: WRONG - Expected {article_num}, got {actual_article}")
                    print(f"       Content: {line[:100]}...")
            
            # Determine overall status
            if correct_matches > 0 and wrong_matches == 0:
                status = 'PASS'
                message = f'Found {correct_matches} correct matches'
                print(f"   ✅ Article {article_num}: {message}")
            elif correct_matches > 0 and wrong_matches > 0:
                status = 'PARTIAL'
                message = f'Found {correct_matches} correct, {wrong_matches} wrong matches'
                print(f"   ⚠️  Article {article_num}: {message}")
            else:
                status = 'FAIL'
                message = f'No correct matches found'
                print(f"   ❌ Article {article_num}: {message}")
            
            self.test_results.append({
                'article': article_num,
                'status': status,
                'message': message,
                'correct_matches': correct_matches,
                'wrong_matches': wrong_matches,
                'total_matches': len(matches)
            })
    
    def test_specific_bug_case(self):
        """
        Тестирует конкретный случай бага: статья 379 vs 380
        """
        print("\n🐛 Testing specific bug case: Article 379 vs 380")
        print("="*60)
        
        # Test the problematic articles
        problematic_articles = [379, 380, 381]
        
        for article_num in problematic_articles:
            print(f"\n🔍 Testing Article {article_num}:")
            
            # Read the data file
            try:
                with open(self.data_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"❌ Data file not found: {self.data_file_path}")
                return
            
            # Find the article
            lines = content.split('\n')
            found_lines = []
            
            for i, line in enumerate(lines):
                if f"Статья {article_num}:" in line and line.strip().startswith(f"Статья {article_num}:"):
                    found_lines.append((i, line))
            
            if found_lines:
                print(f"   ✅ Found {len(found_lines)} correct matches")
                for line_num, line in found_lines:
                    print(f"   📝 Line {line_num}: {line[:100]}...")
            else:
                print(f"   ❌ No correct matches found")
                
                # Check for partial matches
                partial_matches = []
                for i, line in enumerate(lines):
                    if f"Статья {article_num}" in line and not line.strip().startswith(f"Статья {article_num}:"):
                        partial_matches.append((i, line))
                
                if partial_matches:
                    print(f"   ⚠️  Found {len(partial_matches)} partial matches:")
                    for line_num, line in partial_matches:
                        print(f"       Line {line_num}: {line[:100]}...")
    
    def run_comprehensive_test(self):
        """
        Запускает комплексный тест
        """
        print("🚀 Starting Comprehensive Article Accuracy Test")
        print("="*60)
        
        # Test a range of articles
        test_articles = [1, 2, 3, 4, 5, 22, 222, 379, 380, 381, 382, 383, 384, 385]
        
        # Run the test
        self.test_article_retrieval(test_articles)
        
        # Test specific bug case
        self.test_specific_bug_case()
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        partial = sum(1 for r in self.test_results if r['status'] == 'PARTIAL')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        not_found = sum(1 for r in self.test_results if r['status'] == 'NOT_FOUND')
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"⚠️  Partial: {partial}")
        print(f"❌ Failed: {failed}")
        print(f"🚫 Not Found: {not_found}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Article retrieval is working correctly!")
        elif success_rate >= 70:
            print("⚠️  GOOD, but some issues remain.")
        else:
            print("🚨 POOR! Significant issues with article retrieval.")
        
        return {
            'total_tests': total_tests,
            'passed': passed,
            'partial': partial,
            'failed': failed,
            'not_found': not_found,
            'success_rate': success_rate,
            'results': self.test_results
        }
    
    def save_results(self, filename: str = None):
        """
        Сохраняет результаты в файл
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_test_results_{timestamp}.json"
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"📁 Results saved to: {filepath}")
        return filepath


def main():
    """
    Main function
    """
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_file = os.path.join(project_root, 'data', 'civil_code_chunks.txt')
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return
    
    # Initialize tester
    tester = SimpleArticleTester(data_file)
    
    # Run comprehensive test
    results = tester.run_comprehensive_test()
    
    # Save results
    tester.save_results()
    
    return results


if __name__ == "__main__":
    main()
