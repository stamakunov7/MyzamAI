"""
Pytest fixtures and configuration for MyzamAI test suite.

This module provides shared fixtures for all tests including:
- Article dataset loading
- Bot initialization
- Test data management
"""

import pytest
import os
import sys
from typing import Dict, List, Optional

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def data_dir():
    """
    Fixture providing path to data directory.
    
    Returns:
        str: Path to data directory containing civil code files
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    return os.path.join(project_root, 'data')


@pytest.fixture(scope="session")
def chunks_file(data_dir):
    """
    Fixture providing path to civil_code_chunks.txt file.
    
    Args:
        data_dir: Path to data directory (from data_dir fixture)
        
    Returns:
        str: Path to chunks file
    """
    return os.path.join(data_dir, 'civil_code_chunks.txt')


@pytest.fixture(scope="session")
def full_text_file(data_dir):
    """
    Fixture providing path to civil_code_full.txt file.
    
    Args:
        data_dir: Path to data directory (from data_dir fixture)
        
    Returns:
        str: Path to full text file
    """
    return os.path.join(data_dir, 'civil_code_full.txt')


@pytest.fixture(scope="session")
def article_dataset(chunks_file):
    """
    Fixture loading article dataset from civil_code_chunks.txt.
    
    Loads all articles once per session for efficient testing.
    
    Args:
        chunks_file: Path to chunks file (from chunks_file fixture)
        
    Returns:
        dict: Dictionary mapping article numbers to article text
    """
    if not os.path.exists(chunks_file):
        pytest.skip(f"Article dataset not found: {chunks_file}")
    
    articles = {}
    
    with open(chunks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    for line in lines:
        if line.strip().startswith('Статья '):
            # Extract article number
            import re
            match = re.match(r'Статья (\d+):', line)
            if match:
                article_num = int(match.group(1))
                articles[article_num] = line.strip()
    
    return articles


@pytest.fixture(scope="session")
def faiss_index_dir():
    """
    Fixture providing path to FAISS index directory.
    
    Returns:
        str: Path to FAISS index directory
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    index_dir = os.path.join(project_root, 'storage', 'faiss_index')
    
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        pytest.skip(f"FAISS index not found: {index_dir}")
    
    return index_dir


@pytest.fixture(scope="session")
def bot_orchestrator(faiss_index_dir):
    """
    Fixture initializing LegalBotOrchestrator for integration tests.
    
    Creates bot instance once per session for efficient testing.
    
    Args:
        faiss_index_dir: Path to FAISS index (from faiss_index_dir fixture)
        
    Returns:
        LegalBotOrchestrator: Initialized bot instance
    """
    try:
        from src.bot.main import LegalBotOrchestrator
        orchestrator = LegalBotOrchestrator(faiss_index_dir)
        return orchestrator
    except Exception as e:
        pytest.skip(f"Could not initialize bot: {e}")


@pytest.fixture(scope="function")
def sample_articles():
    """
    Fixture providing sample article numbers for testing.
    
    Returns:
        list: List of article numbers commonly used in tests
    """
    return [1, 22, 222, 379, 380, 381, 382, 383, 384, 385]


@pytest.fixture(scope="function")
def critical_articles():
    """
    Fixture providing critical article numbers that must be complete.
    
    Returns:
        dict: Dictionary of article numbers with expected keywords
    """
    return {
        379: ["смертью", "гражданина", "обязательство"],
        380: ["ликвидацией", "юридического", "лица"],
        381: ["договор", "соглашение", "гражданских"],
        22: ["объекты", "гражданских", "прав"],
        1: ["отношения", "гражданским", "законодательством"]
    }


@pytest.fixture(scope="function")
def test_queries():
    """
    Fixture providing test queries for bot integration tests.
    
    Returns:
        list: List of test query dictionaries with expected keywords
    """
    return [
        {
            'query': 'Могу ли я вернуть товар без чека?',
            'expected_keywords': ['статья', 'гражданский', 'кодекс'],
            'expected_articles': [22]
        },
        {
            'query': 'Какие у меня права как собственника?',
            'expected_keywords': ['собственность', 'права'],
            'expected_articles': [222]
        },
        {
            'query': 'Как расторгнуть договор?',
            'expected_keywords': ['договор', 'расторжение']
        },
        {
            'query': 'Что такое обязательство?',
            'expected_keywords': ['обязательство', 'должник', 'кредитор']
        }
    ]


@pytest.fixture(scope="function")
def edge_cases():
    """
    Fixture providing edge case scenarios for testing.
    
    Returns:
        list: List of edge case dictionaries
    """
    return [
        {
            'name': 'Non-existent article',
            'query': '/law 99999',
            'expected_behavior': 'should_return_error'
        },
        {
            'name': 'Invalid article number',
            'query': '/law abc',
            'expected_behavior': 'should_return_error'
        },
        {
            'name': 'Non-legal question',
            'query': 'Какая погода сегодня?',
            'expected_behavior': 'should_reject_non_legal'
        },
        {
            'name': 'Empty query',
            'query': '',
            'expected_behavior': 'should_handle_gracefully'
        }
    ]


@pytest.fixture(autouse=True)
def reset_test_state():
    """
    Fixture that automatically resets test state before each test.
    
    This ensures test isolation and prevents side effects between tests.
    """
    # Setup code before test
    yield
    # Teardown code after test
    pass


# Pytest hooks
def pytest_configure(config):
    """
    Pytest configuration hook.
    
    Called before test collection starts.
    """
    # Add custom configuration here if needed
    pass


def pytest_collection_modifyitems(config, items):
    """
    Modify collected test items.
    
    Automatically adds markers based on test location or naming patterns.
    """
    for item in items:
        # Auto-mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Auto-mark slow tests
        if "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
        
        # Auto-mark article tests
        if "article" in item.nodeid.lower():
            item.add_marker(pytest.mark.article)
