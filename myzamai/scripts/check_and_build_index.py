"""
Smart FAISS index builder - checks if index exists before building
Optimized for Railway deployment
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scripts.build_faiss_index import FAISSIndexBuilder


def main():
    """
    Build FAISS index only if it doesn't exist
    """
    import sys
    import time
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..')
    
    index_dir = os.path.join(project_root, 'storage', 'faiss_index')
    index_path = os.path.join(index_dir, 'faiss_index.bin')
    chunks_path = os.path.join(index_dir, 'chunks.pkl')
    
    # Create storage directory if it doesn't exist
    os.makedirs(index_dir, exist_ok=True)
    
    # Check if index already exists
    if os.path.exists(index_path) and os.path.exists(chunks_path):
        print("=" * 60)
        print("✓ FAISS index already exists, skipping build")
        print(f"Index location: {index_path}")
        print("=" * 60)
        sys.stdout.flush()
        return 0
    
    # Index doesn't exist, build it
    print("=" * 60)
    print("FAISS index not found, building now...")
    print("This may take 5-15 minutes (downloading model + processing)...")
    print("=" * 60)
    sys.stdout.flush()
    
    data_path = os.path.join(project_root, 'data', 'civil_code_full.txt')
    
    if not os.path.exists(data_path):
        print(f"❌ ERROR: Data file not found: {data_path}")
        print("Please ensure data/civil_code_full.txt exists in the repository")
        return 1
    
    try:
        print("Step 1/4: Initializing FAISS builder...")
        sys.stdout.flush()
        builder = FAISSIndexBuilder()
        
        print("Step 2/4: Loading legal documents (this may take a moment)...")
        sys.stdout.flush()
        
        print("Step 3/4: Building FAISS index (this is the slow part)...")
        sys.stdout.flush()
        
        builder.build_and_save(data_path, index_dir)
        
        print("\n" + "=" * 60)
        print("✓ FAISS index built successfully!")
        print(f"Index saved to: {index_dir}")
        print("=" * 60)
        sys.stdout.flush()
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR building FAISS index: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

