# 🚂 Railway Deployment Guide

Пошаговая инструкция по деплою MyzamAI на Railway.

## 📋 Что будет задеплоено

Railway задеплоит:
- ✅ Telegram бот (`src/bot/main.py`)
- ✅ FAISS индекс (будет создан автоматически при первом запуске)
- ✅ Все зависимости из `myzamai/requirements.txt`
- ✅ Конфигурацию из `myzamai/config/`

## 🔧 Подготовка

### 1. Убедитесь что у вас есть:
- ✅ Railway аккаунт с Hobby планом ($5/месяц)
- ✅ Telegram Bot Token (от @BotFather)
- ✅ Hugging Face API Token

### 2. Переменные окружения (Environment Variables)

Вам нужно будет добавить эти переменные в Railway Dashboard:

**Обязательные:**
```
TELEGRAM_BOT_TOKEN=ваш_telegram_bot_token
HUGGINGFACE_API_TOKEN=ваш_huggingface_token
```

**Опциональные:**
```
PYTHON_VERSION=3.11
```

## 🚀 Деплой на Railway

### Вариант 1: Через GitHub (Рекомендуется)

1. **Подключите GitHub репозиторий:**
   - Зайдите на [Railway Dashboard](https://railway.app)
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий `MyzamAI`

2. **Настройте переменные окружения:**
   - В проекте Railway перейдите в "Variables"
   - Добавьте:
     - `TELEGRAM_BOT_TOKEN` = ваш токен от @BotFather
     - `HUGGINGFACE_API_TOKEN` = ваш HF токен

3. **Настройте деплой:**
   - Railway автоматически обнаружит `railway.json`
   - Или в настройках проекта укажите:
     - **Root Directory:** `.` (корень репозитория)
     - **Start Command:** `cd myzamai && python scripts/build_faiss_index.py && python src/bot/main.py`

4. **Дождитесь деплоя:**
   - Railway автоматически соберет проект
   - Установит зависимости из `myzamai/requirements.txt`
   - Запустит бота

### Вариант 2: Через Railway CLI

1. **Установите Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Залогиньтесь:**
   ```bash
   railway login
   ```

3. **Инициализируйте проект:**
   ```bash
   cd /Users/stam7/Documents/Coding Workspace/MyzamAI
   railway init
   ```

4. **Добавьте переменные окружения:**
   ```bash
   railway variables set TELEGRAM_BOT_TOKEN=ваш_токен
   railway variables set HUGGINGFACE_API_TOKEN=ваш_hf_токен
   ```

5. **Задеплойте:**
   ```bash
   railway up
   ```

## ⚙️ Важные настройки

### 1. Build Command (если нужно)
Railway автоматически определит Python проект через NIXPACKS. Но можно указать явно:
```
pip install -r myzamai/requirements.txt
```

### 2. Start Command
Уже настроен в `railway.json`:
```bash
cd myzamai && python scripts/build_faiss_index.py && python src/bot/main.py
```

### 3. Healthcheck (опционально)
Railway автоматически проверит что процесс запущен. Если бот не отвечает на команды - проверьте логи.

## 🔍 Проверка работы

После деплоя:

1. **Проверьте логи в Railway Dashboard:**
   - Откройте проект → "Deployments" → выберите последний деплой → "Logs"
   - Должны увидеть:
     ```
     ✅ Configuration loaded
     ✅ FAISS index built successfully
     🚀 Starting MyzamAI...
     ✓ Telegram bot initialized
     ```

2. **Протестируйте бота в Telegram:**
   - Откройте вашего бота в Telegram
   - Отправьте `/start`
   - Должен прийти welcome message

3. **Проверьте что FAISS индекс создан:**
   - В логах должно быть: `✓ Loaded index with X vectors`

## 🐛 Troubleshooting

### Проблема: "FAISS index not found"
**Решение:** Проверьте что `myzamai/data/civil_code_full.txt` существует. Railway может не загрузить файлы если они в .gitignore.

### Проблема: "TELEGRAM_BOT_TOKEN not found"
**Решение:** Добавьте переменную окружения в Railway Dashboard → Variables.

### Проблема: Бот не отвечает
**Решение:**
1. Проверьте логи в Railway
2. Убедитесь что бот запущен (в логах должно быть "Starting MyzamAI...")
3. Проверьте что Telegram Bot Token правильный

### Проблема: Build fails
**Решение:**
- Проверьте что `myzamai/requirements.txt` существует
- Проверьте логи сборки на наличие ошибок установки зависимостей

### Проблема: Out of memory
**Решение:**
- Hobby план дает 512MB RAM
- Если не хватает, попробуйте оптимизировать:
  - Используйте `faiss-cpu` вместо `faiss-gpu`
  - Убедитесь что не загружаются локальные модели (используется HF API)

## 💰 Стоимость

**Hobby Plan ($5/месяц):**
- 512MB RAM
- 1GB storage
- 500 hours compute/month (≈720 hours в месяце)
- Бот будет работать 24/7

**Расходы:**
- Railway: $5/месяц
- Hugging Face API: бесплатно (до лимита)
- Telegram Bot API: бесплатно

## 📝 Чеклист перед деплоем

- [ ] Репозиторий залит на GitHub
- [ ] `railway.json` в корне проекта
- [ ] `.railwayignore` создан (опционально)
- [ ] `TELEGRAM_BOT_TOKEN` готов
- [ ] `HUGGINGFACE_API_TOKEN` готов
- [ ] `myzamai/data/civil_code_full.txt` существует в репозитории
- [ ] Все зависимости в `myzamai/requirements.txt`

## 🎉 После успешного деплоя

1. Бот будет работать 24/7
2. Автоматический рестарт при падении (restartPolicyType: ON_FAILURE)
3. Логи доступны в реальном времени в Railway Dashboard
4. Автоматический redeploy при push в GitHub (если настроен)

---

**Вопросы?** Проверьте логи в Railway Dashboard или документацию на [railway.app/docs](https://railway.app/docs)

