# 🤖 MyzamAI

**Multi-Agent Legal Chatbot powered by Meta Llama3 (Hugging Face API)**

MyzamAI (from the Kyrgyz word «Мыйзам», meaning 'Law') is an AI-powered legal assistant that answers questions about the Civil Code of the Kyrgyz Republic.

**Link:**
https://t.me/myzam_ai_bot

## 📁 Project Structure

```
MyzamAI/
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
└── 📁 myzamai/                # Main project directory
    ├── 📁 src/                # Main application code
    │   ├── bot/               # Telegram bot interface
    │   └── core/              # Core business logic & agents
    ├── 📁 config/             # Configuration files
    ├── 📁 data/               # Legal documents & data
    ├── 📁 storage/            # Database & persistent storage
    ├── 📁 scripts/            # Utility scripts & tools
    ├── 📁 tests/              # Test suite
    ├── 📁 docs/               # Documentation
    └── requirements.txt       # Dependencies
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r myzamai/requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp myzamai/config/config.py.example myzamai/config/config.py
   # Edit myzamai/config/config.py with your API tokens
   ```

3. **Build FAISS index:**
   ```bash
   python myzamai/scripts/build_faiss_index.py
   ```

4. **Run bot:**
   ```bash
   python myzamai/src/bot/main.py
   ```

## 📖 Documentation

- **[📖 User Guide](myzamai/docs/README.md)** - Complete user documentation
- **[🛠️ Developer Guide](myzamai/docs/DEVELOPMENT.md)** - Technical documentation
- **[🧪 Testing Guide](myzamai/tests/README.md)** - Test suite documentation

## 💬 Usage

Start a conversation with the bot on Telegram:
- `/start` - Begin
- `/help` - Show commands
- `/law <number>` - Get specific article

## 🤝 Contributing

See [DEVELOPMENT.md](myzamai/docs/DEVELOPMENT.md) for development guidelines.

---

**MyzamAI v3.0 - Powered by Meta Llama3 (Hugging Face API)** 🤖⚖️
