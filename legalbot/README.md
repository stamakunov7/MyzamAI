# 🤖 MyzamAI

**Intelligent Multi-Agent Legal Chatbot powered by Free Open-Source LLMs**

MyzamAI is a sophisticated AI-powered legal assistant that answers questions about the Civil Code of the Kyrgyz Republic using a multi-agent architecture, FAISS vector search, and state-of-the-art language models from Hugging Face.

---

## 🌟 Features

- ⚖️ **Legal Question Answering** - Answers legal questions based on Kyrgyz Civil Code
- 🤖 **Multi-Agent Architecture** - Specialized agents for retrieval, interpretation, summarization, translation, and review
- 🔍 **FAISS Vector Search** - Fast and accurate document retrieval
- 🌐 **Bilingual Support** - Works in Russian and English with automatic language detection
- 📱 **Telegram Integration** - User-friendly Telegram bot interface
- 💾 **Conversation Memory** - Remembers user interactions
- ✅ **Quality Control** - Automatic review and correction of responses
- 🆓 **100% Free & Open Source** - No API keys or paid services required

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    TELEGRAM USER                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                TELEGRAM BOT INTERFACE                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              MULTI-AGENT ORCHESTRATOR                   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Translator  │  │ LawRetriever │  │ Legal Expert │   │
│  │    Agent     │─>│   (FAISS)    │─>│    Agent     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│         │                                     │         │
│         │          ┌──────────────┐           │         │
│         │          │   Reviewer   │           │         │
│         │          │    Agent     │<──────────┘         │
│         │          └──────────────┘                     │
│         │                  │                            │
│         │          ┌──────────────┐                     │
│         └─────────>│ Summarizer   │                     │
│                    │    Agent     │                     │
│                    └──────────────┘                     │
│                            │                            │
│                    ┌──────────────┐                     │
│                    │  UI Agent    │                     │
│                    └──────────────┘                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    FORMATTED RESPONSE                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- 4GB+ RAM (8GB recommended for optimal performance)
- 10GB+ free disk space (for models)

### Step 1: Clone or Navigate to Project

```bash
cd legalbot
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `transformers` - HuggingFace transformers library
- `torch` - PyTorch for model inference
- `faiss-cpu` - Facebook AI Similarity Search
- `sentence-transformers` - Sentence embeddings
- `python-telegram-bot` - Telegram bot API
- `langchain` - LLM framework utilities
- `langdetect` - Language detection

---

## 🚀 Quick Start

### 1. Build FAISS Index

First, create the vector database from legal documents:

```bash
cd legalbot
python core/build_faiss_index.py
```

This will:
- Load the Civil Code from `data/civil_code.txt`
- Split it into chunks
- Generate embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Build and save FAISS index to `faiss_index/`

**Expected output:**
```
==============================================================
FAISS Index Builder for LegalBot+
==============================================================
Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
Loading legal documents from: ../data/civil_code.txt
Found 40 articles
Total chunks after processing: 40
Generating embeddings...
Building FAISS index with 40 vectors...
Index built successfully. Total vectors: 40
Saving index to: ../faiss_index/faiss_index.bin
✓ Index and chunks saved successfully
==============================================================
✓ FAISS index built successfully!
==============================================================
```

### 2. Test Individual Components

#### Test Law Retriever
```bash
python core/law_retriever.py
```

#### Test Legal Expert Agent
```bash
python core/agents/legal_expert.py
```

#### Test Translator
```bash
python core/agents/translator.py
```

### 3. Run the Bot

#### Option A: Demo Mode (Without Telegram)

```bash
cd bot
python main.py
```

This runs in demo mode and processes a test query to verify everything works.

#### Option B: Full Telegram Bot

1. **Get a Telegram Bot Token:**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy your bot token

2. **Set Environment Variable:**

```bash
export TELEGRAM_BOT_TOKEN='your_token_here'
```

On Windows:
```cmd
set TELEGRAM_BOT_TOKEN=your_token_here
```

3. **Run the Bot:**

```bash
python bot/main.py
```

4. **Start Chatting:**
   - Open Telegram
   - Search for your bot
   - Send `/start`
   - Ask legal questions!

---

## 💬 Usage Examples

### Example 1: Product Return Question

**User:** Могу ли я вернуть товар без чека?

**LegalBot+:**
```
⚖️ Юридическая консультация

