# 🤖 MyzamAI

**Multi-Agent Legal Chatbot powered by Meta Llama 3**

MyzamAI (from the Kyrgyz word «Мыйзам», meaning 'Law') is an AI-powered legal assistant that answers questions about the Civil Code of the Kyrgyz Republic using a multi-agent architecture, FAISS vector search, and Meta Llama 3 from Hugging Face.

---

## ⚡ Features

- 🤖 **Meta Llama 3 (8B-Instruct)** - Centralized LLM for all agents
- 🔍 **FAISS Vector Search** - Fast semantic document retrieval
- 🎯 **6 Specialized Agents** - Legal Expert, Summarizer, Translator, Reviewer, UI, Retriever
- 📱 **Telegram Bot** - User-friendly interface
- 🌐 **Bilingual Support** - Russian/English with auto-detection
- 💾 **Conversation Memory** - Remembers user interactions
- ✅ **Quality Control** - Self-correction and review system
- 🍎 **Apple Silicon Support** - Optimized for M1/M2 Macs

---

## 🏗️ Architecture

```
User → Telegram Bot → Orchestrator
                          ↓
    ┌─────────────────────┴─────────────────────┐
    │                                            │
    ▼                                            ▼
Translator → LawRetriever (FAISS) → Legal Expert (Llama 3)
                                           ↓
                                      Reviewer (Llama 3)
                                           ↓
                                    Summarizer (Llama 3)
                                           ↓
                                       UI Agent
                                           ↓
                                   Formatted Response
```

### Centralized LLM Manager

All agents share a single **Meta Llama 3** instance via `core/llm_manager.py`:

```python
from core.llm_manager import llama

# Used by: LegalExpertAgent, SummarizerAgent, ReviewerAgent
response = llama(prompt)
result = response[0]["generated_text"]
```

---

## 📦 Installation

### Requirements

- Python 3.10+
- 8GB+ RAM (16GB recommended)
- CUDA GPU or Apple Silicon (optional, but recommended)

### Setup

```bash
# Clone repository
cd MyzamAI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build FAISS index
python core/build_faiss_index.py
```

---

## 🚀 Running the Bot

### Set Telegram Token

```bash
export TELEGRAM_BOT_TOKEN='your_token_from_botfather'
```

### Start Bot

```bash
python bot/main.py
```

The bot will:
1. Load Meta Llama 3 (8B-Instruct) model
2. Initialize all 6 agents
3. Load FAISS index
4. Start Telegram bot

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
- **LLM:** Meta Llama 3 (8B-Instruct) via Hugging Face Transformers
- **Vector DB:** FAISS with sentence-transformers
- **Framework:** Python 3.10+
- **Bot API:** python-telegram-bot

### Models
- **Main LLM:** `meta-llama/Meta-Llama-3-8B-Instruct`
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Translation:** `Helsinki-NLP/opus-mt-ru-en` & `opus-mt-en-ru`

### Device Support
- ✅ CUDA (NVIDIA GPUs)
- ✅ Apple Silicon (MPS for M1/M2/M3)
- ✅ CPU (fallback)

---

## 📁 Project Structure

```
MyzamAI/
├── core/
│   ├── llm_manager.py           # Hugging Face API client wrapper
│   ├── build_faiss_index.py     # FAISS index builder
│   ├── law_retriever.py         # Document retrieval
│   └── agents/
│       ├── legal_expert.py      # Legal interpretation (HF API)
│       ├── summarizer.py        # Text summarization (HF API)
│       ├── translator.py        # RU↔EN translation
│       ├── reviewer_agent.py    # Quality control (HF API)
│       └── user_interface_agent.py  # Response formatting
│
├── bot/
│   └── main.py                  # Telegram bot + orchestrator
│
├── data/
│   ├── civil_code_full.txt      # Complete legal documents
│   └── civil_code_chunks.txt    # Processed chunks
│
├── faiss_index/                 # Vector database
│   ├── faiss_index.bin         # FAISS index file
│   └── chunks.pkl              # Text chunks
│
├── tests/                       # Test suite
├── config.py                    # Configuration & API tokens
├── requirements.txt             # Dependencies
└── README.md
```

---

## 🔧 Configuration

### Llama 3 Settings

Edit `core/llm_manager.py`:

```python
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

llama = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,      # Adjust response length
    temperature=0.2,         # Lower = more focused
    top_p=0.9               # Nucleus sampling
)
```

### Device Selection

The system automatically detects:
1. **Apple Silicon (MPS)** - M1/M2/M3 Macs
2. **CUDA** - NVIDIA GPUs
3. **CPU** - Fallback

---

## 📊 Performance

| Component | CPU | GPU | Apple Silicon |
|-----------|-----|-----|---------------|
| Model Loading | 2min | 30s | 45s |
| Query Processing | 30-60s | 5-10s | 8-15s |
| Memory Usage | 10GB | 8GB VRAM | 8GB unified |

---

## 🐛 Troubleshooting

### "FAISS index not found"
```bash
python core/build_faiss_index.py
```

### "Out of memory"
- Use smaller batch sizes
- Enable CPU offloading in `llm_manager.py`
- Reduce `max_new_tokens` in pipeline config

### "Model download timeout"
```bash
export HF_HOME=/path/to/cache
huggingface-cli login  # If using gated models
```

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
- **Hugging Face** - Transformers library
- **Facebook AI** - FAISS vector search

---

**MyzamAI v2.0 - Powered by Meta Llama 3** 🤖⚖️
