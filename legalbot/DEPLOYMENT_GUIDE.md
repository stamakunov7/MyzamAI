# 🚀 Полный гайд по деплойменту MyzamAI

## 📋 Этап 1: Создание Telegram бота (5 минут)

### 1.1 Создать бота через BotFather

1. Открой Telegram и найди **@BotFather**
2. Отправь команду: `/newbot`
3. Введи имя бота: `MyzamAI Legal Bot`
4. Введи username: `myzamai_legal_bot` (или другой свободный)
5. **СОХРАНИ ТОКЕН!** Он выглядит так:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
   ```

### 1.2 Настроить описание бота

```
/setdescription
MyzamAI - AI-powered legal assistant for Kyrgyz Civil Code

/setabouttext
Intelligent multi-agent legal chatbot powered by Meta Llama 3

/setcommands
start - Начать работу
help - Показать справку
law - Получить статью закона
```

---

## 💻 Этап 2: Локальное тестирование (30 минут)

### 2.1 Установить зависимости

```bash
cd legalbot

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить пакеты
pip install -r requirements.txt
```

### 2.2 Создать файл .env

Создай файл `.env` в папке `legalbot/`:

```bash
# Создать .env файл
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=your_token_here
EOF
```

**Вставь свой токен вместо `your_token_here`!**

### 2.3 Построить FAISS индекс

```bash
python core/build_faiss_index.py
```

Должно появиться:
```
Loading Meta Llama 3 model: meta-llama/Meta-Llama-3-8B-Instruct
✓ Meta Llama 3 model loaded successfully
Found 40 articles
Total chunks: 40
✓ FAISS index built successfully!
```

### 2.4 Запустить бота локально

```bash
python bot/main.py
```

**Первый запуск:**
- Llama 3 загрузится (~16GB, 5-10 минут)
- Модель кешируется в `~/.cache/huggingface/`

**Должно появиться:**
```
INFO:core.llm_manager:Using Apple Silicon (MPS) device
INFO:core.llm_manager:✓ Meta Llama 3 model loaded successfully
INFO:bot.main:Legal Expert Agent initialized with Meta Llama 3
INFO:bot.main:Summarizer Agent initialized with Meta Llama 3
INFO:bot.main:Reviewer Agent initialized with Meta Llama 3
INFO:telegram.ext.Application:Application started
🚀 Starting LegalBot+...
```

### 2.5 Протестировать бота

1. Открой Telegram
2. Найди своего бота по username
3. Отправь `/start`
4. Задай вопрос: `Могу ли я вернуть товар без чека?`

**Если работает - переходим к деплойменту! ✅**

---

## ☁️ Этап 3: Деплоймент онлайн

### Вариант A: Railway (РЕКОМЕНДУЕТСЯ)

**Плюсы:** Бесплатно, простой деплой, 500 часов/месяц

#### A.1 Подготовка

1. Создай аккаунт на [Railway.app](https://railway.app/)
2. Подключи свой GitHub аккаунт

#### A.2 Создать GitHub репозиторий

```bash
cd /Users/stam7/Documents/Coding\ Workspace/MyzamAI

# Инициализировать git (если еще не сделано)
git init
git add legalbot/
git commit -m "MyzamAI: Multi-agent legal bot with Llama 3"

# Создать репозиторий на GitHub и запушить
git remote add origin https://github.com/your-username/myzamai.git
git push -u origin main
```

#### A.3 Создать файлы для деплоя

**Создай `Procfile`:**

```bash
cat > Procfile << 'EOF'
web: cd legalbot && python bot/main.py
EOF
```

**Создай `railway.json`:**

```bash
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd legalbot && python core/build_faiss_index.py && python bot/main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
```

#### A.4 Деплой на Railway

1. Зайди на [railway.app](https://railway.app/)
2. Нажми **"New Project"**
3. Выбери **"Deploy from GitHub repo"**
4. Выбери свой репозиторий `myzamai`
5. Railway автоматически начнет деплой

#### A.5 Установить переменные окружения

В Railway dashboard:
1. Перейди в **Variables**
2. Добавь переменную:
   - **Key:** `TELEGRAM_BOT_TOKEN`
   - **Value:** `твой_токен_от_botfather`
3. Нажми **Deploy**

#### A.6 Проверить логи

В Railway:
- Перейди в **Deployments**
- Открой **Logs**
- Должно появиться:
  ```
  ✓ Meta Llama 3 model loaded successfully
  🚀 Starting LegalBot+...
  ```

**Готово! Бот работает 24/7!** 🎉

---

### Вариант B: Render (Альтернатива)

**Плюсы:** Тоже бесплатно, больше контроля

#### B.1 Подготовка

1. Создай аккаунт на [Render.com](https://render.com/)
2. Подключи GitHub

#### B.2 Создать `render.yaml`

```yaml
services:
  - type: web
    name: myzamai-bot
    env: python
    buildCommand: cd legalbot && pip install -r requirements.txt && python core/build_faiss_index.py
    startCommand: cd legalbot && python bot/main.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

