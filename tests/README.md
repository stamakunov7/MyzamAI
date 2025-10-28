# 🧪 MyzamAI Test Suite

Pytest-compatible test suite for MyzamAI legal bot.

> **📖 For detailed testing documentation, see [DEVELOPMENT.md](../DEVELOPMENT.md)**

## 📁 Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── unit/                          # Unit tests (granular component tests)
│   ├── test_parser.py            # Article parsing and regex tests
│   ├── test_matcher.py           # Article matching and bug fix tests
│   └── test_performance.py       # Performance and response time tests
├── integration/                   # Integration tests (full pipeline tests)
│   ├── test_article_accuracy.py  # Article accuracy and completeness tests
│   └── test_bot_integration.py   # Bot integration and agent pipeline tests
└── README.md                      # This file
```

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements-test.txt
```

### Run Tests
```bash
# Run all tests
python run_pytest.py all

# Run unit tests only
python run_pytest.py unit

# Run integration tests only
python run_pytest.py integration

# Run with coverage
python run_pytest.py coverage
```

## 🎯 Test Categories

### Unit Tests (`tests/unit/`)
- **`test_parser.py`**: Article parsing, regex extraction, content validation
- **`test_matcher.py`**: Article matching, strict matching fix for article 379 bug
- **`test_performance.py`**: Response time, memory usage, concurrent performance

### Integration Tests (`tests/integration/`)
- **`test_article_accuracy.py`**: Article completeness, keyword validation, data quality
- **`test_bot_integration.py`**: Full bot pipeline, agent interactions, query processing

## 🏷️ Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit`: Unit-level tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.article`: Article-related tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.slow`: Slow tests (exclude with `-m "not slow"`)
- `@pytest.mark.quick`: Quick tests

## 🔧 Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_parser.py

# Run tests with specific marker
pytest -m unit
pytest -m integration
pytest -m article
pytest -m performance

# Run quick tests (exclude slow)
pytest -m "not slow"

# Run slow tests only
pytest -m slow
```

### Advanced Commands
```bash
# Run with coverage
pytest --cov=. --cov-report=html

# Run in parallel
pytest -n 4

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_parser.py::TestArticleParser::test_extract_article_number

# Run with HTML report
pytest --html=report.html
```

### Using the Runner Script
```bash
# Run all tests
python run_pytest.py all

# Run unit tests
python run_pytest.py unit -v

# Run with coverage
python run_pytest.py coverage

# Run in parallel
python run_pytest.py parallel -n 8

# Run performance tests
python run_pytest.py performance
```

## 📊 Test Coverage

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Generate terminal coverage report
pytest --cov=. --cov-report=term

# Generate XML coverage report
pytest --cov=. --cov-report=xml
```

### Coverage Targets
- **Unit Tests**: >90% coverage
- **Integration Tests**: >80% coverage
- **Overall**: >85% coverage

## 🎯 Test Scenarios

### Article Accuracy Tests
- ✅ Article 379 completeness (bug fix verification)
- ✅ Article 380 completeness
- ✅ Article 381 completeness
- ✅ No incomplete articles (suspicious endings)
- ✅ Minimum article length validation
- ✅ Proper punctuation validation

### Bot Integration Tests
- ✅ `/law` command functionality
- ✅ Query processing pipeline
- ✅ Edge case handling
- ✅ Error handling
- ✅ Response format validation

### Performance Tests
- ✅ Article retrieval < 2s
- ✅ Query processing < 5s
- ✅ Concurrent request handling
- ✅ Memory usage monitoring
- ✅ Response size limits

### Unit Tests
- ✅ Regex pattern matching
- ✅ Article number extraction
- ✅ Strict matching (379 bug fix)
- ✅ Content validation
- ✅ Error handling

## 🔍 Debugging Tests

### Run Single Test
```bash
pytest tests/unit/test_parser.py::TestArticleParser::test_extract_article_number -v
```

### Run with Debug Output
```bash
pytest -s -v tests/unit/test_parser.py
```

### Run with PDB Debugger
```bash
pytest --pdb tests/unit/test_parser.py
```

### Run with Logging
```bash
pytest --log-cli-level=DEBUG tests/integration/test_bot_integration.py
```

## 📈 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements-test.txt
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 🛠️ Fixtures

### Available Fixtures
- `data_dir`: Path to data directory
- `chunks_file`: Path to civil_code_chunks.txt
- `full_text_file`: Path to civil_code_full.txt
- `article_dataset`: Loaded article dataset
- `faiss_index_dir`: Path to FAISS index
- `bot_orchestrator`: Initialized bot instance
- `sample_articles`: Sample article numbers
- `critical_articles`: Critical articles with keywords
- `test_queries`: Test query data
- `edge_cases`: Edge case scenarios

### Using Fixtures
```python
def test_article_retrieval(bot_orchestrator, sample_articles):
    for article_num in sample_articles:
        article_text = bot_orchestrator.get_article_by_number(article_num)
        assert article_text is not None
```

## 🚨 Troubleshooting

### Common Issues

1. **FAISS Index Not Found**
   ```bash
   # Build FAISS index first
   python core/build_faiss_index.py
   ```

2. **Import Errors**
   ```bash
   # Install dependencies
   pip install -r requirements-test.txt
   ```

3. **Slow Tests**
   ```bash
   # Run only quick tests
   pytest -m "not slow"
   ```

4. **Memory Issues**
   ```bash
   # Run with memory profiling
   pytest --memray
   ```

### Test Data Requirements
- `data/civil_code_chunks.txt`: Article chunks file
- `data/civil_code_full.txt`: Full text file
- `faiss_index/faiss_index.bin`: FAISS index file

## 📝 Adding New Tests

### Unit Test Example
```python
@pytest.mark.unit
class TestNewFeature:
    def test_new_functionality(self):
        result = new_function()
        assert result == expected_result
```

### Integration Test Example
```python
@pytest.mark.integration
def test_new_integration(bot_orchestrator):
    response = await bot_orchestrator.process_query("test query")
    assert "expected" in response
```

## 🎉 Success Criteria

### Test Pass Requirements
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Performance tests meet requirements
- ✅ Coverage targets met
- ✅ No flaky tests

### Quality Gates
- **Unit Tests**: 100% pass rate
- **Integration Tests**: 100% pass rate
- **Performance Tests**: Meet time requirements
- **Coverage**: >85% overall
- **No Critical Issues**: Zero critical test failures

---

**MyzamAI Test Suite v1.0** 🧪⚖️
