"""
FAISS Index Builder for Legal Documents
Builds vector embeddings using sentence-transformers and creates FAISS index
"""

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class FAISSIndexBuilder:
    """
    Builds and manages FAISS index for legal document retrieval
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the FAISS index builder
        
        Args:
            model_name: HuggingFace model for embeddings
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 embedding size
        self.index = None
        self.chunks = []
        
    def chunk_text(self, text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            chunk_size: Maximum chunk size in characters
            overlap: Overlap between consecutive chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
        return chunks
    
    def load_legal_documents(self, data_path: str) -> List[str]:
        """
        Load and chunk legal documents
        
        Args:
            data_path: Path to legal document file
            
        Returns:
            List of document chunks
        """
        print(f"Loading legal documents from: {data_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split into articles for better granularity
        articles = []
        current_article = []
        
        for line in text.split('\n'):
            if line.strip().startswith('Статья'):
                if current_article:
                    articles.append('\n'.join(current_article))
                current_article = [line]
            else:
                current_article.append(line)
        
        if current_article:
            articles.append('\n'.join(current_article))
        
        print(f"Found {len(articles)} articles")
        
        # Use articles as chunks directly (no further chunking needed)
        all_chunks = []
        for article in articles:
            # Clean up article text
            article = article.strip()
            if article and len(article) > 10:  # Only include non-empty articles
                all_chunks.append(article)
        
        print(f"Total chunks after processing: {len(all_chunks)}")
        return all_chunks
    
    def build_index(self, chunks: List[str]) -> faiss.Index:
        """
        Build FAISS index from text chunks
        
        Args:
            chunks: List of text chunks
            
        Returns:
            FAISS index
        """
        print("Generating embeddings...")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')
        
        print(f"Building FAISS index with {len(embeddings)} vectors...")
        index = faiss.IndexFlatL2(self.dimension)
        index.add(embeddings)
        
        print(f"Index built successfully. Total vectors: {index.ntotal}")
        return index
    
    def save_index(self, index: faiss.Index, chunks: List[str], save_dir: str):
        """
        Save FAISS index and chunks to disk
        
        Args:
            index: FAISS index
            chunks: Text chunks
            save_dir: Directory to save index
        """
        os.makedirs(save_dir, exist_ok=True)
        
        index_path = os.path.join(save_dir, 'faiss_index.bin')
        chunks_path = os.path.join(save_dir, 'chunks.pkl')
        
        print(f"Saving index to: {index_path}")
        faiss.write_index(index, index_path)
        
        print(f"Saving chunks to: {chunks_path}")
        with open(chunks_path, 'wb') as f:
            pickle.dump(chunks, f)
        
        print("✓ Index and chunks saved successfully")
    
    def build_and_save(self, data_path: str, save_dir: str):
        """
        Complete pipeline: load, chunk, build index, and save
        
        Args:
            data_path: Path to legal document
            save_dir: Directory to save index
        """
        self.chunks = self.load_legal_documents(data_path)
        self.index = self.build_index(self.chunks)
        self.save_index(self.index, self.chunks, save_dir)


def main():
    """
    Main function to build FAISS index
    """
    # Get paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..')
    
    # Use the new full civil code file from PDF processing
    data_path = os.path.join(project_root, 'data', 'civil_code_full.txt')
    save_dir = os.path.join(project_root, 'storage', 'faiss_index')
    
    print("=" * 60)
    print("FAISS Index Builder for LegalBot+")
    print("=" * 60)
    
    builder = FAISSIndexBuilder()
    builder.build_and_save(data_path, save_dir)
    
    print("\n" + "=" * 60)
    print("✓ FAISS index built successfully!")
    print(f"Index saved to: {save_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()

