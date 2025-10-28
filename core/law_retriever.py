"""
Law Retriever - Searches relevant laws using FAISS vector database
"""

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class LawRetriever:
    """
    Retrieves relevant legal articles using FAISS similarity search
    """
    
    def __init__(self, index_dir: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the Law Retriever
        
        Args:
            index_dir: Directory containing FAISS index and chunks
            model_name: Embedding model name
        """
        self.model_name = model_name
        self.index_dir = index_dir
        self.model = None
        self.index = None
        self.chunks = None
        
    def load(self):
        """
        Load FAISS index and chunks from disk
        """
        if self.model is None:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        
        index_path = os.path.join(self.index_dir, 'faiss_index.bin')
        chunks_path = os.path.join(self.index_dir, 'chunks.pkl')
        
        if not os.path.exists(index_path):
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. "
                "Please run build_faiss_index.py first."
            )
        
        print(f"Loading FAISS index from: {index_path}")
        self.index = faiss.read_index(index_path)
        
        print(f"Loading chunks from: {chunks_path}")
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)
        
        print(f"✓ Loaded index with {self.index.ntotal} vectors and {len(self.chunks)} chunks")
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for relevant legal articles
        
        Args:
            query: User query
            top_k: Number of top results to return
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        if self.index is None or self.chunks is None:
            self.load()
        
        # Generate query embedding
        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector).astype('float32')
        
        # Search in FAISS index (get more results for filtering)
        distances, indices = self.index.search(query_vector, top_k * 2)
        
        # Prepare results with relevance filtering
        results = []
        query_words = [word.lower() for word in query.split() if len(word) > 3]
        
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                chunk_lower = chunk.lower()
                
                # Check if chunk contains key words from query
                relevance_score = sum(1 for word in query_words if word in chunk_lower)
                
                # Only include if at least one key word matches or it's in top 2 by similarity
                if relevance_score > 0 or len(results) < 2:
                    similarity = 1 / (1 + distance)  # Convert distance to similarity
                    results.append((chunk, similarity))
                
                # Stop when we have enough relevant results
                if len(results) >= top_k:
                    break
        
        # If no results passed the filter, return top 2 by similarity
        if not results:
            for idx, distance in zip(indices[0][:2], distances[0][:2]):
                if idx < len(self.chunks):
                    chunk = self.chunks[idx]
                    similarity = 1 / (1 + distance)
                    results.append((chunk, similarity))
        
        return results[:top_k]
    
    def format_results(self, results: List[Tuple[str, float]]) -> str:
        """
        Format search results into readable text
        
        Args:
            results: List of (chunk, score) tuples
            
        Returns:
            Formatted string
        """
        formatted = []
        for i, (chunk, score) in enumerate(results, 1):
            formatted.append(f"[Результат {i}] (релевантность: {score:.3f})")
            formatted.append(chunk)
            formatted.append("-" * 60)
        
        return "\n".join(formatted)


def main():
    """
    Test the law retriever
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    index_dir = os.path.join(project_root, 'faiss_index')
    
    print("=" * 60)
    print("Law Retriever Test")
    print("=" * 60)
    
    retriever = LawRetriever(index_dir)
    
    # Test query
    test_query = "Могу ли я вернуть товар без чека?"
    print(f"\nQuery: {test_query}\n")
    
    results = retriever.search(test_query, top_k=3)
    print(retriever.format_results(results))


if __name__ == "__main__":
    main()

