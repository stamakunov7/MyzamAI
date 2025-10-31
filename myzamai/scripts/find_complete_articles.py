#!/usr/bin/env python3
"""
Поиск полных статей в PDF файлах
Автоматическое исправление неполных статей
"""

import os
import re
import json
from typing import List, Dict, Tuple, Optional


class CompleteArticleFinder:
    """
    Находит полные версии статей в PDF файлах
    """
    
    def __init__(self, data_dir: str):
        """
        Initialize finder
        
        Args:
            data_dir: Directory containing PDF files
        """
        self.data_dir = data_dir
        self.pdf_files = [
            os.path.join(data_dir, 'civil_code_part1.pdf'),
            os.path.join(data_dir, 'civil_code_part2.pdf')
        ]
        self.chunks_file = os.path.join(data_dir, 'civil_code_chunks.txt')
        self.full_file = os.path.join(data_dir, 'civil_code_full.txt')
        
        # Articles to fix (priority list)
        self.priority_articles = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,  # Basic articles
            22, 222, 223, 226, 227, 232, 233,  # Property rights
            379, 380, 381, 382, 383, 384, 385,  # Contract law
            100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110  # General provisions
        ]
    
    def find_article_in_full_text(self, article_num: int) -> Optional[str]:
        """
        Ищет полную версию статьи в civil_code_full.txt
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Полный текст статьи или None
        """
        if not os.path.exists(self.full_file):
            print(f"❌ Full text file not found: {self.full_file}")
            return None
        
        print(f"🔍 Searching for Article {article_num} in full text...")
        
        with open(self.full_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all occurrences of the article
        pattern = f"Статья {article_num}"
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if pattern in line and line.strip().startswith(f"Статья {article_num}"):
                # Found the article, now get the complete text
                complete_text = self._extract_complete_article(lines, i, article_num)
                if complete_text and len(complete_text) > 100:  # Ensure it's substantial
                    print(f"✅ Found complete Article {article_num} ({len(complete_text)} chars)")
                    return complete_text
        
        print(f"❌ Article {article_num} not found in full text")
        return None
    
    def _extract_complete_article(self, lines: List[str], start_line: int, article_num: int) -> str:
        """
        Извлекает полный текст статьи начиная с указанной строки
        
        Args:
            lines: Все строки файла
            start_line: Номер начальной строки
            article_num: Номер статьи
            
        Returns:
            Полный текст статьи
        """
        article_lines = []
        current_line = start_line
        
        # Get the first line
        article_lines.append(lines[current_line])
        current_line += 1
        
        # Continue until we hit the next article or end of file
        while current_line < len(lines):
            line = lines[current_line].strip()
            
            # Check if this is the start of another article
            if line.startswith(f"Статья {article_num + 1}") or \
               (line.startswith("Статья") and not line.startswith(f"Статья {article_num}")):
                break
            
            # Check if this is a separator line
            if line.startswith("=" * 20):
                break
            
            # Add the line if it's not empty
            if line:
                article_lines.append(line)
            
            current_line += 1
        
        # Join all lines and clean up
        complete_text = " ".join(article_lines)
        complete_text = self._clean_article_text(complete_text)
        
        return complete_text
    
    def _clean_article_text(self, text: str) -> str:
        """
        Очищает текст статьи
        
        Args:
            text: Исходный текст
            
        Returns:
            Очищенный текст
        """
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove separators
        text = re.sub(r'=+', '', text)
        
        # Remove bullet points
        text = re.sub(r'^•\s*', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def check_article_completeness(self, article_num: int) -> Dict:
        """
        Проверяет полноту статьи
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Информация о полноте статьи
        """
        print(f"\n📚 Checking Article {article_num}:")
        
        # Check current version in chunks
        current_version = self._get_current_article(article_num)
        if not current_version:
            return {
                'article': article_num,
                'status': 'NOT_FOUND',
                'current_length': 0,
                'is_complete': False
            }
        
        # Check if current version is complete
        is_complete = self._is_article_complete(current_version)
        
        result = {
            'article': article_num,
            'status': 'COMPLETE' if is_complete else 'INCOMPLETE',
            'current_length': len(current_version),
            'is_complete': is_complete,
            'current_text': current_version[:200] + '...' if len(current_version) > 200 else current_version
        }
        
        if not is_complete:
            print(f"   ⚠️  Article {article_num}: INCOMPLETE ({len(current_version)} chars)")
            print(f"   📝 Current: {current_version[:100]}...")
            
            # Try to find complete version
            complete_version = self.find_article_in_full_text(article_num)
            if complete_version:
                result['complete_version'] = complete_version
                result['complete_length'] = len(complete_version)
                result['can_fix'] = True
                print(f"   ✅ Found complete version ({len(complete_version)} chars)")
            else:
                result['can_fix'] = False
                print(f"   ❌ Complete version not found")
        else:
            print(f"   ✅ Article {article_num}: COMPLETE ({len(current_version)} chars)")
        
        return result
    
    def _get_current_article(self, article_num: int) -> Optional[str]:
        """
        Получает текущую версию статьи из chunks файла
        
        Args:
            article_num: Номер статьи
            
        Returns:
            Текущий текст статьи или None
        """
        if not os.path.exists(self.chunks_file):
            return None
        
        with open(self.chunks_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith(f"Статья {article_num}:"):
                return line
        
        return None
    
    def _is_article_complete(self, text: str) -> bool:
        """
        Проверяет, полная ли статья
        
        Args:
            text: Текст статьи
            
        Returns:
            True если статья полная
        """
        # Remove article header
        content = re.sub(r'^Статья \d+: Статья \d+\. ', '', text)
        
        # Check for suspicious endings
        suspicious_endings = [
            r'применяются$',
            r'предусмотрены$',
            r'устанавливаются$',
            r'определяются$',
            r'регулируются$'
        ]
        
        for pattern in suspicious_endings:
            if re.search(pattern, content.strip()):
                return False
        
        # Check if ends with period
        if not content.strip().endswith('.'):
            return False
        
        # Check minimum length
        if len(content) < 100:
            return False
        
        return True
    
    def fix_priority_articles(self) -> Dict:
        """
        Исправляет приоритетные статьи
        
        Returns:
            Результаты исправления
        """
        print("🔧 Fixing priority articles...")
        
        results = {
            'total_checked': len(self.priority_articles),
            'fixed': 0,
            'already_complete': 0,
            'not_found': 0,
            'details': []
        }
        
        for article_num in self.priority_articles:
            print(f"\n{'='*50}")
            print(f"🔍 Processing Article {article_num}")
            print(f"{'='*50}")
            
            # Check current status
            status = self.check_article_completeness(article_num)
            results['details'].append(status)
            
            if status['status'] == 'COMPLETE':
                results['already_complete'] += 1
                print(f"✅ Article {article_num}: Already complete")
            elif status['status'] == 'NOT_FOUND':
                results['not_found'] += 1
                print(f"❌ Article {article_num}: Not found")
            elif status.get('can_fix', False):
                # Try to fix the article
                if self._fix_article(article_num, status['complete_version']):
                    results['fixed'] += 1
                    print(f"✅ Article {article_num}: Fixed successfully")
                else:
                    print(f"❌ Article {article_num}: Fix failed")
            else:
                print(f"⚠️  Article {article_num}: Cannot fix")
        
        return results
    
    def _fix_article(self, article_num: int, complete_text: str) -> bool:
        """
        Исправляет статью в chunks файле
        
        Args:
            article_num: Номер статьи
            complete_text: Полный текст статьи
            
        Returns:
            True если исправление успешно
        """
        try:
            # Read current file
            with open(self.chunks_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace the article
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                if line.strip().startswith(f"Статья {article_num}:"):
                    # Replace with complete version
                    new_lines.append(f"Статья {article_num}: {complete_text}")
                else:
                    new_lines.append(line)
            
            # Write back to file
            with open(self.chunks_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print(f"   📝 Article {article_num} updated in chunks file")
            return True
            
        except Exception as e:
            print(f"   ❌ Error fixing article {article_num}: {e}")
            return False
    
    def generate_report(self, results: Dict) -> str:
        """
        Генерирует отчет о результатах
        
        Args:
            results: Результаты исправления
            
        Returns:
            Текст отчета
        """
        report = f"""
📊 ARTICLE FIXING REPORT
{'='*50}
Total Articles Checked: {results['total_checked']}
✅ Already Complete: {results['already_complete']}
🔧 Fixed: {results['fixed']}
❌ Not Found: {results['not_found']}
⚠️  Cannot Fix: {results['total_checked'] - results['already_complete'] - results['fixed'] - results['not_found']}

📈 Success Rate: {(results['fixed'] + results['already_complete']) / results['total_checked'] * 100:.1f}%

📋 DETAILED RESULTS:
"""
        
        for detail in results['details']:
            status_icon = "✅" if detail['status'] == 'COMPLETE' else "🔧" if detail.get('can_fix', False) else "❌"
            report += f"{status_icon} Article {detail['article']}: {detail['status']} ({detail['current_length']} chars)\n"
        
        return report


def main():
    """
    Main function
    """
    print("🔍 Complete Article Finder")
    print("="*50)
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Initialize finder
    finder = CompleteArticleFinder(data_dir)
    
    # Fix priority articles
    results = finder.fix_priority_articles()
    
    # Generate report
    report = finder.generate_report(results)
    print("\n" + report)
    
    # Save results
    results_file = os.path.join(script_dir, 'article_fixing_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()
