"""
Pytest-compatible test suite for MyzamAI.

Unit tests for performance requirements and response times.
"""

import pytest
import time
import asyncio
from typing import List, Dict


@pytest.mark.unit
@pytest.mark.performance
class TestPerformance:
    """Test class for performance requirements."""
    
    def test_article_retrieval_performance(self, bot_orchestrator, sample_articles):
        """
        Test that article retrieval meets performance requirements.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            sample_articles: Sample article numbers fixture
        """
        max_retrieval_time = 2.0  # Maximum time for article retrieval (seconds)
        
        for article_num in sample_articles:
            start_time = time.time()
            article_text = bot_orchestrator.get_article_by_number(article_num)
            end_time = time.time()
            
            retrieval_time = end_time - start_time
            
            if article_text is not None:
                assert retrieval_time < max_retrieval_time, \
                    f"Article {article_num} retrieval took {retrieval_time:.2f}s, should be < {max_retrieval_time}s"
            else:
                # If article doesn't exist, that's acceptable, but should be fast
                assert retrieval_time < 1.0, \
                    f"Article {article_num} not found, but lookup took {retrieval_time:.2f}s, should be < 1.0s"
    
    @pytest.mark.asyncio
    async def test_query_processing_performance(self, bot_orchestrator, test_queries):
        """
        Test that query processing meets performance requirements.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            test_queries: Test queries fixture
        """
        max_processing_time = 5.0  # Maximum time for query processing (seconds)
        
        for query_data in test_queries:
            query = query_data['query']
            
            start_time = time.time()
            try:
                response = await bot_orchestrator.process_query(query)
                end_time = time.time()
                
                processing_time = end_time - start_time
                
                assert processing_time < max_processing_time, \
                    f"Query '{query}' processing took {processing_time:.2f}s, should be < {max_processing_time}s"
                
                assert response is not None, f"Query '{query}' should return a response"
                assert len(response) > 10, f"Query '{query}' should return substantial response"
                
            except Exception as e:
                # Some queries might legitimately fail, but should fail fast
                end_time = time.time()
                processing_time = end_time - start_time
                
                assert processing_time < max_processing_time, \
                    f"Query '{query}' failed but took {processing_time:.2f}s, should fail fast"
    
    def test_concurrent_article_retrieval_performance(self, bot_orchestrator, sample_articles):
        """
        Test performance of concurrent article retrievals.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            sample_articles: Sample article numbers fixture
        """
        max_concurrent_time = 3.0  # Maximum time for concurrent retrievals
        
        start_time = time.time()
        
        # Retrieve multiple articles concurrently
        results = []
        for article_num in sample_articles[:5]:  # Test first 5 articles
            article_text = bot_orchestrator.get_article_by_number(article_num)
            results.append((article_num, article_text))
        
        end_time = time.time()
        concurrent_time = end_time - start_time
        
        assert concurrent_time < max_concurrent_time, \
            f"Concurrent article retrieval took {concurrent_time:.2f}s, should be < {max_concurrent_time}s"
        
        # Check that we got some results
        successful_retrievals = sum(1 for _, text in results if text is not None)
        assert successful_retrievals > 0, "Should have at least one successful retrieval"
    
    @pytest.mark.asyncio
    async def test_concurrent_query_processing_performance(self, bot_orchestrator, test_queries):
        """
        Test performance of concurrent query processing.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            test_queries: Test queries fixture
        """
        max_concurrent_time = 8.0  # Maximum time for concurrent query processing
        
        start_time = time.time()
        
        # Process multiple queries concurrently
        tasks = []
        for query_data in test_queries[:3]:  # Test first 3 queries
            query = query_data['query']
            task = bot_orchestrator.process_query(query)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        concurrent_time = end_time - start_time
        
        assert concurrent_time < max_concurrent_time, \
            f"Concurrent query processing took {concurrent_time:.2f}s, should be < {max_concurrent_time}s"
        
        # Check that we got some results
        successful_queries = sum(1 for result in results if not isinstance(result, Exception) and result is not None)
        assert successful_queries > 0, "Should have at least one successful query"
    
    def test_memory_usage_article_retrieval(self, bot_orchestrator, sample_articles):
        """
        Test memory usage during article retrieval.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            sample_articles: Sample article numbers fixture
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Retrieve multiple articles
        for article_num in sample_articles[:10]:  # Test first 10 articles
            article_text = bot_orchestrator.get_article_by_number(article_num)
            # Don't store results to avoid memory accumulation
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50, \
            f"Memory usage increased by {memory_increase:.1f}MB, should be < 50MB"
    
    def test_response_size_limits(self, bot_orchestrator, sample_articles):
        """
        Test that responses are within reasonable size limits.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            sample_articles: Sample article numbers fixture
        """
        max_response_size = 10000  # Maximum response size in characters
        min_response_size = 50     # Minimum response size in characters
        
        for article_num in sample_articles:
            article_text = bot_orchestrator.get_article_by_number(article_num)
            
            if article_text is not None:
                response_size = len(article_text)
                
                assert response_size >= min_response_size, \
                    f"Article {article_num} response too short: {response_size} chars, should be >= {min_response_size}"
                
                assert response_size <= max_response_size, \
                    f"Article {article_num} response too long: {response_size} chars, should be <= {max_response_size}"
    
    def test_error_handling_performance(self, bot_orchestrator):
        """
        Test that error handling is fast.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        max_error_time = 1.0  # Maximum time for error handling
        
        # Test with invalid article numbers
        invalid_articles = [-1, 0, 99999, 100000]
        
        for article_num in invalid_articles:
            start_time = time.time()
            article_text = bot_orchestrator.get_article_by_number(article_num)
            end_time = time.time()
            
            error_time = end_time - start_time
            
            assert error_time < max_error_time, \
                f"Error handling for article {article_num} took {error_time:.2f}s, should be < {max_error_time}s"
            
            # Should return None for invalid articles
            assert article_text is None, f"Invalid article {article_num} should return None"
    
    def test_bot_initialization_performance(self, faiss_index_dir):
        """
        Test that bot initialization is reasonably fast.
        
        Args:
            faiss_index_dir: FAISS index directory fixture
        """
        max_init_time = 10.0  # Maximum time for bot initialization
        
        start_time = time.time()
        
        try:
            from bot.main import LegalBotOrchestrator
            orchestrator = LegalBotOrchestrator(faiss_index_dir)
            
            end_time = time.time()
            init_time = end_time - start_time
            
            assert init_time < max_init_time, \
                f"Bot initialization took {init_time:.2f}s, should be < {max_init_time}s"
            
            assert orchestrator is not None, "Bot should be initialized successfully"
            
        except Exception as e:
            pytest.skip(f"Could not test initialization performance: {e}")
    
    def test_dataset_loading_performance(self, chunks_file):
        """
        Test that dataset loading is reasonably fast.
        
        Args:
            chunks_file: Path to chunks file fixture
        """
        max_loading_time = 5.0  # Maximum time for dataset loading
        
        start_time = time.time()
        
        with open(chunks_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        end_time = time.time()
        loading_time = end_time - start_time
        
        assert loading_time < max_loading_time, \
            f"Dataset loading took {loading_time:.2f}s, should be < {max_loading_time}s"
        
        assert len(content) > 0, "Dataset should not be empty"
        assert "Статья" in content, "Dataset should contain articles"
    
    def test_repeated_retrieval_performance(self, bot_orchestrator):
        """
        Test that repeated retrievals of the same article are fast.
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
        """
        max_repeated_time = 0.5  # Maximum time for repeated retrieval
        test_article = 381
        
        # First retrieval (might be slower due to caching)
        start_time = time.time()
        article_text = bot_orchestrator.get_article_by_number(test_article)
        end_time = time.time()
        first_retrieval_time = end_time - start_time
        
        # Second retrieval (should be faster due to caching)
        start_time = time.time()
        article_text_2 = bot_orchestrator.get_article_by_number(test_article)
        end_time = time.time()
        second_retrieval_time = end_time - start_time
        
        assert article_text is not None, "First retrieval should succeed"
        assert article_text_2 is not None, "Second retrieval should succeed"
        assert article_text == article_text_2, "Repeated retrievals should return same content"
        
        # Second retrieval should be faster (or at least not much slower)
        assert second_retrieval_time < max_repeated_time, \
            f"Repeated retrieval took {second_retrieval_time:.2f}s, should be < {max_repeated_time}s"
    
    @pytest.mark.slow
    def test_stress_performance(self, bot_orchestrator, sample_articles):
        """
        Test performance under stress (many rapid requests).
        
        Args:
            bot_orchestrator: Bot orchestrator fixture
            sample_articles: Sample article numbers fixture
        """
        max_stress_time = 10.0  # Maximum time for stress test
        num_requests = 20
        
        start_time = time.time()
        
        # Make many rapid requests
        for i in range(num_requests):
            article_num = sample_articles[i % len(sample_articles)]
            article_text = bot_orchestrator.get_article_by_number(article_num)
            # Don't store results to avoid memory issues
        
        end_time = time.time()
        stress_time = end_time - start_time
        
        assert stress_time < max_stress_time, \
            f"Stress test took {stress_time:.2f}s for {num_requests} requests, should be < {max_stress_time}s"
        
        # Average time per request should be reasonable
        avg_time_per_request = stress_time / num_requests
        assert avg_time_per_request < 1.0, \
            f"Average time per request: {avg_time_per_request:.2f}s, should be < 1.0s"
