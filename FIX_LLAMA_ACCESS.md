# 🔧 Решение проблемы доступа к Llama 3

## ❌ Проблема

```
ERROR: You are trying to access a gated repo.
Access to model meta-llama/Meta-Llama-3-8B-Instruct is restricted.
```

**Meta Llama 3 - это закрытая модель** (gated repository), требует авторизацию.

---

## ✅ Решение 1: Получить доступ к Llama 3 (РЕКОМЕНДУЕТСЯ)

### Шаг 1: Создать аккаунт HuggingFace

1. Перейди на https://huggingface.co/join
2. Зарегистрируйся (бесплатно)

### Шаг 2: Запросить доступ к Llama 3

1. Открой https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
2. Нажми **"Request access"**
3. Прими лицензионное соглашение Meta
4. Подожди подтверждения (обычно мгновенно)

### Шаг 3: Получить токен

1. Перейди в https://huggingface.co/settings/tokens
2. Нажми **"New token"**
3. Выбери **"Read"** permissions
4. Скопируй токен

### Шаг 4: Авторизоваться

```bash
cd legalbot
source venv/bin/activate

# Авторизоваться с токеном
huggingface-cli login
# Вставь свой токен и нажми Enter
```

### Шаг 5: Запустить бота снова

```bash
python bot/main.py
```

Теперь Llama 3 загрузится! ✅

---

## ✅ Решение 2: Использовать открытую модель (БЕЗ АВТОРИЗАЦИИ)

Если не хочешь регистрироваться, используй **полностью открытую модель**.

### Вариант A: Microsoft Phi-3 (3.8B) ⭐ Рекомендую

Отредактируй `core/llm_manager.py`:

```python
# Было:
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

# Стало:
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
```

**Плюсы:**
- ✅ Не нужна авторизация
- ✅ Меньше памяти (3.8B vs 8B)
- ✅ Быстрее работает
- ✅ Хорошее качество для юридических задач

### Вариант B: TinyLlama (1.1B) - Самый легкий

```python
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

**Плюсы:**
- ✅ Очень быстрая
- ✅ Мало памяти (~2GB)
- ⚠️ Качество хуже

### Вариант C: Mistral-7B-Instruct

```python
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
```

**Плюсы:**
- ✅ Не требует авторизации
- ✅ Хорошее качество
- ⚠️ Нужно ~16GB RAM

---

## 🚀 Быстрое решение (прямо сейчас!)

### 1. Изменить на Phi-3

```bash
cd legalbot
nano core/llm_manager.py
```

Замени строку 14:
```python
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
```

Сохрани: `Ctrl+O`, Enter, `Ctrl+X`

### 2. Запустить бота

```bash
source venv/bin/activate
python bot/main.py
```

**Готово!** Phi-3 загрузится без проблем! ✅

---

## 📊 Сравнение моделей

| Модель | Размер | Требует авторизацию? | RAM | Качество | Скорость |
|--------|--------|---------------------|-----|----------|----------|
| **Llama 3** | 8B | ✅ Да | 16GB | ⭐⭐⭐⭐⭐ | Средняя |
| **Phi-3** | 3.8B | ❌ Нет | 8GB | ⭐⭐⭐⭐ | Быстрая |
| **Mistral-7B** | 7B | ❌ Нет | 16GB | ⭐⭐⭐⭐ | Средняя |
| **TinyLlama** | 1.1B | ❌ Нет | 2GB | ⭐⭐⭐ | Очень быстрая |

---

## 💡 Рекомендация

**Для продакшна:** Используй **Llama 3** (получи доступ)
**Для разработки:** Используй **Phi-3** (быстро и без авторизации)

---

## 🔄 После изменения модели

1. Удали старый кеш (опционально):
```bash
rm -rf ~/.cache/huggingface/hub/models--meta-llama*
```

2. Перезапусти бота:
```bash
python bot/main.py
```

Модель загрузится заново! ✅

---

## ✅ Готово!

Теперь бот будет работать с выбранной моделью! 🚀