Ваш вопрос:
Могу ли я вернуть товар без чека?

Ответ:
Да, согласно статье 22 Гражданского кодекса КР, отсутствие 
кассового или товарного чека не является основанием для отказа 
в удовлетворении требований потребителя. Вы можете ссылаться 
на свидетельские показания в подтверждение покупки.

📚 Правовая основа:
1. Статья 22. Отсутствие кассового или товарного чека...

💡 Рекомендации:
• Сохраняйте все документы о покупке
• Товар должен быть в надлежащем состоянии
• Соберите свидетельские показания если нет чека

⚠️ Данная информация носит справочный характер...
```

### Example 2: Contract Question (English)

**User:** What are the requirements for a valid contract?

**LegalBot+:** (Automatically detects English, translates query, retrieves articles, translates response back)

---

## 🎯 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show help and usage instructions |
| `/law <number>` | Get specific article by number (e.g., `/law 22`) |

---

## 🔧 Configuration

### Changing LLM Models

Edit the model names in the agent files:

**For Legal Expert & Reviewer:**
```python
# In core/agents/legal_expert.py
model_name = "HuggingFaceH4/zephyr-7b-beta"  # Default

# Alternative options:
# "mistralai/Mistral-7B-Instruct-v0.2"
# "microsoft/phi-2"
# "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

**For Embeddings:**
```python
# In core/build_faiss_index.py and core/law_retriever.py
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Default

# Alternative options:
# "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# "intfloat/multilingual-e5-small"
```

### Using GPU Acceleration

If you have NVIDIA GPU with CUDA:

```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

The code automatically detects and uses GPU if available.

---

## 📂 Project Structure

```
legalbot/
│
├── data/
│   └── civil_code.txt              # Legal documents (40 articles)
│
├── core/
│   ├── build_faiss_index.py        # FAISS index builder
│   ├── law_retriever.py            # Document retrieval via FAISS
│   │
│   └── agents/
│       ├── __init__.py
│       ├── legal_expert.py         # Legal interpretation
│       ├── summarizer.py           # Text summarization
│       ├── translator.py           # RU ↔ EN translation
│       ├── reviewer_agent.py       # Quality control
│       └── user_interface_agent.py # Response formatting
│
├── bot/
│   └── main.py                     # Telegram bot + orchestrator
│
├── faiss_index/                    # Generated FAISS index
│   ├── faiss_index.bin
│   └── chunks.pkl
│
├── memory.json                     # Conversation history (generated)
├── requirements.txt
└── README.md
```

---

## 🤖 Multi-Agent System

### 1. **LawRetriever Agent**
- Uses FAISS vector search
- Retrieves top-3 most relevant articles
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`

### 2. **Legal Expert Agent**
- Interprets legal texts
- Provides analysis in natural language
- Model: `HuggingFaceH4/zephyr-7b-beta`

### 3. **Summarizer Agent**
- Condenses long responses
- Ensures Telegram message limits
- Extractive + abstractive summarization

### 4. **Translator Agent**
- Translates RU ↔ EN
- Auto-detects language
- Models: `Helsinki-NLP/opus-mt-ru-en` and `opus-mt-en-ru`

### 5. **Reviewer Agent**
- Validates response quality
- Checks accuracy and relevance
- Self-correction loop

### 6. **User Interface Agent**
- Formats responses for Telegram
- Adds emojis and structure
- Context-aware recommendations

---

## 🎁 Bonus Features Implemented

✅ **Conversation Memory** - Stores last 20 queries per user in `memory.json`

✅ **Language Auto-Detection** - Automatically detects Russian or English

