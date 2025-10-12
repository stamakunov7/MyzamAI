# ⚡ LegalBot+ Quick Start Guide

Get LegalBot+ up and running in 5 minutes!

---

## 🚀 One-Command Setup (Linux/Mac)

```bash
chmod +x setup.sh && ./setup.sh
```

That's it! The script will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Build FAISS index
- Run system tests

---

## 🚀 One-Command Setup (Windows)

```cmd
setup.bat
```

---

## 📋 Manual Setup (All Platforms)

### Step 1: Install Dependencies (2 min)
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Build Search Index (1 min)
```bash
python core/build_faiss_index.py
```

### Step 3: Test the System (30 sec)
```bash
python test_system.py
```

### Step 4: Run the Bot (1 min)

**Option A: Demo Mode (No Telegram)**
```bash
python bot/main.py
```

**Option B: Full Telegram Bot**
```bash
# Get token from @BotFather on Telegram
export TELEGRAM_BOT_TOKEN='your_token_here'
python bot/main.py
```

---

## 💬 First Query

Send this to your bot:
```
Могу ли я вернуть товар без чека?
```

Expected response:
```
⚖️ Юридическая консультация

Ваш вопрос:
Могу ли я вернуть товар без чека?

Ответ:
Да, согласно статье 22 Гражданского кодекса КР...
```

---

## 🎯 Common Commands

| Command | What it does |
|---------|--------------|
| `/start` | Start conversation |
| `/help` | Show help |
| `/law 22` | Get Article 22 |

---

## ⚡ Performance Tips

### Faster Inference

**Use GPU (if available):**
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Use Smaller Model:**
```python
# In core/agents/legal_expert.py
model_name = "microsoft/phi-2"  # 2.7B instead of 7B
```

---

## 🐛 Troubleshooting

### "FAISS index not found"
```bash
python core/build_faiss_index.py
```

### "Out of memory"
```python
# Use smaller model in legal_expert.py
model_name = "microsoft/phi-2"
```

### "Telegram token not set"
```bash
export TELEGRAM_BOT_TOKEN='your_token'
```

---

## 📚 Next Steps

1. **Read full docs:** `README.md`
2. **See examples:** `EXAMPLES.md`
3. **Learn architecture:** `ARCHITECTURE.md`
4. **Contribute:** `CONTRIBUTING.md`

---

## 🎉 You're Ready!

Your LegalBot+ is now operational. Start asking legal questions!

For detailed documentation, see **README.md**

---

**Need Help?** Open an issue on GitHub or check the documentation.

