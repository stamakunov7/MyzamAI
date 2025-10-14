"""
Pytest-compatible test suite for MyzamAI.

Unit tests for article matching and the strict matching fix for article 379 bug.
"""

import pytest
from typing import List, Optional


@pytest.mark.unit
@pytest.mark.article
class TestArticleMatcher:
    """Test class for article matching functionality."""
    
    def test_strict_article_matching_379_bug_fix(self):
        """
        Test the specific fix for article 379 bug.
        
        This test ensures that when searching for article 379,
        we don't accidentally match article 380 or other articles.
        """
        # Test data simulating the bug scenario
        test_chunks = [
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина 1. Обязательство прекращается смертью должника, если исполнение не может быть произведено без личного участия должника либо обязательство иным образом неразрывно связано с личностью должника. 2. Обязательство прекращается смертью кредитора, если исполнение предназначено лично для кредитора либо обязательство иным образом неразрывно связано с личностью кредитора.",
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица Обязательство прекращается ликвидацией юридического лица (должника или кредитора), кроме случаев, когда законодательством исполнение обязательства ликвидированного юридического лица возлагается на другое юридическое лицо (по обязательствам, возникающим вследствие причинения вреда жизни или здоровью и др.).",
            "Статья 381: Статья 381. Понятие договора 1. Договором признается соглашение двух или нескольких лиц об установлении, изменении или прекращении гражданских прав и обязанностей. 2. К обязательствам, возникшим из договора, применяются общие положения об обязательствах, поскольку иное не предусмотрено правилами настоящей главы и правилами об отдельных видах договоров, содержащимися в настоящем Кодексе. 3. К договорам, заключаемым более чем двумя сторонами (многосторонние договоры), общие положения о договоре применяются, если это не противоречит многостороннему характеру таких договоров."
        ]
        
        # Test strict matching for article 379
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 1, "Should find exactly one match for article 379"
        assert "смертью гражданина" in article_379_matches[0], "Should contain 'смертью гражданина'"
        assert "ликвидацией юридического лица" not in article_379_matches[0], "Should not contain content from article 380"
        
        # Test strict matching for article 380
        article_380_matches = self._find_strict_matches(test_chunks, 380)
        assert len(article_380_matches) == 1, "Should find exactly one match for article 380"
        assert "ликвидацией юридического лица" in article_380_matches[0], "Should contain 'ликвидацией юридического лица'"
        assert "смертью гражданина" not in article_380_matches[0], "Should not contain content from article 379"
        
        # Test strict matching for article 381
        article_381_matches = self._find_strict_matches(test_chunks, 381)
        assert len(article_381_matches) == 1, "Should find exactly one match for article 381"
        assert "Понятие договора" in article_381_matches[0], "Should contain 'Понятие договора'"
        assert "смертью гражданина" not in article_381_matches[0], "Should not contain content from article 379"
        assert "ликвидацией юридического лица" not in article_381_matches[0], "Should not contain content from article 380"
    
    def test_partial_match_prevention(self):
        """
        Test that partial matches are prevented.
        
        This ensures that searching for "Статья 37" doesn't match "Статья 379".
        """
        test_chunks = [
            "Статья 37: Статья 37. Неполная статья",
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина",
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица"
        ]
        
        # Test that searching for 37 doesn't match 379
        article_37_matches = self._find_strict_matches(test_chunks, 37)
        assert len(article_37_matches) == 1, "Should find exactly one match for article 37"
        assert "Неполная статья" in article_37_matches[0], "Should contain 'Неполная статья'"
        assert "смертью гражданина" not in article_37_matches[0], "Should not contain content from article 379"
        
        # Test that searching for 379 doesn't match 37
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 1, "Should find exactly one match for article 379"
        assert "смертью гражданина" in article_379_matches[0], "Should contain 'смертью гражданина'"
        assert "Неполная статья" not in article_379_matches[0], "Should not contain content from article 37"
    
    def test_edge_case_matching(self):
        """Test edge cases in article matching."""
        test_chunks = [
            "Статья 1: Статья 1. Отношения, регулируемые гражданским законодательством",
            "Статья 10: Статья 10. Осуществление гражданских прав",
            "Статья 100: Статья 100. Общие положения",
            "Статья 1000: Статья 1000. Специальные нормы"
        ]
        
        # Test single digit articles
        article_1_matches = self._find_strict_matches(test_chunks, 1)
        assert len(article_1_matches) == 1, "Should find exactly one match for article 1"
        assert "Отношения, регулируемые" in article_1_matches[0], "Should contain correct content"
        
        # Test double digit articles
        article_10_matches = self._find_strict_matches(test_chunks, 10)
        assert len(article_10_matches) == 1, "Should find exactly one match for article 10"
        assert "Осуществление гражданских прав" in article_10_matches[0], "Should contain correct content"
        
        # Test triple digit articles
        article_100_matches = self._find_strict_matches(test_chunks, 100)
        assert len(article_100_matches) == 1, "Should find exactly one match for article 100"
        assert "Общие положения" in article_100_matches[0], "Should contain correct content"
        
        # Test four digit articles
        article_1000_matches = self._find_strict_matches(test_chunks, 1000)
        assert len(article_1000_matches) == 1, "Should find exactly one match for article 1000"
        assert "Специальные нормы" in article_1000_matches[0], "Should contain correct content"
    
    def test_no_matches_found(self):
        """Test behavior when no matches are found."""
        test_chunks = [
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина",
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица"
        ]
        
        # Test non-existent article
        article_999_matches = self._find_strict_matches(test_chunks, 999)
        assert len(article_999_matches) == 0, "Should find no matches for non-existent article"
        
        # Test empty chunks
        empty_matches = self._find_strict_matches([], 379)
        assert len(empty_matches) == 0, "Should find no matches in empty chunks"
    
    def test_duplicate_article_handling(self):
        """Test handling of duplicate articles."""
        test_chunks = [
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина (Version 1)",
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина (Version 2)",
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица"
        ]
        
        # Test that duplicates are handled correctly
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 2, "Should find both versions of article 379"
        
        # Test that non-duplicate articles are not affected
        article_380_matches = self._find_strict_matches(test_chunks, 380)
        assert len(article_380_matches) == 1, "Should find exactly one match for article 380"
    
    def test_case_sensitivity(self):
        """Test case sensitivity in article matching."""
        test_chunks = [
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина",  # Normal case
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица",  # Normal case
            "Статья 381: Статья 381. Понятие договора"  # Normal case
        ]
        
        # Test that case doesn't affect matching
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 1, "Should find match regardless of case"
        
        article_380_matches = self._find_strict_matches(test_chunks, 380)
        assert len(article_380_matches) == 1, "Should find match regardless of case"
        
        article_381_matches = self._find_strict_matches(test_chunks, 381)
        assert len(article_381_matches) == 1, "Should find match regardless of case"
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in article matching."""
        test_chunks = [
            "  Статья 379: Статья 379. Прекращение обязательства смертью гражданина  ",  # Extra whitespace
            "\tСтатья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица\t",  # Tabs
            "Статья 381: Статья 381. Понятие договора"  # Normal
        ]
        
        # Test that whitespace doesn't affect matching
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 1, "Should find match despite extra whitespace"
        
        article_380_matches = self._find_strict_matches(test_chunks, 380)
        assert len(article_380_matches) == 1, "Should find match despite tabs"
        
        article_381_matches = self._find_strict_matches(test_chunks, 381)
        assert len(article_381_matches) == 1, "Should find match for normal case"
    
    def test_special_characters_handling(self):
        """Test handling of special characters in article matching."""
        test_chunks = [
            "Статья 379: Статья 379. Прекращение обязательства смертью гражданина (с изменениями)",
            "Статья 380: Статья 380. Прекращение обязательства ликвидацией юридического лица [исключена]",
            "Статья 381: Статья 381. Понятие договора «специальные термины»"
        ]
        
        # Test that special characters don't affect matching
        article_379_matches = self._find_strict_matches(test_chunks, 379)
        assert len(article_379_matches) == 1, "Should find match despite special characters"
        assert "смертью гражданина" in article_379_matches[0], "Should contain correct content"
        
        article_380_matches = self._find_strict_matches(test_chunks, 380)
        assert len(article_380_matches) == 1, "Should find match despite special characters"
        assert "ликвидацией юридического лица" in article_380_matches[0], "Should contain correct content"
        
        article_381_matches = self._find_strict_matches(test_chunks, 381)
        assert len(article_381_matches) == 1, "Should find match despite special characters"
        assert "Понятие договора" in article_381_matches[0], "Should contain correct content"
    
    # Helper methods
    def _find_strict_matches(self, chunks: List[str], article_num: int) -> List[str]:
        """
        Find strict matches for article number in chunks.
        
        This implements the strict matching logic that prevents partial matches.
        
        Args:
            chunks: List of text chunks to search
            article_num: Article number to search for
            
        Returns:
            List of matching chunks
        """
        matches = []
        
        for chunk in chunks:
            chunk_clean = chunk.strip()
            
            # Check if chunk starts with the exact article pattern
            if chunk_clean.startswith(f"Статья {article_num}:"):
                # Additional validation: ensure it's not a partial match
                # Check that the next character after the number is not a digit
                pattern = f"Статья {article_num}"
                if len(chunk_clean) > len(pattern):
                    next_char = chunk_clean[len(pattern)]
                    if next_char.isdigit():
                        # This is a partial match (e.g., "Статья 37" matches "Статья 379")
                        continue
                
                matches.append(chunk_clean)
        
        return matches
