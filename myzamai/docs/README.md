# 🤖 MyzamAI

**Multi-Agent Legal Chatbot powered by Hugging Face API**

MyzamAI (from the Kyrgyz word «Мыйзам», meaning 'Law') is an AI-powered legal assistant that answers questions about the Civil Code of the Kyrgyz Republic using a multi-agent architecture, FAISS vector search, and Hugging Face Inference API.

---

## ⚡ Features

- 🌐 **Hugging Face API** - Meta Llama 3 (8B-Instruct) via cloud inference
- 🔍 **FAISS Vector Search** - Fast semantic document retrieval
- 🎯 **6 Specialized Agents** - Legal Expert, Summarizer, Translator, Reviewer, UI, Retriever
- 📱 **Telegram Bot** - User-friendly interface
- 🌐 **Bilingual Support** - Russian/English with auto-detection
- 💾 **Conversation Memory** - Remembers user interactions
- ✅ **Quality Control** - Self-correction and review system
- ⚡ **Zero Local GPU Load** - All processing happens on HF servers

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- 2GB+ RAM (lightweight - no local models!)
- Internet connection (for HF API)
- Hugging Face API token

### Installation
```bash
# Clone repository
git clone https://github.com/stamakunov7/MyzamAI.git
cd MyzamAI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build FAISS index
python scripts/build_faiss_index.py
```

### Configuration
Create a `.env` file:
```bash
# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=your_token_from_botfather

# Hugging Face API Token (get from https://huggingface.co/settings/tokens)
HUGGINGFACE_API_TOKEN=hf_your_token_here
```

### Run Bot
```bash
python src/bot/main.py
```

---

## 💬 Usage

### Telegram Commands
- `/start` - Start conversation
- `/help` - Show help
- `/law <number>` - Get specific article (e.g., `/law 22`)

### Example Query
**User:**
```
Могу ли я вернуть товар без чека?
```

**MyzamAI:**
```
⚖️ Юридическая консультация

Ваш вопрос:
Могу ли я вернуть товар без чека?

Ответ:
Да, согласно статье 22 Гражданского кодекса КР, 
отсутствие кассового чека не является основанием 
для отказа. Вы можете ссылаться на свидетельские 
показания...

💡 Рекомендации:
• Сохраняйте все документы о покупке
• Товар должен быть в надлежащем состоянии
• Соберите свидетельские показания если нет чека
```

---

## 🧠 Tech Stack

### Core
- **LLM:** Meta Llama 3 (8B-Instruct) via Hugging Face Inference API
- **Vector DB:** FAISS with sentence-transformers
- **Framework:** Python 3.10+
- **Bot API:** python-telegram-bot

### Models & Services
- **Main LLM:** `meta-llama/Meta-Llama-3-8B-Instruct` (HF API)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local)
- **Translation:** `Helsinki-NLP/opus-mt-ru-en` & `opus-mt-en-ru` (local)

### Infrastructure
- ✅ **Cloud Inference** - All LLM processing on HF servers
- ✅ **Local Embeddings** - Only sentence-transformers runs locally
- ✅ **Lightweight** - Minimal resource usage

---

## 📁 Project Structure

```
MyzamAI/
├── src/
│   ├── bot/
│   │   └── main.py                  # Telegram bot + orchestrator
│   └── core/
│       ├── llm_manager.py           # Hugging Face API client wrapper
│       ├── law_retriever.py         # Document retrieval
│       └── agents/
│           ├── legal_expert.py      # Legal interpretation (HF API)
│           ├── summarizer.py        # Text summarization (HF API)
│           ├── translator.py        # RU↔EN translation
│           ├── reviewer_agent.py    # Quality control (HF API)
│           └── user_interface_agent.py  # Response formatting
│
├── config/
│   ├── config.py                    # Configuration & API tokens
│   └── railway.json                 # Railway deployment config
│
├── data/
│   ├── civil_code_full.txt          # Complete legal documents
│   └── civil_code_chunks.txt        # Processed chunks
│
├── storage/
│   ├── faiss_index/                 # Vector database
│   │   ├── faiss_index.bin         # FAISS index file
│   │   └── chunks.pkl              # Text chunks
│   └── memory.json                  # Conversation memory
│
├── scripts/
│   ├── build_faiss_index.py         # FAISS index builder
│   ├── check_incomplete_articles.py # Article validation
│   └── *.py                         # Other utility scripts
│
├── tests/                           # Test suite
├── docs/                            # Documentation
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

---

## 📊 Performance

| Component | Startup Time | Query Processing | Resource Usage |
|-----------|--------------|------------------|----------------|
| Bot Initialization | < 5s | - | 200MB RAM |
| FAISS Index Loading | < 2s | - | 100MB RAM |
| HF API Connection | < 1s | 2-5s | 0MB (cloud) |
| Embeddings (local) | < 3s | 0.5s | 500MB RAM |

**Total Memory Usage:** ~800MB (vs 8GB+ for local models)

---

## 🐛 Troubleshooting

### "FAISS index not found"
```bash
python scripts/build_faiss_index.py
```

### "Hugging Face API token not found"
1. Go to https://huggingface.co/settings/tokens
2. Create a new token (Read access)
3. Add to `.env` file: `HUGGINGFACE_API_TOKEN=hf_your_token_here`
4. Restart the bot

### "API rate limit exceeded"
- Wait a few minutes and try again
- Consider upgrading HF account for higher limits
- Reduce `max_new_tokens` in config

### "Telegram bot token not found"
1. Message @BotFather on Telegram
2. Create a new bot and get token
3. Add to `.env` file: `TELEGRAM_BOT_TOKEN=your_token`

---

## 📄 License

MIT License

---

## 📧 Contact

- **Email:** tstamakunov@stetson.edu
- **Issues:** GitHub Issues

---

## 🙏 Acknowledgments

- **Meta AI** - Llama 3 model
- **Hugging Face** - Inference API & Transformers library
- **Facebook AI** - FAISS vector search

---

**MyzamAI v3.0 - Powered by Meta Llama3 (Hugging Face API)** 🤖⚖️