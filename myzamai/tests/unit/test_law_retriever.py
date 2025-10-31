"""
Unit tests for LawRetriever
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)


@pytest.mark.unit
class TestLawRetriever:
    """Tests for LawRetriever"""
    
    def test_initialization(self):
        """Test retriever initialization"""
        from src.core.law_retriever import LawRetriever
        
        index_dir = "/fake/path"
        retriever = LawRetriever(index_dir)
        
        assert retriever is not None
        assert retriever.index_dir == index_dir
        assert retriever.model_name == "sentence-transformers/all-MiniLM-L6-v2"
        assert retriever.model is None
        assert retriever.index is None
        assert retriever.chunks is None
    
    @patch('src.core.law_retriever.SentenceTransformer')
    @patch('src.core.law_retriever.faiss.read_index')
    @patch('src.core.law_retriever.pickle.load')
    @patch('builtins.open')
    def test_load(self, mock_open, mock_pickle, mock_faiss, mock_sentence):
        """Test loading FAISS index and chunks"""
        from src.core.law_retriever import LawRetriever
        
        # Setup mocks
        mock_model = Mock()
        mock_sentence.return_value = mock_model
        
        mock_index = Mock()
        mock_index.ntotal = 100
        mock_faiss.return_value = mock_index
        
        mock_chunks = ["chunk1", "chunk2", "chunk3"]
        mock_pickle.return_value = mock_chunks
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Mock file existence
        with patch('os.path.exists', return_value=True):
            retriever = LawRetriever("/fake/index_dir")
            retriever.load()
            
            assert retriever.model == mock_model
            assert retriever.index == mock_index
            assert retriever.chunks == mock_chunks
    
    @patch('os.path.exists')
    def test_load_index_not_found(self, mock_exists):
        """Test loading when index file doesn't exist"""
        from src.core.law_retriever import LawRetriever
        
        # Make index file not exist
        def exists_side_effect(path):
            return False
        
        mock_exists.side_effect = exists_side_effect
        
        retriever = LawRetriever("/fake/index_dir")
        
        with pytest.raises(FileNotFoundError):
            retriever.load()
    
    @patch('src.core.law_retriever.SentenceTransformer')
    @patch('src.core.law_retriever.faiss.read_index')
    @patch('src.core.law_retriever.pickle.load')
    @patch('builtins.open')
    def test_search(self, mock_open, mock_pickle, mock_faiss, mock_sentence):
        """Test search functionality"""
        from src.core.law_retriever import LawRetriever
        import numpy as np
        
        # Setup mocks
        mock_model = Mock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_sentence.return_value = mock_model
        
        mock_index = Mock()
        mock_index.ntotal = 10
        mock_index.search.return_value = (
            np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]]),  # distances
            np.array([[0, 1, 2, 3, 4, 5]])  # indices
        )
        mock_faiss.return_value = mock_index
        
        mock_chunks = [
            "Статья 22. О возврате товара",
            "Статья 23. О гарантии",
            "Статья 24. О продаже",
            "Статья 25. О договоре",
            "Статья 26. О оплате",
            "Статья 27. О доставке"
        ]
        mock_pickle.return_value = mock_chunks
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        with patch('os.path.exists', return_value=True):
            retriever = LawRetriever("/fake/index_dir")
            retriever.load()
            
            # Perform search
            query = "возврат товара"
            results = retriever.search(query, top_k=3)
            
            assert len(results) <= 3
            assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
            assert all(isinstance(r[0], str) for r in results)
            assert all(isinstance(r[1], (int, float)) for r in results)
    
    def test_format_results(self):
        """Test formatting search results"""
        from src.core.law_retriever import LawRetriever
        
        retriever = LawRetriever("/fake/path")
        
        results = [
            ("Статья 22. Текст статьи", 0.95),
            ("Статья 23. Другой текст", 0.87),
            ("Статья 24. Еще текст", 0.75)
        ]
        
        formatted = retriever.format_results(results)
        
        assert "Результат 1" in formatted
        assert "Результат 2" in formatted
        assert "Результат 3" in formatted
        assert "0.950" in formatted or "0.95" in formatted
        assert "Статья 22" in formatted
        assert len(formatted) > 0
    
    def test_format_results_empty(self):
        """Test formatting empty results"""
        from src.core.law_retriever import LawRetriever
        
        retriever = LawRetriever("/fake/path")
        
        results = []
        formatted = retriever.format_results(results)
        
        assert formatted == ""
    
    @patch('src.core.law_retriever.SentenceTransformer')
    @patch('src.core.law_retriever.faiss.read_index')
    @patch('src.core.law_retriever.pickle.load')
    @patch('builtins.open')
    def test_search_no_relevant_results(self, mock_open, mock_pickle, mock_faiss, mock_sentence):
        """Test search when no chunks match keywords"""
        from src.core.law_retriever import LawRetriever
        import numpy as np
        
        # Setup mocks
        mock_model = Mock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
        mock_sentence.return_value = mock_model
        
        mock_index = Mock()
        mock_index.ntotal = 10
        mock_index.search.return_value = (
            np.array([[0.1, 0.2, 0.3]]),  # distances
            np.array([[0, 1, 2]])  # indices
        )
        mock_faiss.return_value = mock_index
        
        # Chunks that don't match query keywords
        mock_chunks = [
            "Статья 100. О налогах",
            "Статья 101. О сборах",
            "Статья 102. О пошлинах"
        ]
        mock_pickle.return_value = mock_chunks
        
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        with patch('os.path.exists', return_value=True):
            retriever = LawRetriever("/fake/index_dir")
            retriever.load()
            
            # Search with query that doesn't match any keywords
            query = "возврат товара чек"
            results = retriever.search(query, top_k=3)
            
            # Should still return top 2 by similarity if no keyword matches
            assert len(results) > 0
            assert len(results) <= 3

