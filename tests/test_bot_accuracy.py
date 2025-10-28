"""
Комплексная система тестирования точности MyzamAI бота
Проверяет правильность ссылок на статьи и работу агентов
"""

import asyncio
import sys
import os
import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.law_retriever import LawRetriever
from core.agents import (
    LegalExpertAgent,
    SummarizerAgent,
    TranslatorAgent,
    ReviewerAgent,
    UserInterfaceAgent
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class BotAccuracyTester:
    """
    Комплексный тестер точности бота
    """
    
    def __init__(self, index_dir: str):
        """
        Initialize tester with all components
        
        Args:
            index_dir: Directory containing FAISS index
        """
        logger.info("Initializing Bot Accuracy Tester...")
        
        # Initialize all agents
        self.retriever = LawRetriever(index_dir)
        self.legal_expert = LegalExpertAgent()
        self.summarizer = SummarizerAgent()
        self.translator = TranslatorAgent()
        self.reviewer = ReviewerAgent()
        self.ui_agent = UserInterfaceAgent()
        
        # Test results storage
        self.test_results = {
            'article_accuracy': [],
            'agent_pipeline': [],
            'edge_cases': [],
            'performance': [],
            'summary': {}
        }
        
        logger.info("✓ Bot Accuracy Tester initialized")
    
    def test_article_retrieval(self, article_numbers: List[int]) -> Dict:
        """
        Тестирует точность извлечения статей
        
        Args:
            article_numbers: Список номеров статей для тестирования
            
        Returns:
            Результаты тестирования
        """
        logger.info(f"Testing article retrieval for {len(article_numbers)} articles...")
        
        results = {
            'total_tests': len(article_numbers),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'details': []
        }
        
        for article_num in article_numbers:
            try:
                logger.info(f"Testing article {article_num}...")
                
                # Test direct article retrieval
                article_text = self._get_article_by_number(article_num)
                
                if article_text is None:
                    results['errors'] += 1
                    results['details'].append({
                        'article': article_num,
                        'status': 'ERROR',
                        'message': 'Article not found',
                        'retrieved_text': None
                    })
                    continue
                
                # Check if retrieved text starts with correct article number
                if article_text.strip().startswith(f"Статья {article_num}"):
                    results['passed'] += 1
                    results['details'].append({
                        'article': article_num,
                        'status': 'PASS',
                        'message': 'Correct article retrieved',
                        'retrieved_text': article_text[:200] + '...' if len(article_text) > 200 else article_text
                    })
                else:
                    results['failed'] += 1
                    # Extract actual article number from retrieved text
                    actual_article = self._extract_article_number(article_text)
                    results['details'].append({
                        'article': article_num,
                        'status': 'FAIL',
                        'message': f'Wrong article retrieved. Expected {article_num}, got {actual_article}',
                        'retrieved_text': article_text[:200] + '...' if len(article_text) > 200 else article_text,
                        'actual_article': actual_article
                    })
                
            except Exception as e:
                results['errors'] += 1
                results['details'].append({
                    'article': article_num,
                    'status': 'ERROR',
                    'message': f'Exception: {str(e)}',
                    'retrieved_text': None
                })
                logger.error(f"Error testing article {article_num}: {e}")
        
        self.test_results['article_accuracy'] = results
        return results
    
    def _get_article_by_number(self, article_num: int) -> Optional[str]:
        """
        Get specific article by number (copied from main.py)
        """
        try:
            # Load chunks directly and search for exact match
            if not hasattr(self.retriever, 'chunks') or self.retriever.chunks is None:
                self.retriever.load()
            
            # Collect all parts of the article
            article_parts = []
            for chunk in self.retriever.chunks:
                if chunk.strip().startswith(f"Статья {article_num}"):
                    article_parts.append(chunk.strip())
            
            if article_parts:
                # Combine all parts and clean up
                full_article = self._combine_article_parts(article_parts)
                return full_article
            
            # If not found, try FAISS search as fallback
            results = self.retriever.search(f"Статья {article_num}", top_k=10)
            for chunk, score in results:
                if chunk.strip().startswith(f"Статья {article_num}"):
                    return chunk
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving article: {e}")
            return None
    
    def _extract_article_number(self, text: str) -> Optional[int]:
        """
        Extract article number from text
        """
        import re
        match = re.search(r'Статья (\d+)', text)
        if match:
            return int(match.group(1))
        return None
    
    def _combine_article_parts(self, parts: list) -> str:
        """
        Combine article parts and clean up formatting (copied from main.py)
        """
        if not parts:
            return ""
        
        # Use only the first complete part to avoid duplication
        combined = parts[0]
        
        # Clean up the combined text
        combined = self._clean_article_text(combined)
        return combined
    
    def _clean_article_text(self, text: str) -> str:
        """
        Clean up article text (copied from main.py)
        """
        import re
        
        # Remove multiple consecutive separators
        text = re.sub(r'=+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove bullet points that might be artifacts
        text = re.sub(r'^•\s*', '', text, flags=re.MULTILINE)
        
        # Remove duplicate content by finding repeated patterns
        lines = text.split('.')
        unique_lines = []
        seen_content = set()
        
        for line in lines:
            line = line.strip()
            if line and line not in seen_content:
                # Check if this line is not a duplicate of previous content
                is_duplicate = False
                for seen in seen_content:
                    if len(line) > 20 and line in seen:
                        is_duplicate = True
                        break
                    if len(seen) > 20 and seen in line:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_lines.append(line)
                    seen_content.add(line)
        
        # Rejoin the unique content
        text = '. '.join(unique_lines)
        
        # Clean up the text
        text = text.strip()
        
        return text
    
    def test_agent_pipeline(self, test_queries: List[Dict]) -> Dict:
        """
        Тестирует весь пайплайн агентов
        
        Args:
            test_queries: Список тестовых запросов с ожидаемыми результатами
            
        Returns:
            Результаты тестирования пайплайна
        """
        logger.info(f"Testing agent pipeline with {len(test_queries)} queries...")
        
        results = {
            'total_tests': len(test_queries),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'details': []
        }
        
        for i, test_case in enumerate(test_queries):
            try:
                logger.info(f"Testing query {i+1}: {test_case['query']}")
                
                start_time = datetime.now()
                
                # Process query through full pipeline
                response = asyncio.run(self._process_query_pipeline(test_case['query']))
                
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                # Check if response contains expected elements
                success = self._validate_response(response, test_case)
                
                if success:
                    results['passed'] += 1
                    status = 'PASS'
                    message = 'Pipeline processed correctly'
                else:
                    results['failed'] += 1
                    status = 'FAIL'
                    message = 'Pipeline validation failed'
                
                results['details'].append({
                    'query': test_case['query'],
                    'status': status,
                    'message': message,
                    'processing_time': processing_time,
                    'response_length': len(response),
                    'response_preview': response[:200] + '...' if len(response) > 200 else response
                })
                
            except Exception as e:
                results['errors'] += 1
                results['details'].append({
                    'query': test_case['query'],
                    'status': 'ERROR',
                    'message': f'Exception: {str(e)}',
                    'processing_time': None,
                    'response_length': 0,
                    'response_preview': None
                })
                logger.error(f"Error testing query {test_case['query']}: {e}")
        
        self.test_results['agent_pipeline'] = results
        return results
    
    async def _process_query_pipeline(self, query: str) -> str:
        """
        Process query through full agent pipeline
        """
        try:
            # Step 1: Detect language
            detected_lang = self.translator.detect_language(query)
            
            # Step 2: Check language support
            if detected_lang != 'ru':
                return self.ui_agent.format_error(
                    "Извините, я работаю только на русском языке. Пожалуйста, задайте вопрос на русском языке."
                )
            
            query_ru = query
            
            # Step 3: Retrieve relevant legal articles
            search_results = self.retriever.search(query_ru, top_k=3)
            
            if not search_results:
                return self.ui_agent.format_error("Не найдено релевантных статей закона")
            
            # Extract articles
            articles = [article for article, _ in search_results]
            legal_texts = "\n\n".join(articles)
            
            # Step 4: Legal Expert interpretation
            interpretation = self.legal_expert.interpret(query_ru, legal_texts)
            
            # Step 5: Review the interpretation
            review_result = self.reviewer.review(query_ru, legal_texts, interpretation)
            
            if not review_result['approved']:
                interpretation = review_result.get('corrected_response', interpretation)
            
            # Step 6: Summarize if too long
            interpretation = self.summarizer.condense_for_telegram(interpretation)
            
            # Step 7: Format for user interface
            formatted_response = self.ui_agent.format_response(
                query=query,
                legal_interpretation=interpretation,
                source_articles=articles
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return self.ui_agent.format_error(str(e))
    
    def _validate_response(self, response: str, test_case: Dict) -> bool:
        """
        Validate response against test case expectations
        """
        # Check if response is not empty
        if not response or len(response.strip()) < 10:
            return False
        
        # Check for expected keywords if specified
        if 'expected_keywords' in test_case:
            for keyword in test_case['expected_keywords']:
                if keyword.lower() not in response.lower():
                    return False
        
        # Check for expected article numbers if specified
        if 'expected_articles' in test_case:
            for article_num in test_case['expected_articles']:
                if f"Статья {article_num}" not in response:
                    return False
        
        # Check that response doesn't contain error indicators
        error_indicators = ['ошибка', 'error', 'не найдено', 'не удалось']
        for indicator in error_indicators:
            if indicator.lower() in response.lower():
                return False
        
        return True
    
    def test_edge_cases(self) -> Dict:
        """
        Тестирует граничные случаи
        """
        logger.info("Testing edge cases...")
        
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
                'name': 'Empty query',
                'query': '',
                'expected_behavior': 'should_handle_gracefully'
            },
            {
                'name': 'Non-legal question',
                'query': 'Какая погода сегодня?',
                'expected_behavior': 'should_reject_non_legal'
            },
            {
                'name': 'Very long query',
                'query': 'Могу ли я вернуть товар без чека? ' * 100,
                'expected_behavior': 'should_handle_long_query'
            }
        ]
        
        results = {
            'total_tests': len(edge_cases),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'details': []
        }
        
        for case in edge_cases:
            try:
                logger.info(f"Testing edge case: {case['name']}")
                
                # Process the edge case
                response = asyncio.run(self._process_query_pipeline(case['query']))
                
                # Validate based on expected behavior
                success = self._validate_edge_case(response, case)
                
                if success:
                    results['passed'] += 1
                    status = 'PASS'
                else:
                    results['failed'] += 1
                    status = 'FAIL'
                
                results['details'].append({
                    'name': case['name'],
                    'query': case['query'],
                    'status': status,
                    'response_preview': response[:200] + '...' if len(response) > 200 else response
                })
                
            except Exception as e:
                results['errors'] += 1
                results['details'].append({
                    'name': case['name'],
                    'query': case['query'],
                    'status': 'ERROR',
                    'response_preview': f'Exception: {str(e)}'
                })
        
        self.test_results['edge_cases'] = results
        return results
    
    def _validate_edge_case(self, response: str, case: Dict) -> bool:
        """
        Validate edge case response
        """
        if case['expected_behavior'] == 'should_return_error':
            return 'не найдена' in response.lower() or 'ошибка' in response.lower()
        elif case['expected_behavior'] == 'should_handle_gracefully':
            return len(response) > 0
        elif case['expected_behavior'] == 'should_reject_non_legal':
            return 'не относится к гражданскому праву' in response.lower()
        elif case['expected_behavior'] == 'should_handle_long_query':
            return len(response) > 0
        
        return True
    
    def run_comprehensive_tests(self) -> Dict:
        """
        Запускает все тесты и возвращает сводный отчет
        """
        logger.info("🚀 Starting comprehensive bot accuracy tests...")
        
        # Test article retrieval accuracy
        test_articles = [22, 222, 379, 380, 381, 1, 2, 3, 4, 5]
        article_results = self.test_article_retrieval(test_articles)
        
        # Test agent pipeline
        test_queries = [
            {
                'query': 'Могу ли я вернуть товар без чека?',
                'expected_keywords': ['статья', 'гражданский кодекс'],
                'expected_articles': [22]
            },
            {
                'query': 'Какие у меня права как собственника?',
                'expected_keywords': ['собственность', 'права'],
                'expected_articles': [222]
            },
            {
                'query': 'Как расторгнуть договор?',
                'expected_keywords': ['договор', 'расторжение']
            }
        ]
        pipeline_results = self.test_agent_pipeline(test_queries)
        
        # Test edge cases
        edge_results = self.test_edge_cases()
        
        # Calculate summary
        total_tests = (article_results['total_tests'] + 
                      pipeline_results['total_tests'] + 
                      edge_results['total_tests'])
        
        total_passed = (article_results['passed'] + 
                       pipeline_results['passed'] + 
                       edge_results['passed'])
        
        total_failed = (article_results['failed'] + 
                       pipeline_results['failed'] + 
                       edge_results['failed'])
        
        total_errors = (article_results['errors'] + 
                       pipeline_results['errors'] + 
                       edge_results['errors'])
        
        self.test_results['summary'] = {
            'total_tests': total_tests,
            'passed': total_passed,
            'failed': total_failed,
            'errors': total_errors,
            'success_rate': (total_passed / total_tests * 100) if total_tests > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Tests completed! Success rate: {self.test_results['summary']['success_rate']:.1f}%")
        
        return self.test_results
    
    def save_results(self, filename: str = None):
        """
        Сохраняет результаты тестирования в файл
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📊 Test results saved to: {filepath}")
        return filepath
    
    def print_summary(self):
        """
        Выводит сводный отчет о тестировании
        """
        summary = self.test_results['summary']
        
        print("\n" + "="*60)
        print("📊 BOT ACCURACY TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"🚨 Errors: {summary['errors']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print("="*60)
        
        # Article accuracy details
        if self.test_results['article_accuracy']:
            print("\n📚 ARTICLE ACCURACY:")
            for detail in self.test_results['article_accuracy']['details']:
                status_icon = "✅" if detail['status'] == 'PASS' else "❌" if detail['status'] == 'FAIL' else "🚨"
                print(f"  {status_icon} Article {detail['article']}: {detail['status']} - {detail['message']}")
        
        # Pipeline details
        if self.test_results['agent_pipeline']:
            print("\n🔄 AGENT PIPELINE:")
            for detail in self.test_results['agent_pipeline']['details']:
                status_icon = "✅" if detail['status'] == 'PASS' else "❌" if detail['status'] == 'FAIL' else "🚨"
                print(f"  {status_icon} Query: {detail['query'][:50]}... - {detail['status']}")
        
        # Edge cases details
        if self.test_results['edge_cases']:
            print("\n🔍 EDGE CASES:")
            for detail in self.test_results['edge_cases']['details']:
                status_icon = "✅" if detail['status'] == 'PASS' else "❌" if detail['status'] == 'FAIL' else "🚨"
                print(f"  {status_icon} {detail['name']}: {detail['status']}")


def main():
    """
    Main function to run comprehensive tests
    """
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    index_dir = os.path.join(project_root, 'faiss_index')
    
    # Check if FAISS index exists
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        logger.error("FAISS index not found! Please run core/build_faiss_index.py first.")
        return
    
    # Initialize tester
    tester = BotAccuracyTester(index_dir)
    
    # Run comprehensive tests
    results = tester.run_comprehensive_tests()
    
    # Print summary
    tester.print_summary()
    
    # Save results
    results_file = tester.save_results()
    
    print(f"\n📁 Detailed results saved to: {results_file}")


if __name__ == "__main__":
    main()