✅ **Specific Article Command** - Use `/law <number>` to fetch specific articles

✅ **Quality Review Logging** - Tracks problematic responses for improvement

✅ **Typing Indicator** - Shows "typing..." while processing

✅ **Context-Aware Tips** - Provides relevant advice based on query type

✅ **Graceful Fallbacks** - Works even if some models fail to load

---

## 🐛 Troubleshooting

### Issue: FAISS Index Not Found

**Solution:**
```bash
python core/build_faiss_index.py
```

### Issue: Out of Memory

**Solution:** Use lighter models:
```python
# In legal_expert.py, change to:
model_name = "microsoft/phi-2"  # Smaller 2.7B model
```

### Issue: Slow Response Times

**Solutions:**
1. Use GPU if available
2. Reduce `top_k` in retriever (default: 3)
3. Disable LLM review in `reviewer_agent.py`
4. Use quantized models (4-bit or 8-bit)

### Issue: Telegram Bot Won't Start

**Solution:** Verify token is set:
```bash
echo $TELEGRAM_BOT_TOKEN  # Should show your token
```

---

## 🔬 Technical Details

### Embedding Model
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384
- **Speed:** ~1000 sentences/second on CPU
- **Languages:** 100+ languages

### LLM Backbone
- **Model:** `HuggingFaceH4/zephyr-7b-beta` (7B parameters)
- **Context:** 4096 tokens
- **Format:** ChatML template
- **Inference:** FP16 on GPU, FP32 on CPU

### Vector Database
- **Engine:** FAISS (Facebook AI Similarity Search)
- **Index Type:** IndexFlatL2 (exact search)
- **Distance:** L2 (Euclidean)

### Chunking Strategy
- **Size:** 700 characters per chunk
- **Overlap:** 100 characters
- **Boundary:** Sentence-aware splitting

---

## 📊 Performance Metrics

| Component | Time (CPU) | Time (GPU) |
|-----------|------------|------------|
| Document Retrieval | ~0.5s | ~0.2s |
| Legal Expert | ~10-30s | ~3-5s |
| Summarization | ~5-15s | ~2-3s |
| Translation | ~2-5s | ~1-2s |
| Review | ~5-10s | ~2-3s |
| **Total** | **~30-60s** | **~8-15s** |

*Measurements on Intel i7 CPU and NVIDIA RTX 3060*

---

## 🚀 Deployment Options

### Local
```bash
python bot/main.py
```

### Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN python core/build_faiss_index.py

CMD ["python", "bot/main.py"]
```

### Cloud (Railway, Render, Fly.io)
1. Add `Procfile`:
```
bot: python bot/main.py
```

2. Set environment variables in dashboard:
```
TELEGRAM_BOT_TOKEN=your_token
```

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more legal documents
- [ ] Support other languages
- [ ] Implement RAG with larger context
- [ ] Add voice message support
- [ ] Create web interface
- [ ] Fine-tune models on legal texts
- [ ] Add citation verification

---

## 📧 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Email: support@legalbot.example

---

## 🙏 Acknowledgments

- **HuggingFace** - For free, open-source models
- **Facebook AI** - For FAISS vector search
- **Sentence Transformers** - For embedding models
- **Python Telegram Bot** - For Telegram integration

---

## 📈 Roadmap

- **v1.0** ✅ - Basic multi-agent system with Telegram integration
- **v1.1** 🔄 - Voice message support
- **v1.2** 📅 - Web interface with Streamlit
- **v2.0** 📅 - Fine-tuned legal models
- **v2.1** 📅 - Multi-document support (Criminal Code, Tax Code, etc.)

---

## ⚠️ Disclaimer

LegalBot+ provides general legal information based on the Civil Code of the Kyrgyz Republic. This information is for educational purposes only and should not be considered professional legal advice. Always consult with a qualified attorney for specific legal matters.

---

**Made with ❤️ and 🤖 AI**

**LegalBot+ v1.0**

