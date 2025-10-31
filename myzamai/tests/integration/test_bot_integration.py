"""
Pytest-compatible test suite for MyzamAI.

Integration tests for bot functionality and agent pipeline.
Migrated from test_bot_integration.py with pytest assertions.
"""

import pytest  # type: ignore[reportMissingImports]
import asyncio
from typing import Dict, List


@pytest.mark.integration
@pytest.mark.agent
class TestBotIntegration:
    """Test class for bot integration and agent pipeline."""
    
    @pytest.mark.asyncio
    async def test_law_command_379(self, bot_orchestrator):
        """
        Test /law 379 command returns correct article.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        article_text = bot_orchestrator.get_article_by_number(379)
        
        assert article_text is not None, "Article 379 should be found"
        assert article_text.startswith("Статья 379"), "Article 379 should start correctly"
        
        # Check for key terms
        assert "смертью" in article_text, "Article 379 should contain 'смертью'"
        assert "гражданина" in article_text, "Article 379 should contain 'гражданина'"
        assert "обязательство" in article_text, "Article 379 should contain 'обязательство'"
    
    @pytest.mark.asyncio
    async def test_law_command_380(self, bot_orchestrator):
        """Test /law 380 command returns correct article."""
        article_text = bot_orchestrator.get_article_by_number(380)
        
        assert article_text is not None, "Article 380 should be found"
        assert article_text.startswith("Статья 380"), "Article 380 should start correctly"
        
        # Check for key terms
        assert "ликвидацией" in article_text, "Article 380 should contain 'ликвидацией'"
        assert "юридического" in article_text, "Article 380 should contain 'юридического'"
        assert "лица" in article_text, "Article 380 should contain 'лица'"
    
    @pytest.mark.asyncio
    async def test_law_command_381(self, bot_orchestrator):
        """Test /law 381 command returns complete article."""
        article_text = bot_orchestrator.get_article_by_number(381)
        
        assert article_text is not None, "Article 381 should be found"
        assert article_text.startswith("Статья 381"), "Article 381 should start correctly"
        
        # Check for key content about contracts
        assert "договор" in article_text, \
            "Article 381 should contain 'договор'"
        assert "соглашение" in article_text, \
            "Article 381 should contain 'соглашение'"
    
    @pytest.mark.asyncio
    async def test_law_command_22(self, bot_orchestrator):
        """Test /law 22 command returns correct article."""
        article_text = bot_orchestrator.get_article_by_number(22)
        
        assert article_text is not None, "Article 22 should be found"
        assert article_text.startswith("Статья 22"), "Article 22 should start correctly"
        
        # Check for key terms about civil rights objects
        assert "объект" in article_text, "Article 22 should contain 'объект'"
        assert "гражданских" in article_text, "Article 22 should contain 'гражданских'"
        assert "прав" in article_text, "Article 22 should contain 'прав'"
    
    @pytest.mark.asyncio
    async def test_law_command_nonexistent(self, bot_orchestrator):
        """Test /law command with nonexistent article returns None."""
        article_text = bot_orchestrator.get_article_by_number(99999)
        
        assert article_text is None, "Nonexistent article should return None"
    
    @pytest.mark.asyncio
    async def test_law_command_invalid(self, bot_orchestrator):
        """Test /law command with invalid article number."""
        # This should raise an exception or return None
        try:
            article_text = bot_orchestrator.get_article_by_number(-1)
            assert article_text is None, "Invalid article number should return None"
        except (ValueError, TypeError):
            # Expected behavior for invalid input
            pass
    
    @pytest.mark.parametrize("article_num,expected_keywords", [
        (379, ["смертью", "гражданина", "обязательство"]),
        (380, ["ликвидацией", "юридического", "лица"]),
        (381, ["договор", "соглашение", "гражданских"]),
        (22, ["объект", "гражданских", "прав"]),
        (1, ["отношения", "гражданским", "законодательством"])
    ])
    @pytest.mark.asyncio
    async def test_law_command_keywords(self, bot_orchestrator, article_num, expected_keywords):
        """
        Test that law commands return articles with expected keywords.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            article_num: Article number to test
            expected_keywords: List of expected keywords
        """
        article_text = bot_orchestrator.get_article_by_number(article_num)
        
        if article_text is None:
            pytest.skip(f"Article {article_num} not found")
        
        for keyword in expected_keywords:
            assert keyword.lower() in article_text.lower(), \
                f"Article {article_num} should contain keyword '{keyword}'"
    
    @pytest.mark.asyncio
    async def test_query_processing_basic(self, bot_orchestrator, test_queries):
        """
        Test basic query processing through bot pipeline.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            test_queries: Test queries fixture
        """
        for query_data in test_queries:
            query = query_data['query']
            expected_keywords = query_data.get('expected_keywords', [])
            
            # Process query through bot pipeline
            try:
                response = await bot_orchestrator.process_query(query)
                
                assert response is not None, f"Response should not be None for query: {query}"
                assert len(response) > 50, f"Response should be substantial for query: {query}"
                
                # Check for expected keywords if specified
                if expected_keywords:
                    found_keywords = []
                    for keyword in expected_keywords:
                        if keyword.lower() in response.lower():
                            found_keywords.append(keyword)
                    
                    # At least 30% of keywords should be found
                    assert len(found_keywords) >= len(expected_keywords) * 0.3, \
                        f"Query '{query}' should contain at least 30% of expected keywords. " \
                        f"Found: {found_keywords}, Expected: {expected_keywords}"
                
            except Exception as e:
                pytest.fail(f"Query processing failed for '{query}': {e}")
    
    @pytest.mark.asyncio
    async def test_edge_cases(self, bot_orchestrator, edge_cases):
        """
        Test edge cases and error handling.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            edge_cases: Edge cases fixture
        """
        for case in edge_cases:
            name = case['name']
            query = case['query']
            expected_behavior = case['expected_behavior']
            
            try:
                if query.startswith('/law'):
                    # Handle law commands
                    article_num = query.split()[1]
                    try:
                        article_num = int(article_num)
                        response = bot_orchestrator.get_article_by_number(article_num)
                    except (ValueError, IndexError):
                        response = None
                else:
                    # Handle regular queries
                    response = await bot_orchestrator.process_query(query)
                
                # Validate based on expected behavior
                if expected_behavior == 'should_return_error':
                    assert response is None or 'не найдена' in response.lower() or 'ошибка' in response.lower(), \
                        f"Edge case '{name}' should return error"
                elif expected_behavior == 'should_handle_gracefully':
                    assert response is not None and len(response) > 0, \
                        f"Edge case '{name}' should handle gracefully"
                elif expected_behavior == 'should_reject_non_legal':
                    assert 'не относится к гражданскому праву' in (response or '').lower(), \
                        f"Edge case '{name}' should reject non-legal questions"
                
            except Exception as e:
                # Some edge cases might legitimately raise exceptions
                if expected_behavior == 'should_return_error':
                    pass  # Expected behavior
                else:
                    pytest.fail(f"Unexpected exception in edge case '{name}': {e}")
    
    @pytest.mark.asyncio
    async def test_response_format(self, bot_orchestrator):
        """
        Test that bot responses have proper format.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        # Test law command response format
        article_text = bot_orchestrator.get_article_by_number(381)
        assert article_text is not None, "Article 381 should be found"
        assert article_text.startswith("Статья 381"), "Response should start with article number"
        
        # Test query response format
        response = await bot_orchestrator.process_query("Что такое договор?")
        assert response is not None, "Query response should not be None"
        assert len(response) > 10, "Query response should have content"
    
    @pytest.mark.asyncio
    async def test_performance_basic(self, bot_orchestrator):
        """
        Test basic performance requirements.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        import time
        
        # Test article retrieval performance
        start_time = time.time()
        article_text = bot_orchestrator.get_article_by_number(381)
        end_time = time.time()
        
        retrieval_time = end_time - start_time
        assert retrieval_time < 5.0, f"Article retrieval should be fast (< 5s), got {retrieval_time:.2f}s"
        assert article_text is not None, "Article should be retrieved successfully"
        
        # Test query processing performance
        start_time = time.time()
        response = await bot_orchestrator.process_query("Что такое договор?")
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < 10.0, f"Query processing should be reasonable (< 10s), got {processing_time:.2f}s"
        assert response is not None, "Query should be processed successfully"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, bot_orchestrator):
        """
        Test handling of concurrent requests.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        # Test concurrent article retrievals
        import asyncio
        
        async def get_article(article_num):
            return bot_orchestrator.get_article_by_number(article_num)
        
        # Run multiple article retrievals concurrently
        tasks = [
            get_article(379),
            get_article(380),
            get_article(381),
            get_article(22)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check that all requests succeeded
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                pytest.fail(f"Concurrent request {i} failed: {result}")
            assert result is not None, f"Concurrent request {i} should return result"
    
    def test_bot_initialization(self, bot_orchestrator):
        """
        Test that bot initializes correctly.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        assert bot_orchestrator is not None, "Bot orchestrator should be initialized"
        
        # Test that retriever is available
        assert hasattr(bot_orchestrator, 'retriever'), "Bot should have retriever"
        assert bot_orchestrator.retriever is not None, "Retriever should be initialized"
        
        # Test that agents are available
        assert hasattr(bot_orchestrator, 'legal_expert'), "Bot should have legal expert"
        assert hasattr(bot_orchestrator, 'summarizer'), "Bot should have summarizer"
        assert hasattr(bot_orchestrator, 'translator'), "Bot should have translator"
        assert hasattr(bot_orchestrator, 'reviewer'), "Bot should have reviewer"
        assert hasattr(bot_orchestrator, 'ui_agent'), "Bot should have UI agent"
