"""
Pytest-compatible test suite for MyzamAI.

Integration tests for article accuracy and retrieval.
Migrated from test_article_accuracy_simple.py with pytest assertions.
"""

import pytest
import re
from typing import Dict, List


@pytest.mark.integration
@pytest.mark.article
class TestArticleAccuracy:
    """Test class for article accuracy and retrieval."""
    
    def test_article_retrieval_basic(self, article_dataset, sample_articles):
        """
        Test basic article retrieval for common articles.
        
        Args:
            article_dataset: Article dataset fixture
            sample_articles: Sample article numbers fixture
        """
        for article_num in sample_articles:
            if article_num in article_dataset:
                article_text = article_dataset[article_num]
                
                # Assert article exists and has content
                assert article_text is not None, f"Article {article_num} should exist"
                assert len(article_text) > 50, f"Article {article_num} should have substantial content"
                
                # Assert article starts with correct number
                assert article_text.startswith(f"Статья {article_num}:"), \
                    f"Article {article_num} should start with 'Статья {article_num}:'"
    
    def test_article_379_completeness(self, article_dataset):
        """
        Test that article 379 is complete.

        This test specifically addresses the bug where article 379 was incomplete.
        """
        article_379 = article_dataset.get(379)
        assert article_379 is not None, "Article 379 should exist"

        # Check for key content about death and obligations
        assert "смертью" in article_379, \
            "Article 379 should contain 'смертью'"
        assert "обязательство" in article_379, \
            "Article 379 should contain 'обязательство'"
    
    def test_article_380_completeness(self, article_dataset):
        """Test that article 380 is complete."""
        article_380 = article_dataset.get(380)
        assert article_380 is not None, "Article 380 should exist"
        
        # Check for key terms
        assert "ликвидацией" in article_380, "Article 380 should contain 'ликвидацией'"
        assert "юридического" in article_380, "Article 380 should contain 'юридического'"
        assert "лица" in article_380, "Article 380 should contain 'лица'"
    
    def test_article_381_completeness(self, article_dataset):
        """Test that article 381 is complete."""
        article_381 = article_dataset.get(381)
        assert article_381 is not None, "Article 381 should exist"
        
        # Check for key terms
        assert "договор" in article_381, "Article 381 should contain 'договор'"
        assert "соглашение" in article_381, "Article 381 should contain 'соглашение'"
        assert "гражданских" in article_381, "Article 381 should contain 'гражданских'"
    
    def test_article_22_completeness(self, article_dataset):
        """Test that article 22 is complete."""
        article_22 = article_dataset.get(22)
        assert article_22 is not None, "Article 22 should exist"

        # Check for key terms about civil rights objects
        assert "объект" in article_22, "Article 22 should contain 'объект'"
        assert "гражданских" in article_22, "Article 22 should contain 'гражданских'"
        assert "прав" in article_22, "Article 22 should contain 'прав'"
    
    def test_no_incomplete_articles(self, article_dataset):
        """
        Test that articles don't end with suspicious incomplete patterns.
        
        This test helps identify articles that were cut off during processing.
        """
        suspicious_endings = [
            r'применяются$',
            r'предусмотрены$',
            r'устанавливаются$',
            r'определяются$',
            r'регулируются$'
        ]
        
        incomplete_articles = []
        
        for article_num, article_text in article_dataset.items():
            # Remove article header for content check
            content = re.sub(r'^Статья \d+: Статья \d+\. ', '', article_text)
            
            # Check for suspicious endings
            for pattern in suspicious_endings:
                if re.search(pattern, content.strip()):
                    incomplete_articles.append(article_num)
                    break
        
        # Allow some incomplete articles but flag if too many
        assert len(incomplete_articles) < len(article_dataset) * 0.1, \
            f"Found {len(incomplete_articles)} potentially incomplete articles: {incomplete_articles[:10]}"
    
    def test_article_minimum_length(self, article_dataset):
        """
        Test that articles have minimum required length.
        
        Very short articles might be incomplete or corrupted.
        """
        min_length = 100  # Minimum characters for a complete article
        
        short_articles = []
        for article_num, article_text in article_dataset.items():
            # Remove article header for content check
            content = re.sub(r'^Статья \d+: Статья \d+\. ', '', article_text)
            
            if len(content) < min_length:
                short_articles.append((article_num, len(content)))
        
        # Allow some short articles but flag if too many
        assert len(short_articles) < len(article_dataset) * 0.05, \
            f"Found {len(short_articles)} articles shorter than {min_length} chars: {short_articles[:5]}"
    
    def test_article_ends_with_period(self, article_dataset):
        """
        Test that articles end with proper punctuation.
        
        Articles should end with periods, not incomplete sentences.
        """
        articles_without_periods = []
        
        for article_num, article_text in article_dataset.items():
            # Remove article header for content check
            content = re.sub(r'^Статья \d+: Статья \d+\. ', '', article_text)
            
            if not content.strip().endswith('.'):
                articles_without_periods.append(article_num)
        
        # Allow some articles to not end with periods (e.g., excluded articles)
        # But flag if too many don't end properly
        assert len(articles_without_periods) < len(article_dataset) * 0.3, \
            f"Too many articles ({len(articles_without_periods)}) don't end with periods"
    
    @pytest.mark.parametrize("article_num,expected_keywords", [
        (379, ["смертью", "гражданина", "обязательство"]),
        (380, ["ликвидацией", "юридического", "лица"]),
        (381, ["договор", "соглашение", "гражданских"]),
        (22, ["объект", "гражданских", "прав"]),
        (1, ["селекционного", "достижения", "автор"])
    ])
    def test_article_keywords(self, article_dataset, article_num, expected_keywords):
        """
        Test that specific articles contain expected keywords.
        
        Args:
            article_dataset: Article dataset fixture
            article_num: Article number to test
            expected_keywords: List of keywords that should be present
        """
        article_text = article_dataset.get(article_num)
        assert article_text is not None, f"Article {article_num} should exist"
        
        for keyword in expected_keywords:
            assert keyword.lower() in article_text.lower(), \
                f"Article {article_num} should contain keyword '{keyword}'"
    
    def test_article_dataset_size(self, article_dataset):
        """
        Test that article dataset has reasonable size.
        
        Too few articles might indicate loading problems.
        """
        assert len(article_dataset) > 100, \
            f"Article dataset should contain more than 100 articles, got {len(article_dataset)}"
        
        # Check for some expected articles
        expected_articles = [1, 22, 379, 380, 381]
        for article_num in expected_articles:
            assert article_num in article_dataset, \
                f"Expected article {article_num} should be in dataset"
    
    def test_article_encoding(self, article_dataset):
        """
        Test that articles are properly encoded (no encoding issues).
        
        This helps identify corrupted text or encoding problems.
        """
        encoding_issues = []
        
        for article_num, article_text in article_dataset.items():
            # Check for real encoding issues (not just any special characters)
            # Look for actual encoding problems like replacement characters
            if '�' in article_text or '??' in article_text or '\\x' in article_text:
                encoding_issues.append(article_num)
        
        # Allow some encoding issues but flag if too many
        assert len(encoding_issues) < len(article_dataset) * 0.1, \
            f"Too many articles ({len(encoding_issues)}) have encoding issues: {encoding_issues[:5]}"
