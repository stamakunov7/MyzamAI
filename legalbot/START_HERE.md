# 🚀 НАЧНИ ОТСЮДА - Быстрый старт

## ✅ Что нужно сделать (пошагово):

### 📱 **ШАГ 1: Создать Telegram бота** (5 минут)

1. Открой Telegram
2. Найди **@BotFather**
3. Отправь `/newbot`
4. Придумай имя: `MyzamAI Legal Bot`
5. Придумай username: `myzamai_legal_bot`
6. **СОХРАНИ ТОКЕН!** (скопируй куда-то)

---

### 💻 **ШАГ 2: Установить зависимости** (10 минут)

```bash
cd legalbot

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить пакеты
pip install -r requirements.txt
```

**⏳ Подожди 5-10 минут пока установятся пакеты**

---

### 🔐 **ШАГ 3: Создать файл .env** (1 минута)

В папке `legalbot/` создай файл `.env`:

```bash
TELEGRAM_BOT_TOKEN=твой_токен_от_botfather
```

**⚠️ Замени на свой реальный токен!**

---

### 🔨 **ШАГ 4: Построить FAISS индекс** (2 минуты)

```bash
python core/build_faiss_index.py
```

Должно появиться:
```
✓ FAISS index built successfully!
```

---

### 🚀 **ШАГ 5: Запустить бота** (5-10 минут первый раз)

```bash
python bot/main.py
```

**Первый запуск:**
- Llama 3 загрузится (~16GB)
- Займет 5-10 минут
- Модель закешируется для следующих запусков

**Должно появиться:**
```
✓ Meta Llama 3 model loaded successfully
🚀 Starting LegalBot+...
Application started
```

---

### 📱 **ШАГ 6: Протестировать бота** (1 минута)

1. Открой Telegram
2. Найди своего бота
3. Отправь `/start`
4. Задай вопрос: `Могу ли я вернуть товар без чека?`

**Если работает - ВСЁ ГОТОВО! 🎉**

---

## ☁️ **ШАГ 7: Задеплоить онлайн** (20 минут)

### Railway (РЕКОМЕНДУЕТСЯ - проще всего)

1. **Зарегистрируйся:** [railway.app](https://railway.app/)
2. **Создай GitHub репозиторий:**
   ```bash
   git init
   git add .
   git commit -m "MyzamAI bot"
   git remote add origin https://github.com/твой-username/myzamai.git
   git push -u origin main
   ```
3. **На Railway:**
   - New Project → Deploy from GitHub
   - Выбери свой репозиторий
   - Добавь переменную: `TELEGRAM_BOT_TOKEN`
   - Deploy!

4. **Готово!** Бот работает 24/7 онлайн!

---

## 📚 Полная документация

- 📘 **README.md** - Основная документация
- 🚀 **DEPLOYMENT_GUIDE.md** - Детальный гайд по деплою
- ✅ **REFACTOR_COMPLETE.md** - Что было сделано

---

## 🆘 Проблемы?

### "FAISS index not found"
```bash
python core/build_faiss_index.py
```

### "Out of memory"
Используй GPU или VPS с 16GB RAM

### "Bot not responding"
Проверь:
1. Токен правильный?
2. Бот запущен?
3. Интернет работает?

---

## 🎯 Краткая сводка

```
1. Создать бота в @BotFather → получить токен
2. pip install -r requirements.txt
3. Создать .env с токеном
4. python core/build_faiss_index.py
5. python bot/main.py
6. Протестировать в Telegram
7. Задеплоить на Railway
```

**Всё! Бот готов! 🚀**

---

**Следующий файл для чтения:** `DEPLOYMENT_GUIDE.md` (детальные инструкции)

