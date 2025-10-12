"""
Test script to verify LegalBot+ system components
Run this after installation to ensure everything works
"""

import os
import sys
import asyncio

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required packages are installed"""
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)
    
    try:
        import torch
        print("✓ PyTorch:", torch.__version__)
    except ImportError as e:
        print("✗ PyTorch not found:", e)
        return False
    
    try:
        import transformers
        print("✓ Transformers:", transformers.__version__)
    except ImportError as e:
        print("✗ Transformers not found:", e)
        return False
    
    try:
        import faiss
        print("✓ FAISS: OK")
    except ImportError as e:
        print("✗ FAISS not found:", e)
        return False
    
    try:
        import sentence_transformers
        print("✓ Sentence Transformers:", sentence_transformers.__version__)
    except ImportError as e:
        print("✗ Sentence Transformers not found:", e)
        return False
    
    try:
        import telegram
        print("✓ Python-Telegram-Bot:", telegram.__version__)
    except ImportError as e:
        print("✗ Python-Telegram-Bot not found:", e)
        return False
    
    print("\n✓ All imports successful!\n")
    return True


def test_data_files():
    """Test that required data files exist"""
    print("=" * 60)
    print("Testing data files...")
    print("=" * 60)
    
    civil_code_path = os.path.join(os.path.dirname(__file__), 'data', 'civil_code.txt')
    
    if os.path.exists(civil_code_path):
        with open(civil_code_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"✓ Civil Code found: {len(content)} characters")
    else:
        print(f"✗ Civil Code not found at {civil_code_path}")
        return False
    
    print("\n✓ Data files OK!\n")
    return True


def test_faiss_index():
    """Test FAISS index"""
    print("=" * 60)
    print("Testing FAISS index...")
    print("=" * 60)
    
    index_dir = os.path.join(os.path.dirname(__file__), 'faiss_index')
    index_path = os.path.join(index_dir, 'faiss_index.bin')
    chunks_path = os.path.join(index_dir, 'chunks.pkl')
    
    if not os.path.exists(index_path):
        print(f"✗ FAISS index not found at {index_path}")
        print("Please run: python core/build_faiss_index.py")
        return False
    
    if not os.path.exists(chunks_path):
        print(f"✗ Chunks file not found at {chunks_path}")
        return False
    
    print("✓ FAISS index files found")
    
    try:
        from core.law_retriever import LawRetriever
        retriever = LawRetriever(index_dir)
        retriever.load()
        print(f"✓ FAISS index loaded successfully")
        print(f"✓ Total vectors: {retriever.index.ntotal}")
        print(f"✓ Total chunks: {len(retriever.chunks)}")
    except Exception as e:
        print(f"✗ Error loading FAISS index: {e}")
        return False
    
    print("\n✓ FAISS index OK!\n")
    return True


def test_retriever():
    """Test law retriever"""
    print("=" * 60)
    print("Testing Law Retriever...")
    print("=" * 60)
    
    try:
        from core.law_retriever import LawRetriever
        
        index_dir = os.path.join(os.path.dirname(__file__), 'faiss_index')
        retriever = LawRetriever(index_dir)
        
        test_query = "возврат товара без чека"
        print(f"Test query: '{test_query}'")
        
        results = retriever.search(test_query, top_k=2)
        print(f"✓ Retrieved {len(results)} results")
        
        for i, (chunk, score) in enumerate(results, 1):
            print(f"\nResult {i} (score: {score:.3f}):")
            print(chunk[:200] + "...")
        
    except Exception as e:
        print(f"✗ Error testing retriever: {e}")
        return False
    
    print("\n✓ Law Retriever OK!\n")
    return True


def test_agents():
    """Test individual agents"""
    print("=" * 60)
    print("Testing Agents...")
    print("=" * 60)
    
    # Test Translator
    try:
        from core.agents.translator import TranslatorAgent
        translator = TranslatorAgent()
        
        test_text = "Это тестовый текст"
        detected_lang = translator.detect_language(test_text)
        print(f"✓ Translator Agent: Language detected as '{detected_lang}'")
    except Exception as e:
        print(f"✗ Translator Agent error: {e}")
        return False
    
    # Test UI Agent
    try:
        from core.agents.user_interface_agent import UserInterfaceAgent
        ui_agent = UserInterfaceAgent()
        
        welcome = ui_agent.format_welcome()
        print(f"✓ UI Agent: Welcome message generated ({len(welcome)} chars)")
    except Exception as e:
        print(f"✗ UI Agent error: {e}")
        return False
    
    print("\n✓ All agents initialized successfully!\n")
    return True


async def test_orchestrator():
    """Test the full orchestrator"""
    print("=" * 60)
    print("Testing Orchestrator (Full Pipeline)...")
    print("=" * 60)
    
    try:
        from bot.main import LegalBotOrchestrator
        
        index_dir = os.path.join(os.path.dirname(__file__), 'faiss_index')
        orchestrator = LegalBotOrchestrator(index_dir)
        
        test_query = "Могу ли я вернуть товар без чека?"
        print(f"Test query: '{test_query}'")
        print("\nProcessing (this may take a while on first run)...\n")
        
        response = await orchestrator.process_query(test_query, user_id="test_user")
        
        print("Response received:")
        print("-" * 60)
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 60)
        
        print("\n✓ Orchestrator working!\n")
        
    except Exception as e:
        print(f"✗ Orchestrator error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("LegalBot+ System Test")
    print("=" * 60 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Data Files", test_data_files),
        ("FAISS Index", test_faiss_index),
        ("Law Retriever", test_retriever),
        ("Agents", test_agents),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} test failed with exception: {e}\n")
            results[test_name] = False
    
    # Test orchestrator (may take a while)
    print("\n⚠️  The next test will download models if not cached (may take several minutes)")
    user_input = input("Run full orchestrator test? (y/n): ")
    
    if user_input.lower() == 'y':
        try:
            results["Orchestrator"] = asyncio.run(test_orchestrator())
        except Exception as e:
            print(f"\n✗ Orchestrator test failed: {e}\n")
            results["Orchestrator"] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour LegalBot+ system is ready to use!")
        print("\nNext steps:")
        print("1. Set your Telegram bot token:")
        print("   export TELEGRAM_BOT_TOKEN='your_token'")
        print("2. Run the bot:")
        print("   python bot/main.py")
    else:
        print("\n" + "=" * 60)
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the bot.")
    
    print()


if __name__ == "__main__":
    main()

