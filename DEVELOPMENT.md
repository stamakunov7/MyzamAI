# 🛠️ MyzamAI Development Guide

**Technical documentation for developers and contributors**

---

## 🧪 Testing

### Quick Start
```bash
# Basic article test
python3 simple_test.py

# Comprehensive accuracy test
python3 run_all_tests.py

# Pytest suite
python3 run_pytest.py
```

### Test Structure
```
tests/
├── conftest.py                    # Pytest fixtures
├── unit/                          # Unit tests
│   ├── test_parser.py            # Article parsing
│   ├── test_matcher.py           # Article matching
│   └── test_performance.py       # Performance tests
└── integration/                   # Integration tests
    ├── test_article_accuracy.py  # Article accuracy
    └── test_bot_integration.py   # Bot integration
```

### Test Categories
- **Unit Tests**: 14 tests (parser, matcher, performance)
- **Integration Tests**: 2 test files (article accuracy, bot integration)
- **Coverage**: 85%+ code coverage

---

## 🔧 Troubleshooting

### Hugging Face API Issues

**Problem**: `ERROR: You are trying to access a gated repo`

**Solution**:
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (Read access)
3. Add to `.env` file: `HUGGINGFACE_API_TOKEN=hf_your_token_here`
4. Restart the bot

### FAISS Index Issues

**Problem**: `FAISS index not found`

**Solution**:
```bash
python core/build_faiss_index.py
```

### Telegram Bot Issues

**Problem**: `TELEGRAM_BOT_TOKEN not found`

**Solution**:
1. Message @BotFather on Telegram
2. Create a new bot and get token
3. Add to `.env` file: `TELEGRAM_BOT_TOKEN=your_token`

---

## 📊 Project Status

### ✅ Completed Features
- Multi-agent architecture with 6 specialized agents
- FAISS vector search for document retrieval
- Hugging Face API integration (Meta Llama 3)
- Telegram bot interface
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions

### 🔄 Recent Updates
- **Project Restructure**: Moved all files from `legalbot/` to root directory
- **API Migration**: Switched from local transformers to Hugging Face API
- **Documentation**: Consolidated all technical docs into this file

### 📈 Performance Metrics
- **Startup Time**: < 5s (vs 2min with local models)
- **Memory Usage**: ~800MB (vs 8GB+ with local models)
- **Query Processing**: 2-5s via HF API
- **Test Coverage**: 85%+

---

## 🚀 Deployment

### Railway Deployment
```json
{
  "startCommand": "python core/build_faiss_index.py && python bot/main.py",
  "restartPolicyType": "ON_FAILURE",
  "restartPolicyMaxRetries": 10
}
```

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=your_telegram_token
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

---

## 📝 Development Notes

### Architecture
- **LLM**: Meta Llama 3 (8B-Instruct) via Hugging Face API
- **Vector DB**: FAISS with sentence-transformers
- **Agents**: Legal Expert, Summarizer, Translator, Reviewer, UI, Retriever
- **Framework**: Python 3.10+ with python-telegram-bot

### Code Organization
- `core/` - Main business logic and agents
- `bot/` - Telegram bot interface
- `data/` - Legal documents and processed chunks
- `faiss_index/` - Vector database files
- `tests/` - Comprehensive test suite

---

**Last Updated**: October 2024  
**Version**: 3.0 (Hugging Face API)
