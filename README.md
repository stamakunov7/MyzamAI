# 🚀 MyzamAI Project

Welcome to the MyzamAI workspace! This repository contains various AI and machine learning projects.

---

## 📂 Projects

### 🤖 LegalBot+
**Location:** `legalbot/`

A sophisticated multi-agent legal chatbot powered by free open-source LLMs. Provides legal consultations based on the Civil Code of the Kyrgyz Republic using RAG (Retrieval-Augmented Generation), FAISS vector search, and specialized AI agents.

**Features:**
- ⚖️ Legal question answering
- 🤖 Multi-agent architecture (6 specialized agents)
- 🔍 FAISS vector search for document retrieval
- 🌐 Bilingual support (Russian/English)
- 📱 Telegram bot integration
- 💾 Conversation memory
- ✅ Quality review and self-correction
- 🆓 100% free and open source (no API keys needed)

**Tech Stack:**
- HuggingFace Transformers (Zephyr-7B, Phi-2)
- FAISS Vector Database
- Sentence Transformers
- Python Telegram Bot
- PyTorch

**Quick Start:**
```bash
cd legalbot

# Linux/Mac
./setup.sh

# Windows
setup.bat

# Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python core/build_faiss_index.py
python bot/main.py
```

**Documentation:**
- [📖 Full README](legalbot/README.md) - Complete documentation
- [⚡ Quick Start](legalbot/QUICKSTART.md) - Get started in 5 minutes
- [🏗️ Architecture](legalbot/ARCHITECTURE.md) - Technical details
- [💬 Examples](legalbot/EXAMPLES.md) - Example conversations
- [🤝 Contributing](legalbot/CONTRIBUTING.md) - How to contribute

**Example Usage:**
```
User: Могу ли я вернуть товар без чека?

LegalBot+: ⚖️ Юридическая консультация

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

## 🛠️ General Tech Stack

- **Languages:** Python 3.10+
- **ML/AI:** PyTorch, Transformers, Sentence-Transformers
- **Vector DB:** FAISS
- **APIs:** Telegram Bot API
- **Tools:** Git, Virtual Environments

---

## 📄 License

MIT License - See individual project folders for details

---

## 🤝 Contributing

Contributions are welcome! Each project has its own contributing guidelines:
- [LegalBot+ Contributing Guide](legalbot/CONTRIBUTING.md)

General guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🌟 Future Projects

Stay tuned for more AI projects including:
- Healthcare chatbots
- Financial analysis tools
- Educational AI assistants
- And more...

---

## 📧 Contact

- **Issues:** Open a GitHub issue
- **Email:** tstamakunov@stetson.edu
- **Discussions:** GitHub Discussions

---

## 🙏 Acknowledgments

- HuggingFace for amazing open-source models
- Facebook AI for FAISS
- The open-source community

---

**Made with ❤️ and 🤖 AI**

**MyzamAI © 2025**
