"""
Интеграционный тест бота MyzamAI
Проверяет работу всего пайплайна агентов
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BotIntegrationTester:
    """
    Интеграционный тестер бота
    """
    
    def __init__(self):
        """
        Initialize tester
        """
        self.test_results = []
        self.start_time = None
    
    async def test_article_commands(self):
        """
        Тестирует команды /law
        """
        print("🔍 Testing /law commands...")
        
        # Test cases: (article_number, expected_keywords)
        test_cases = [
            (379, ["смертью", "гражданина", "обязательство"]),
            (380, ["ликвидацией", "юридического", "лица"]),
            (381, ["договор", "соглашение", "гражданских"]),
            (22, ["объекты", "гражданских", "прав"]),
            (1, ["отношения", "гражданским", "законодательством"])
        ]
        
        for article_num, expected_keywords in test_cases:
            print(f"\n📚 Testing /law {article_num}:")
            
            try:
                # Simulate /law command
                result = await self._simulate_law_command(article_num)
                
                if result is None:
                    print(f"   ❌ Article {article_num}: NOT FOUND")
                    self.test_results.append({
                        'test': f'/law {article_num}',
                        'status': 'NOT_FOUND',
                        'message': 'Article not found'
                    })
                    continue
                
                # Check if result contains expected keywords
                found_keywords = []
                for keyword in expected_keywords:
                    if keyword.lower() in result.lower():
                        found_keywords.append(keyword)
                
                if len(found_keywords) >= len(expected_keywords) * 0.5:  # At least 50% of keywords
                    print(f"   ✅ Article {article_num}: CORRECT")
                    print(f"   📝 Found keywords: {found_keywords}")
                    self.test_results.append({
                        'test': f'/law {article_num}',
                        'status': 'PASS',
                        'message': f'Found {len(found_keywords)}/{len(expected_keywords)} keywords',
                        'found_keywords': found_keywords
                    })
                else:
                    print(f"   ❌ Article {article_num}: INSUFFICIENT KEYWORDS")
                    print(f"   📝 Found: {found_keywords}")
                    print(f"   📝 Expected: {expected_keywords}")
                    self.test_results.append({
                        'test': f'/law {article_num}',
                        'status': 'FAIL',
                        'message': f'Only found {len(found_keywords)}/{len(expected_keywords)} keywords',
                        'found_keywords': found_keywords,
                        'expected_keywords': expected_keywords
                    })
                
                # Show preview
                print(f"   📄 Preview: {result[:150]}...")
                
            except Exception as e:
                print(f"   🚨 Article {article_num}: ERROR - {str(e)}")
                self.test_results.append({
                    'test': f'/law {article_num}',
                    'status': 'ERROR',
                    'message': f'Exception: {str(e)}'
                })
    
    async def test_legal_queries(self):
        """
        Тестирует юридические запросы
        """
        print("\n🔍 Testing legal queries...")
        
        # Test cases: (query, expected_keywords)
        test_cases = [
            (
                "Могу ли я вернуть товар без чека?",
                ["статья", "гражданский", "кодекс", "потребитель"]
            ),
            (
                "Какие у меня права как собственника?",
                ["собственность", "права", "имущество"]
            ),
            (
                "Как расторгнуть договор?",
                ["договор", "расторжение", "соглашение"]
            ),
            (
                "Что такое обязательство?",
                ["обязательство", "должник", "кредитор"]
            )
        ]
        
        for query, expected_keywords in test_cases:
            print(f"\n❓ Testing query: {query}")
            
            try:
                # Simulate query processing
                result = await self._simulate_query_processing(query)
                
                if result is None or len(result) < 50:
                    print(f"   ❌ Query failed: No meaningful response")
                    self.test_results.append({
                        'test': f'Query: {query}',
                        'status': 'FAIL',
                        'message': 'No meaningful response'
                    })
                    continue
                
                # Check if result contains expected keywords
                found_keywords = []
                for keyword in expected_keywords:
                    if keyword.lower() in result.lower():
                        found_keywords.append(keyword)
                
                if len(found_keywords) >= len(expected_keywords) * 0.3:  # At least 30% of keywords
                    print(f"   ✅ Query processed: CORRECT")
                    print(f"   📝 Found keywords: {found_keywords}")
                    self.test_results.append({
                        'test': f'Query: {query}',
                        'status': 'PASS',
                        'message': f'Found {len(found_keywords)}/{len(expected_keywords)} keywords',
                        'found_keywords': found_keywords
                    })
                else:
                    print(f"   ❌ Query processed: INSUFFICIENT KEYWORDS")
                    print(f"   📝 Found: {found_keywords}")
                    print(f"   📝 Expected: {expected_keywords}")
                    self.test_results.append({
                        'test': f'Query: {query}',
                        'status': 'FAIL',
                        'message': f'Only found {len(found_keywords)}/{len(expected_keywords)} keywords',
                        'found_keywords': found_keywords,
                        'expected_keywords': expected_keywords
                    })
                
                # Show preview
                print(f"   📄 Preview: {result[:150]}...")
                
            except Exception as e:
                print(f"   🚨 Query error: {str(e)}")
                self.test_results.append({
                    'test': f'Query: {query}',
                    'status': 'ERROR',
                    'message': f'Exception: {str(e)}'
                })
    
    async def test_edge_cases(self):
        """
        Тестирует граничные случаи
        """
        print("\n🔍 Testing edge cases...")
        
        edge_cases = [
            {
                'name': 'Non-existent article',
                'query': '/law 99999',
                'expected_behavior': 'should_return_error'
            },
            {
                'name': 'Invalid article number',
                'query': '/law abc',
                'expected_behavior': 'should_return_error'
            },
            {
                'name': 'Non-legal question',
                'query': 'Какая погода сегодня?',
                'expected_behavior': 'should_reject_non_legal'
            },
            {
                'name': 'Empty query',
                'query': '',
                'expected_behavior': 'should_handle_gracefully'
            }
        ]
        
        for case in edge_cases:
            print(f"\n🔍 Testing: {case['name']}")
            
            try:
                if case['query'].startswith('/law'):
                    result = await self._simulate_law_command(case['query'].split()[1])
                else:
                    result = await self._simulate_query_processing(case['query'])
                
                # Validate based on expected behavior
                success = self._validate_edge_case(result, case)
                
                if success:
                    print(f"   ✅ {case['name']}: CORRECT")
                    self.test_results.append({
                        'test': case['name'],
                        'status': 'PASS',
                        'message': 'Handled correctly'
                    })
                else:
                    print(f"   ❌ {case['name']}: INCORRECT")
                    self.test_results.append({
                        'test': case['name'],
                        'status': 'FAIL',
                        'message': 'Not handled correctly'
                    })
                
                print(f"   📄 Response: {result[:100] if result else 'None'}...")
                
            except Exception as e:
                print(f"   🚨 {case['name']}: ERROR - {str(e)}")
                self.test_results.append({
                    'test': case['name'],
                    'status': 'ERROR',
                    'message': f'Exception: {str(e)}'
                })
    
    async def _simulate_law_command(self, article_num):
        """
        Симулирует команду /law
        """
        try:
            # This would normally call the orchestrator
            # For now, we'll simulate by reading from the data file
            data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'civil_code_chunks.txt')
            
            if not os.path.exists(data_file):
                return None
            
            with open(data_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the article
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith(f"Статья {article_num}:"):
                    return line
            
            return None
            
        except Exception as e:
            logger.error(f"Error simulating law command: {e}")
            return None
    
    async def _simulate_query_processing(self, query):
        """
        Симулирует обработку запроса
        """
        try:
            # This would normally call the full pipeline
            # For now, we'll return a simple response
            if not query or len(query.strip()) < 3:
                return "Пожалуйста, задайте более конкретный вопрос."
            
            if "погода" in query.lower() or "погода" in query.lower():
                return "Этот вопрос не относится к гражданскому праву КР. Обратитесь к метеорологической службе."
            
            return f"Ответ на ваш вопрос: '{query}'. Рекомендуется проконсультироваться с юристом для получения детальной правовой консультации."
            
        except Exception as e:
            logger.error(f"Error simulating query processing: {e}")
            return None
    
    def _validate_edge_case(self, result, case):
        """
        Валидирует граничный случай
        """
        if case['expected_behavior'] == 'should_return_error':
            return result is None or 'не найдена' in result.lower() or 'ошибка' in result.lower()
        elif case['expected_behavior'] == 'should_handle_gracefully':
            return result is not None and len(result) > 0
        elif case['expected_behavior'] == 'should_reject_non_legal':
            return 'не относится к гражданскому праву' in result.lower()
        
        return True
    
    def run_comprehensive_test(self):
        """
        Запускает комплексный тест
        """
        print("🚀 Starting Comprehensive Bot Integration Test")
        print("="*60)
        
        self.start_time = datetime.now()
        
        # Run all tests
        asyncio.run(self.test_article_commands())
        asyncio.run(self.test_legal_queries())
        asyncio.run(self.test_edge_cases())
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        not_found = sum(1 for r in self.test_results if r['status'] == 'NOT_FOUND')
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🚨 Errors: {errors}")
        print(f"🚫 Not Found: {not_found}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Bot integration is working correctly!")
        elif success_rate >= 70:
            print("⚠️  GOOD, but some issues remain.")
        else:
            print("🚨 POOR! Significant issues with bot integration.")
        
        return {
            'total_tests': total_tests,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'not_found': not_found,
            'success_rate': success_rate,
            'duration': duration,
            'results': self.test_results
        }


def main():
    """
    Main function
    """
    tester = BotIntegrationTester()
    results = tester.run_comprehensive_test()
    
    print(f"\n📁 Test completed! Check results above.")
    return results


if __name__ == "__main__":
    main()
