#!/usr/bin/env python3
"""
Проверка неполных статей в базе данных
Ищет статьи, которые могут быть обрезаны
"""

import os
import re
from typing import List, Dict, Tuple


class ArticleCompletenessChecker:
    """
    Проверяет полноту статей в базе данных
    """
    
    def __init__(self, data_file_path: str):
        """
        Initialize checker
        
        Args:
            data_file_path: Path to civil_code_chunks.txt
        """
        self.data_file_path = data_file_path
        self.incomplete_articles = []
        self.suspicious_patterns = [
            r'применяются$',  # Ends with "применяются"
            r'предусмотрены$',  # Ends with "предусмотрены"
            r'устанавливаются$',  # Ends with "устанавливаются"
            r'определяются$',  # Ends with "определяются"
            r'регулируются$',  # Ends with "регулируются"
            r'осуществляются$',  # Ends with "осуществляются"
            r'устанавливается$',  # Ends with "устанавливается"
            r'определяется$',  # Ends with "определяется"
            r'регулируется$',  # Ends with "регулируется"
            r'осуществляется$',  # Ends with "осуществляется"
        ]
    
    def check_article_completeness(self) -> List[Dict]:
        """
        Проверяет полноту всех статей
        
        Returns:
            Список неполных статей
        """
        print("🔍 Checking article completeness...")
        
        if not os.path.exists(self.data_file_path):
            print(f"❌ Data file not found: {self.data_file_path}")
            return []
        
        # Read the data file
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        incomplete_articles = []
        
        # Find all article lines
        article_lines = []
        for i, line in enumerate(lines):
            if re.match(r'^Статья \d+:', line):
                article_lines.append((i, line))
        
        print(f"📊 Found {len(article_lines)} article lines")
        
        # Check each article
        for line_num, line in article_lines:
            # Extract article number
            match = re.match(r'^Статья (\d+):', line)
            if not match:
                continue
            
            article_num = int(match.group(1))
            
            # Check if article ends with suspicious patterns
            is_incomplete = self._check_article_incomplete(line)
            
            if is_incomplete:
                incomplete_articles.append({
                    'article': article_num,
                    'line': line_num,
                    'content': line,
                    'reason': 'Ends with incomplete sentence',
                    'suspicious_end': self._get_suspicious_end(line)
                })
                print(f"⚠️  Article {article_num}: POTENTIALLY INCOMPLETE")
                print(f"   Line {line_num}: {line[:100]}...")
                print(f"   Ends with: '{self._get_suspicious_end(line)}'")
        
        self.incomplete_articles = incomplete_articles
        return incomplete_articles
    
    def _check_article_incomplete(self, line: str) -> bool:
        """
        Проверяет, неполная ли статья
        
        Args:
            line: Строка со статьей
            
        Returns:
            True если статья неполная
        """
        # Remove the article header
        content = re.sub(r'^Статья \d+: Статья \d+\. ', '', line)
        
        # Check if ends with suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, content.strip()):
                return True
        
        # Check if ends with incomplete sentence (no period)
        if not content.strip().endswith('.'):
            return True
        
        # Check if very short (less than 100 characters after header)
        if len(content) < 100:
            return True
        
        return False
    
    def _get_suspicious_end(self, line: str) -> str:
        """
        Получает подозрительное окончание строки
        
        Args:
            line: Строка со статьей
            
        Returns:
            Последние 50 символов
        """
        content = re.sub(r'^Статья \d+: Статья \d+\. ', '', line)
        return content.strip()[-50:] if len(content) > 50 else content.strip()
    
    def check_specific_articles(self, article_numbers: List[int]) -> Dict:
        """
        Проверяет конкретные статьи
        
        Args:
            article_numbers: Список номеров статей для проверки
            
        Returns:
            Результаты проверки
        """
        print(f"\n🔍 Checking specific articles: {article_numbers}")
        
        if not os.path.exists(self.data_file_path):
            print(f"❌ Data file not found: {self.data_file_path}")
            return {}
        
        # Read the data file
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        results = {}
        
        for article_num in article_numbers:
            print(f"\n📚 Checking Article {article_num}:")
            
            # Find all lines with this article
            article_lines = []
            for i, line in enumerate(lines):
                if f"Статья {article_num}:" in line and line.strip().startswith(f"Статья {article_num}:"):
                    article_lines.append((i, line))
            
            if not article_lines:
                print(f"   ❌ Article {article_num}: NOT FOUND")
                results[article_num] = {
                    'status': 'NOT_FOUND',
                    'lines': 0,
                    'is_complete': False
                }
                continue
            
            print(f"   📊 Found {len(article_lines)} lines")
            
            # Check completeness
            is_complete = True
            for line_num, line in article_lines:
                if self._check_article_incomplete(line):
                    is_complete = False
                    print(f"   ⚠️  Line {line_num}: INCOMPLETE")
                    print(f"       Content: {line[:100]}...")
                    print(f"       Ends with: '{self._get_suspicious_end(line)}'")
                else:
                    print(f"   ✅ Line {line_num}: COMPLETE")
                    print(f"       Content: {line[:100]}...")
            
            results[article_num] = {
                'status': 'COMPLETE' if is_complete else 'INCOMPLETE',
                'lines': len(article_lines),
                'is_complete': is_complete
            }
        
        return results
    
    def generate_report(self) -> str:
        """
        Генерирует отчет о неполных статьях
        
        Returns:
            Текст отчета
        """
        if not self.incomplete_articles:
            return "✅ All articles appear to be complete!"
        
        report = f"🚨 Found {len(self.incomplete_articles)} potentially incomplete articles:\n\n"
        
        for article in self.incomplete_articles:
            report += f"📚 Article {article['article']}:\n"
            report += f"   Line: {article['line']}\n"
            report += f"   Reason: {article['reason']}\n"
            report += f"   Content: {article['content'][:100]}...\n"
            report += f"   Ends with: '{article['suspicious_end']}'\n\n"
        
        return report


def main():
    """
    Main function
    """
    print("🔍 Article Completeness Checker")
    print("="*50)
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'data', 'civil_code_chunks.txt')
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return
    
    # Initialize checker
    checker = ArticleCompletenessChecker(data_file)
    
    # Check all articles
    incomplete_articles = checker.check_article_completeness()
    
    # Check specific problematic articles
    problematic_articles = [379, 380, 381, 382, 383, 384, 385]
    specific_results = checker.check_specific_articles(problematic_articles)
    
    # Generate report
    report = checker.generate_report()
    print("\n" + "="*50)
    print("📊 COMPLETENESS REPORT")
    print("="*50)
    print(report)
    
    # Summary
    total_incomplete = len(incomplete_articles)
    total_checked = len(specific_results)
    incomplete_specific = sum(1 for r in specific_results.values() if not r['is_complete'])
    
    print(f"📈 SUMMARY:")
    print(f"   Total potentially incomplete articles: {total_incomplete}")
    print(f"   Specific articles checked: {total_checked}")
    print(f"   Incomplete specific articles: {incomplete_specific}")
    
    if total_incomplete == 0:
        print("🎉 All articles appear to be complete!")
    else:
        print("⚠️  Some articles may be incomplete. Review the report above.")
    
    return {
        'incomplete_articles': incomplete_articles,
        'specific_results': specific_results,
        'total_incomplete': total_incomplete
    }


if __name__ == "__main__":
    main()
