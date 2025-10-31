#!/usr/bin/env python3
"""
Простой тест для проверки исправления бага с неправильными статьями
"""

import sys
import os
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))


def test_article_retrieval():
    """
    Простой тест извлечения статей из файла
    """
    print("🔍 Simple Test: Article 379 vs 380 Bug Fix")
    print("="*50)
    
    # Path to the data file (script is in myzamai/scripts/, go up to myzamai/ then to data/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..')
    data_file = os.path.join(project_root, 'data', 'civil_code_chunks.txt')
    
    if not os.path.exists(data_file):
        print("❌ Data file not found!")
        return
    
    # Test articles
    test_articles = [379, 380, 381]
    
    # Read the file
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for article_num in test_articles:
        print(f"\n🔍 Testing Article {article_num}:")
        
        # Find all occurrences of the article
        pattern = f"Статья {article_num}:"
        matches = []
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if pattern in line:
                matches.append((i, line))
        
        if not matches:
            print(f"   ❌ Article {article_num}: NOT FOUND")
            continue
        
        print(f"   📊 Found {len(matches)} matches")
        
        # Check each match
        correct_matches = 0
        for line_num, line in matches:
            if line.strip().startswith(f"Статья {article_num}:"):
                correct_matches += 1
                print(f"   ✅ Line {line_num}: CORRECT - {line[:100]}...")
            else:
                # Extract actual article number
                match = re.search(r'Статья (\d+):', line)
                actual_article = match.group(1) if match else "Unknown"
                print(f"   ❌ Line {line_num}: WRONG - Expected {article_num}, got {actual_article}")
                print(f"       Content: {line[:100]}...")
        
        if correct_matches > 0:
            print(f"   ✅ Article {article_num}: {correct_matches} correct matches found")
        else:
            print(f"   ❌ Article {article_num}: No correct matches found")
    
    print("\n" + "="*50)
    print("✅ Simple test completed!")


if __name__ == "__main__":
    test_article_retrieval()