#### B.3 Деплой

1. Зайди на render.com
2. **New → Web Service**
3. Подключи свой GitHub repo
4. Добавь переменную `TELEGRAM_BOT_TOKEN`
5. **Create Web Service**

---

### Вариант C: VPS (Для продакшна)

**Плюсы:** Полный контроль, можно использовать GPU

#### C.1 Арендовать VPS

Рекомендации:
- **DigitalOcean** ($6/месяц, 2GB RAM) - для CPU
- **Vast.ai** (~$0.20/час) - для GPU
- **RunPod** (~$0.30/час) - для GPU

#### C.2 Настроить сервер

```bash
# Подключиться к серверу
ssh root@your-server-ip

# Установить зависимости
apt update
apt install -y python3.10 python3-pip git

# Клонировать репозиторий
git clone https://github.com/your-username/myzamai.git
cd myzamai/legalbot

# Установить пакеты
pip3 install -r requirements.txt

# Создать .env
nano .env
# Вставить: TELEGRAM_BOT_TOKEN=your_token

# Построить индекс
python3 core/build_faiss_index.py

# Запустить бота
python3 bot/main.py
```

#### C.3 Запустить как сервис (systemd)

```bash
# Создать service file
sudo nano /etc/systemd/system/myzamai.service
```

Вставить:
```ini
[Unit]
Description=MyzamAI Legal Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/myzamai/legalbot
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
ExecStart=/usr/bin/python3 /root/myzamai/legalbot/bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустить:
```bash
sudo systemctl daemon-reload
sudo systemctl enable myzamai
sudo systemctl start myzamai

# Проверить статус
sudo systemctl status myzamai

# Логи
sudo journalctl -u myzamai -f
```

---

## 🔍 Этап 4: Мониторинг и отладка

### 4.1 Проверить, что бот работает

```bash
# Отправить тестовый запрос
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

Должен вернуть JSON с информацией о боте.

### 4.2 Проверить вебхуки (если используются)

```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
```

### 4.3 Логи

**Railway/Render:**
- Смотри в Dashboard → Logs

**VPS:**
```bash
sudo journalctl -u myzamai -f
```

---

## 🐛 Решение проблем

### Проблема 1: "FAISS index not found"

```bash
python core/build_faiss_index.py
```

### Проблема 2: "Out of memory"

**Решение 1:** Использовать CPU offloading

Отредактируй `core/llm_manager.py`:
```python
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
    low_cpu_mem_usage=True,
    max_memory={0: "8GiB", "cpu": "16GiB"}  # Добавить эту строку
)
```

**Решение 2:** Использовать quantization (4-bit)

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quantization_config,
    device_map="auto"
)
```

### Проблема 3: "Model download timeout"

```bash
# Увеличить таймаут
export HF_HUB_DOWNLOAD_TIMEOUT=600

# Или скачать модель заранее
huggingface-cli download meta-llama/Meta-Llama-3-8B-Instruct
```

### Проблема 4: Бот не отвечает

1. Проверь токен
2. Проверь логи
3. Проверь, что бот запущен
4. Проверь интернет соединение

---

## 📊 Мониторинг производительности

### Добавить логирование

В `bot/main.py` добавь:

```python
import time

async def handle_message(update, context):
    start_time = time.time()
    
    # ... обработка ...
    
    end_time = time.time()
    logger.info(f"Query processed in {end_time - start_time:.2f}s")
```

### Telegram Analytics

Используй команды BotFather:
```
/stats - Статистика бота
/topcommands - Популярные команды
```

---

## 🎉 Готово!

Твой бот теперь:
- ✅ Работает 24/7 онлайн
- ✅ Использует Meta Llama 3
- ✅ Отвечает на юридические вопросы
- ✅ Доступен всем пользователям Telegram

---

## 📞 Полезные ссылки

- **BotFather:** [@BotFather](https://t.me/botfather)
- **Railway:** https://railway.app/
- **Render:** https://render.com/
- **Hugging Face:** https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

---

## 🔄 Обновление бота

```bash
# На сервере/Railway/Render
git pull origin main
pip install -r requirements.txt
sudo systemctl restart myzamai  # Для VPS
```

Railway/Render автоматически перезапустят при новом коммите.

---

**Удачи! 🚀**

