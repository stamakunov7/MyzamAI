#!/usr/bin/env python3
"""
Быстрый тест для проверки исправления бага с неправильными статьями
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from bot.main import LegalBotOrchestrator


async def quick_test():
    """
    Быстрый тест исправления бага
    """
    print("🔍 Quick Test: Article 379 vs 380 Bug Fix")
    print("="*50)
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, 'faiss_index')
    
    # Check if FAISS index exists
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        print("❌ FAISS index not found!")
        return
    
    # Initialize orchestrator
    print("🚀 Initializing orchestrator...")
    orchestrator = LegalBotOrchestrator(index_dir)
    
    # Test the problematic articles
    test_articles = [379, 380, 381]
    
    for article_num in test_articles:
        print(f"\n🔍 Testing Article {article_num}:")
        
        try:
            article_text = orchestrator.get_article_by_number(article_num)
            
            if article_text is None:
                print(f"   ❌ Article {article_num}: NOT FOUND")
                continue
            
            # Check if it's the correct article
            if article_text.strip().startswith(f"Статья {article_num}"):
                print(f"   ✅ Article {article_num}: CORRECT")
                print(f"   📝 Preview: {article_text[:150]}...")
            else:
                # Extract actual article number
                import re
                match = re.search(r'Статья (\d+)', article_text)
                actual_article = match.group(1) if match else "Unknown"
                print(f"   ❌ Article {article_num}: WRONG! Got Article {actual_article}")
                print(f"   📝 Preview: {article_text[:150]}...")
        
        except Exception as e:
            print(f"   🚨 Article {article_num}: ERROR - {str(e)}")
    
    print("\n" + "="*50)
    print("✅ Quick test completed!")


if __name__ == "__main__":
    asyncio.run(quick_test())
