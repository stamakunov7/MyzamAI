# 🚀 Быстрый старт MyzamAI с Hugging Face API

## ✅ Что изменилось?

Теперь бот использует **Hugging Face Inference API** вместо локального запуска модели!

### Преимущества:
- ✅ **Нет нагрузки на твой компьютер** (модель работает на серверах HF)
- ✅ **Никаких лагов** - компьютер остается свободным
- ✅ **Быстрые ответы** - серверы HF мощные
- ✅ **Меньше зависимостей** - не нужно скачивать 8GB модель

---

## 📝 Что тебе нужно сделать:

### 1️⃣ Получи Hugging Face API токен

1. Зайди на: https://huggingface.co/settings/tokens
2. Нажми **"Create new token"** (или **"New token"**)
3. **Name:** `MyzamAI Bot`
4. **Type:** выбери `Write` или `Read`
5. Нажми **"Generate token"**
6. **Скопируй токен** (выглядит как `hf_xxxxxxxxxxxxx`)

⚠️ **Важно:** Сохрани токен - его нельзя будет увидеть снова!

---

### 2️⃣ Добавь токен в .env файл

Открой файл `.env` в папке `legalbot/`:

```bash
cd legalbot
nano .env
```

Добавь/обнови эти строки:

```env
TELEGRAM_BOT_TOKEN=твой_telegram_токен_здесь
HUGGINGFACE_API_TOKEN=hf_твой_huggingface_токен_здесь
```

Сохрани: `Ctrl+O` → `Enter` → `Ctrl+X`

---

### 3️⃣ Перезапусти бота

```bash
cd legalbot
python bot/main.py
```

Должно появиться:
```
✅ Configuration loaded
✅ Telegram Bot token: ***************abc123
✅ Hugging Face API token: ***************xyz789
🚀 LLM will run on HF servers (no local load!)
✅ Llama 3 API wrapper ready!
💡 Your computer will not be loaded - all processing happens on HF servers
```

---

## 🎯 Готово!

Теперь:
- ✅ Модель **не грузится** на твой компьютер
- ✅ Все работает через **API**
- ✅ Никаких лагов
- ✅ Быстрые ответы

---

## 📊 Лимиты бесплатного tier:

- ✅ **1000 запросов в день** (хватит для тестирования)
- ✅ Доступ к **Meta Llama 3 8B**
- ✅ Полностью **бесплатно**

Если нужно больше → Hugging Face Pro (~$9/месяц, безлимит)

---

## 🔧 Troubleshooting

### "HUGGINGFACE_API_TOKEN not found"
→ Проверь что токен добавлен в `.env` файл и начинается с `hf_`

### "Rate limit exceeded"
→ Превышен лимит бесплатного tier. Подожди час или перейди на Pro.

### "Access denied to model"
→ Убедись что у тебя есть доступ к модели на https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

---

**Теперь твой компьютер свободен! 🎉**

