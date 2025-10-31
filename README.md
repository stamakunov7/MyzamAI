# 🤖 MyzamAI

**Multi-Agent Legal Chatbot powered by Meta Llama3 (Hugging Face API)**

MyzamAI (from the Kyrgyz word «Мыйзам», meaning 'Law') is an AI-powered legal assistant that answers questions about the Civil Code of the Kyrgyz Republic.

**Link:**
https://t.me/myzam_ai_bot

## 📁 Project Structure

```
MyzamAI/
├── 📁 src/                    # Main application code
│   ├── bot/                   # Telegram bot interface
│   └── core/                  # Core business logic & agents
├── 📁 config/                 # Configuration files
├── 📁 data/                   # Legal documents & data
├── 📁 storage/                # Database & persistent storage
├── 📁 scripts/                # Utility scripts & tools
├── 📁 tests/                  # Test suite
├── 📁 docs/                   # Documentation
├── requirements.txt           # Dependencies
└── LICENSE                    # MIT License
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp config/config.py.example config/config.py
   # Edit config/config.py with your API tokens
   ```

3. **Build FAISS index:**
   ```bash
   python scripts/build_faiss_index.py
   ```

4. **Run bot:**
   ```bash
   python src/bot/main.py
   ```

## 📖 Documentation

- **[📖 User Guide](docs/README.md)** - Complete user documentation
- **[🛠️ Developer Guide](docs/DEVELOPMENT.md)** - Technical documentation
- **[🧪 Testing Guide](tests/README.md)** - Test suite documentation

## 💬 Usage

Start a conversation with the bot on Telegram:
- `/start` - Begin
- `/help` - Show commands
- `/law <number>` - Get specific article

## 🤝 Contributing

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for development guidelines.

---

**MyzamAI v3.0 - Powered by Meta Llama3 (Hugging Face API)** 🤖⚖️
