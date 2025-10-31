"""
Полный тест retrieval accuracy для всех статей в базе
"""

import os
import sys
import re
import json
from datetime import datetime
from typing import List, Dict, Optional

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class FullRetrievalAccuracyTester:
    """
    Полный тестер accuracy для всех статей
    
    Этот тестер проверяет РЕАЛЬНУЮ работу get_article_by_number,
    используя ту же логику, что и реальный бот.
    """
    
    def __init__(self, data_file_path: str, index_dir: Optional[str] = None):
        """
        Initialize tester
        
        Args:
            data_file_path: Path to civil_code_full.txt
            index_dir: Optional path to FAISS index directory
        """
        self.data_file_path = data_file_path
        self.index_dir = index_dir
        self.test_results = []
        self.retriever = None
        self.orchestrator = None
        
        # Try to load orchestrator (REAL implementation)
        if index_dir and os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
            try:
                from src.bot.main import LegalBotOrchestrator
                self.orchestrator = LegalBotOrchestrator(index_dir)
                print("✅ Orchestrator loaded - using REAL get_article_by_number method")
            except Exception as e:
                print(f"⚠️  Could not load orchestrator: {e}")
                # Fallback to retriever only
                try:
                    from src.core.law_retriever import LawRetriever
                    self.retriever = LawRetriever(index_dir)
                    self.retriever.load()
                    print("✅ FAISS index loaded successfully (fallback mode)")
                except Exception as e2:
                    print(f"⚠️  Could not load FAISS index: {e2}")
                    print("   Will test using file-based method only")
    
    def find_all_articles(self) -> List[int]:
        """
        Находит все уникальные номера статей в базе
        
        Returns:
            Список номеров статей
        """
        print("🔍 Scanning database for all articles...")
        
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Находим все упоминания статей
        article_pattern = re.compile(r'Статья\s+(\d+)')
        all_matches = article_pattern.findall(text)
        
        # Уникальные номера в разумном диапазоне
        unique_articles = set()
        for match in all_matches:
            num = int(match)
            if 1 <= num <= 2000:  # Разумный диапазон для гражданского кодекса
                unique_articles.add(num)
        
        sorted_articles = sorted(unique_articles)
        print(f"   Found {len(sorted_articles)} unique articles")
        print(f"   Range: {sorted_articles[0]} - {sorted_articles[-1]}")
        
        return sorted_articles
    
    def test_article_via_retriever(self, article_num: int) -> Dict:
        """
        Тестирует извлечение статьи через REAL get_article_by_number method
        
        Этот метод использует ТОЧНУЮ логику из main.py для проверки реальной работы
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Результат теста
        """
        if not self.retriever:
            return None
        
        try:
            # Используем РЕАЛЬНУЮ логику из orchestrator.get_article_by_number
            # Это точная копия логики из main.py для проверки реальной работы
            chunks = self.retriever.chunks or []
            
            # STRICT matching - точно как в get_article_by_number
            article_parts = []
            for chunk in chunks:
                chunk_clean = chunk.strip()
                # STRICT: Must start with exact "Статья {article_num}" pattern
                if chunk_clean.startswith(f"Статья {article_num}"):
                    # Additional validation: ensure it's not a partial match
                    # Check that the next character after the number is not a digit
                    pattern = f"Статья {article_num}"
                    if len(chunk_clean) > len(pattern):
                        next_char = chunk_clean[len(pattern)]
                        if next_char.isdigit():
                            # This is a partial match (e.g., "Статья 37" matches "Статья 379")
                            continue
                    article_parts.append(chunk_clean)
            
            if article_parts:
                # Final validation: ensure the result starts with the correct article
                # (simulating _combine_article_parts logic - use first part)
                full_article = article_parts[0]  # Simplified for testing
                if full_article.strip().startswith(f"Статья {article_num}"):
                    return {
                        'status': 'PASS',
                        'found': True,
                        'method': 'retriever_real',
                        'parts_count': len(article_parts),
                        'article_preview': full_article[:100] + '...' if len(full_article) > 100 else full_article
                    }
                else:
                    return {
                        'status': 'PARTIAL',
                        'found': True,
                        'method': 'retriever_real',
                        'issue': 'Validation failed - wrong article number in result',
                        'article_preview': full_article[:100] + '...' if len(full_article) > 100 else full_article
                    }
            else:
                # If not found in chunks, try FAISS search (simulating fallback)
                # This is the fallback logic from get_article_by_number
                try:
                    results = self.retriever.search(f"Статья {article_num}", top_k=20)
                    for chunk, score in results:
                        chunk_clean = chunk.strip()
                        if chunk_clean.startswith(f"Статья {article_num}"):
                            pattern = f"Статья {article_num}"
                            if len(chunk_clean) > len(pattern):
                                next_char = chunk_clean[len(pattern)]
                                if next_char.isdigit():
                                    continue
                            if chunk_clean.startswith(f"Статья {article_num}"):
                                return {
                                    'status': 'PASS',
                                    'found': True,
                                    'method': 'retriever_faiss_fallback',
                                    'score': float(score),
                                    'article_preview': chunk_clean[:100] + '...' if len(chunk_clean) > 100 else chunk_clean
                                }
                except Exception as e:
                    pass  # Fallback failed, continue to NOT_FOUND
                
                return {
                    'status': 'NOT_FOUND',
                    'found': False,
                    'method': 'retriever_real',
                    'note': 'Article not found in chunks and FAISS fallback also failed'
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'found': False,
                'method': 'retriever_real',
                'error': str(e)
            }
    
    def test_article_via_file(self, article_num: int) -> Dict:
        """
        Тестирует наличие статьи в файле
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Результат теста
        """
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Ищем точное совпадение "Статья {num}" в начале строки или после переноса
            pattern = rf'^Статья\s+{article_num}\b'
            matches = re.findall(pattern, text, re.MULTILINE)
            
            if matches:
                # Проверяем контекст - следующая позиция после номера
                # Ищем паттерн и проверяем, что после номера не идет еще цифра
                full_pattern = rf'Статья\s+{article_num}([^\d]|$)'
                full_matches = re.findall(full_pattern, text, re.MULTILINE)
                
                if full_matches:
                    return {
                        'status': 'PASS',
                        'found': True,
                        'method': 'file',
                        'matches': len(full_matches)
                    }
                else:
                    return {
                        'status': 'PARTIAL',
                        'found': True,
                        'method': 'file',
                        'issue': 'Possible partial match'
                    }
            else:
                return {
                    'status': 'NOT_FOUND',
                    'found': False,
                    'method': 'file'
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'found': False,
                'method': 'file',
                'error': str(e)
            }
    
    def test_article_via_orchestrator(self, article_num: int) -> Dict:
        """
        Тестирует через РЕАЛЬНЫЙ orchestrator.get_article_by_number
        
        Это самый точный тест - использует ТОЧНО ту же логику, что и бот в продакшене
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Результат теста
        """
        if not self.orchestrator:
            return None
        
        try:
            # РЕАЛЬНЫЙ вызов метода из production кода
            article_text = self.orchestrator.get_article_by_number(article_num)
            
            if article_text is None:
                return {
                    'status': 'NOT_FOUND',
                    'found': False,
                    'method': 'orchestrator_real'
                }
            
            # Проверяем, что возвращенная статья правильная
            article_text_clean = article_text.strip()
            
            # Валидация: статья должна начинаться с правильного номера
            if article_text_clean.startswith(f"Статья {article_num}"):
                # Более строгая проверка: статья должна содержать существенный контент
                # Минимум 50 символов (чтобы исключить только "Статья N" или очень короткие заголовки)
                min_content_length = 50
                
                # Проверяем, есть ли контент после номера статьи
                pattern_variants = [
                    f"Статья {article_num} ",
                    f"Статья {article_num}:",
                    f"Статья {article_num}.",
                    f"Статья {article_num}"
                ]
                
                content_length = 0
                for pattern in pattern_variants:
                    if article_text_clean.startswith(pattern):
                        # Содержимое после паттерна
                        content_after_pattern = article_text_clean[len(pattern):].strip()
                        content_length = len(content_after_pattern)
                        break
                
                if content_length >= min_content_length:
                    return {
                        'status': 'PASS',
                        'found': True,
                        'method': 'orchestrator_real',
                        'article_length': len(article_text),
                        'content_length': content_length,
                        'article_preview': article_text[:150] + '...' if len(article_text) > 150 else article_text
                    }
                else:
                    return {
                        'status': 'PARTIAL',
                        'found': True,
                        'method': 'orchestrator_real',
                        'issue': f'Article found but content too short: {content_length} chars (min: {min_content_length})',
                        'article_length': len(article_text),
                        'content_length': content_length,
                        'article_preview': article_text
                    }
            else:
                # Статья найдена, но с неправильным номером
                # Извлекаем реальный номер
                match = re.search(r'Статья\s+(\d+)', article_text_clean)
                actual_num = match.group(1) if match else "Unknown"
                return {
                    'status': 'FAIL',
                    'found': False,
                    'method': 'orchestrator_real',
                    'issue': f'Wrong article returned: expected {article_num}, got {actual_num}',
                    'article_preview': article_text[:150] + '...' if len(article_text) > 150 else article_text
                }
                
        except Exception as e:
            return {
                'status': 'ERROR',
                'found': False,
                'method': 'orchestrator_real',
                'error': str(e)
            }
    
    def test_article(self, article_num: int) -> Dict:
        """
        Тестирует одну статью всеми доступными методами
        
        Приоритет тестирования:
        1. orchestrator.get_article_by_number (реальный production метод) - САМЫЙ ТОЧНЫЙ
        2. retriever (имитация логики)
        3. file (базовая проверка наличия)
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Результат теста
        """
        result = {
            'article': article_num,
            'results': {}
        }
        
        # ПРИОРИТЕТ 1: Тест через реальный orchestrator (самый точный)
        if self.orchestrator:
            orchestrator_result = self.test_article_via_orchestrator(article_num)
            result['results']['orchestrator'] = orchestrator_result
            primary_result = orchestrator_result
        # ПРИОРИТЕТ 2: Тест через retriever (если orchestrator недоступен)
        elif self.retriever:
            retriever_result = self.test_article_via_retriever(article_num)
            result['results']['retriever'] = retriever_result
            primary_result = retriever_result
        # ПРИОРИТЕТ 3: Тест через файл (базовая проверка)
        else:
            file_result = self.test_article_via_file(article_num)
            result['results']['file'] = file_result
            primary_result = file_result
        
        result['status'] = primary_result['status'] if primary_result else 'ERROR'
        result['found'] = primary_result.get('found', False) if primary_result else False
        
        return result
    
    def run_full_test(self, article_numbers: Optional[List[int]] = None, sample: bool = False):
        """
        Запускает полный тест
        
        Args:
            article_numbers: Список статей для тестирования (если None - все)
            sample: Если True, тестирует каждую 10-ю статью для скорости
        """
        print("\n" + "="*60)
        print("🚀 FULL RETRIEVAL ACCURACY TEST")
        print("="*60)
        
        # Получаем список всех статей
        if article_numbers is None:
            all_articles = self.find_all_articles()
            if sample:
                test_articles = all_articles[::10]  # Каждая 10-я статья
                print(f"\n📊 Testing sample: {len(test_articles)} articles (every 10th)")
            else:
                test_articles = all_articles
                print(f"\n📊 Testing ALL {len(test_articles)} articles")
        else:
            test_articles = article_numbers
            print(f"\n📊 Testing {len(test_articles)} specified articles")
        
        print(f"   This may take several minutes...\n")
        
        # Тестируем каждую статью
        total = len(test_articles)
        for i, article_num in enumerate(test_articles, 1):
            if i % 50 == 0 or i == 1 or i == total:
                print(f"Progress: {i}/{total} ({i/total*100:.1f}%) - Testing Article {article_num}...")
            
            result = self.test_article(article_num)
            self.test_results.append(result)
        
        print(f"\n✅ Testing completed: {total} articles")
        
        return self.calculate_summary()
    
    def calculate_summary(self) -> Dict:
        """
        Вычисляет итоговую статистику
        
        Returns:
            Словарь со статистикой
        """
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        partial = sum(1 for r in self.test_results if r['status'] == 'PARTIAL')
        not_found = sum(1 for r in self.test_results if r['status'] == 'NOT_FOUND')
        errors = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        
        accuracy = (passed / total * 100) if total > 0 else 0
        
        # Определяем метод тестирования
        test_method = "Unknown"
        if self.orchestrator:
            test_method = "orchestrator.get_article_by_number (REAL production method)"
        elif self.retriever:
            test_method = "retriever chunks search (simulated logic)"
        else:
            test_method = "file pattern matching (basic check)"
        
        summary = {
            'total_tests': total,
            'passed': passed,
            'partial': partial,
            'not_found': not_found,
            'errors': errors,
            'accuracy': accuracy,
            'timestamp': datetime.now().isoformat(),
            'test_method': test_method,
            'test_description': self._get_test_description(),
            'results': self.test_results
        }
        
        # Выводим результаты
        print("\n" + "="*60)
        print("📊 RETRIEVAL ACCURACY SUMMARY")
        print("="*60)
        print(f"\n🔬 TEST METHOD: {test_method}")
        print(f"   {self._get_test_description()}")
        print(f"\n📈 TEST RESULTS:")
        print(f"Total Articles Tested: {total}")
        print(f"✅ Passed (Correctly Retrieved): {passed} ({passed/total*100:.1f}%)")
        print(f"⚠️  Partial Matches: {partial} ({partial/total*100:.1f}%)")
        print(f"🚫 Not Found: {not_found} ({not_found/total*100:.1f}%)")
        print(f"❌ Errors: {errors} ({errors/total*100:.1f}%)")
        print(f"\n🎯 RETRIEVAL ACCURACY: {accuracy:.1f}%")
        print("="*60)
        
        if accuracy >= 90:
            print("🎉 EXCELLENT! Retrieval accuracy is very high!")
        elif accuracy >= 80:
            print("✅ GOOD! Retrieval accuracy is acceptable.")
        elif accuracy >= 70:
            print("⚠️  MODERATE. Some improvements needed.")
        else:
            print("🚨 LOW. Significant issues with retrieval.")
        
        return summary
    
    def _get_test_description(self) -> str:
        """
        Возвращает описание метода тестирования для документации
        """
        if self.orchestrator:
            return (
                "Tests use the REAL production method LegalBotOrchestrator.get_article_by_number() "
                "which is the exact same code used in production. For each article number, we call "
                "get_article_by_number() and validate that: (1) method returns non-None result, "
                "(2) returned text starts with correct article number 'Статья {N}', "
                "(3) returned text has substantial content. This is the most accurate test as it "
                "simulates real user requests to the bot."
            )
        elif self.retriever:
            return (
                "Tests simulate the get_article_by_number logic by searching chunks directly. "
                "For each article, we search chunks for exact match starting with 'Статья {N}' "
                "with validation to prevent partial matches (e.g., article 37 matching article 379). "
                "This is less accurate than orchestrator method but validates chunk structure."
            )
        else:
            return (
                "Tests check article existence in raw text file using regex pattern matching. "
                "This is a basic validation that articles exist in the database but does not test "
                "actual retrieval functionality. Use this only if FAISS index is unavailable."
            )
    
    def save_results(self, filename: Optional[str] = None):
        """
        Сохраняет результаты в файл
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"full_retrieval_accuracy_{timestamp}.json"
        
        output_dir = os.path.join(project_root, 'storage')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        summary = self.calculate_summary()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 Full results saved to: {filepath}")
        return filepath


def main():
    """
    Main function
    """
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    data_file = os.path.join(project_root, 'data', 'civil_code_full.txt')
    index_dir = os.path.join(project_root, 'storage', 'faiss_index')
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return
    
    # Initialize tester
    print("🔧 Initializing Full Retrieval Accuracy Tester...")
    tester = FullRetrievalAccuracyTester(data_file, index_dir)
    
    # Ask user for test mode
    print("\nSelect test mode:")
    print("1. Full test (all articles) - slow but complete")
    print("2. Sample test (every 10th article) - faster")
    
    try:
        choice = input("\nEnter choice (1 or 2, default=2): ").strip()
        sample_mode = (choice != '1')
    except:
        sample_mode = True  # Default to sample for safety
    
    # Run full test
    summary = tester.run_full_test(sample=sample_mode)
    
    # Save results
    tester.save_results()
    
    return summary


if __name__ == "__main__":
    main()

