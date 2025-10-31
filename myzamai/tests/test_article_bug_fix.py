"""
Тест для проверки исправления бага с неправильными статьями
Проверяет, что бот возвращает правильную статью по номеру
"""

import pytest
import asyncio
import sys
import os
import logging

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.bot.main import LegalBotOrchestrator

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_article_accuracy():
    """
    Тестирует точность извлечения статей
    """
    print("🔍 Testing article retrieval accuracy...")
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    index_dir = os.path.join(project_root, 'storage', 'faiss_index')
    
    # Check if FAISS index exists
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        print("❌ FAISS index not found! Please run scripts/build_faiss_index.py first.")
        return
    
    # Initialize orchestrator
    orchestrator = LegalBotOrchestrator(index_dir)
    
    # Test cases: (article_number, expected_start)
    test_cases = [
        (379, "Статья 379. Прекращение обязательства смертью гражданина"),
        (380, "Статья 380. Прекращение обязательства ликвидацией юридического лица"),
        (381, "Статья 381. Понятие договора"),
        (22, "Статья 22. Виды объектов гражданских прав"),
        (222, "Статья 222. Понятие и содержание права собственности"),
        (1, "Статья 1. Отношения, регулируемые гражданским законодательством"),
        (2, "Статья 2. Гражданское законодательство"),
        (3, "Статья 3. Действие гражданского законодательства во времени")
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "="*80)
    print("📚 ARTICLE ACCURACY TEST RESULTS")
    print("="*80)
    
    for article_num, expected_start in test_cases:
        print(f"\n🔍 Testing Article {article_num}...")
        
        try:
            # Get article
            article_text = orchestrator.get_article_by_number(article_num)
            
            if article_text is None:
                print(f"❌ Article {article_num}: NOT FOUND")
                failed += 1
                continue
            
            # Check if it starts with the correct article number
            if article_text.strip().startswith(f"Статья {article_num}"):
                print(f"✅ Article {article_num}: CORRECT")
                print(f"   Preview: {article_text[:100]}...")
                passed += 1
            else:
                # Extract actual article number
                import re
                match = re.search(r'Статья (\d+)', article_text)
                actual_article = match.group(1) if match else "Unknown"
                print(f"❌ Article {article_num}: WRONG ARTICLE RETURNED")
                print(f"   Expected: Статья {article_num}")
                print(f"   Got: Статья {actual_article}")
                print(f"   Preview: {article_text[:100]}...")
                failed += 1
        
        except Exception as e:
            print(f"🚨 Article {article_num}: ERROR - {str(e)}")
            failed += 1
    
    # Summary
    total = passed + failed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Article retrieval is working correctly!")
    elif success_rate >= 70:
        print("⚠️  GOOD, but some issues remain. Consider further improvements.")
    else:
        print("🚨 POOR! Significant issues with article retrieval.")
    
    return success_rate


def main():
    """
    Main function
    """
    print("🚀 Starting Article Bug Fix Test...")
    
    # Run the test
    success_rate = asyncio.run(test_article_accuracy())
    
    if success_rate >= 90:
        print("\n✅ Bug fix successful! Bot should now return correct articles.")
    else:
        print("\n❌ Bug fix needs more work. Check the implementation.")


if __name__ == "__main__":
    main()
