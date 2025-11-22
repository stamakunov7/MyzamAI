# 🛠️ MyzamAI Development Guide

**Technical documentation for developers and contributors**

---

## 🧪 Testing

### Quick Start
```bash
# Run all tests with pytest
python scripts/run_pytest.py all

# Run specific test types
python scripts/run_pytest.py unit          # Unit tests only
python scripts/run_pytest.py integration  # Integration tests only
python scripts/run_pytest.py coverage     # With coverage report

# Or use pytest directly
cd myzamai
pytest tests/                             # All tests
pytest tests/unit/                        # Unit tests
pytest tests/integration/                 # Integration tests
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
- **Unit Tests**: 50+ tests (parser, matcher, performance, agents, retriever, LLM manager)
- **Integration Tests**: 2 test files (article accuracy, bot integration)
- **Coverage**: 90%+ code coverage (target: 95%)

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
cd myzamai
python scripts/check_and_build_index.py  # Smart builder (checks if exists)
# OR
python scripts/build_faiss_index.py     # Force rebuild
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
- **Retrieval Accuracy**: 99.16% (1,180/1,190 articles tested)
- **Test Coverage**: 90%+ (target: 95%)
- **Article Database**: 1,190 unique articles from Kyrgyz Civil Code

---

## 🚀 Deployment

### Railway Deployment

**Конфигурация:** `railway.json` в корне проекта

**Start Command:**
```bash
cd myzamai && python scripts/check_and_build_index.py && python src/bot/main.py
```

**Environment Variables (обязательные):**
- `TELEGRAM_BOT_TOKEN` - токен от @BotFather
- `HUGGINGFACE_API_TOKEN` - токен от Hugging Face

📖 **Полная инструкция:** см. [RAILWAY_DEPLOY.md](../../RAILWAY_DEPLOY.md) в корне проекта

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
- `src/` - Main application code
  - `bot/` - Telegram bot interface
  - `core/` - Business logic and agents
- `config/` - Configuration files
- `data/` - Legal documents and processed chunks
- `storage/` - Database and persistent storage
- `scripts/` - Utility scripts and tools
- `tests/` - Comprehensive test suite

---

**Last Updated**: October 2024  
**Version**: 3.0 (Hugging Face API)
