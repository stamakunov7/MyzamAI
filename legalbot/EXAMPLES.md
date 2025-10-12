# 💬 LegalBot+ Example Conversations

This document shows real example conversations demonstrating the multi-agent system in action.

---

## Example 1: Consumer Rights - Product Return Without Receipt

### User Query
```
Могу ли я вернуть товар без чека?
```

### Agent Pipeline

#### Step 1: Language Detection
- **Agent:** Translator
- **Detected:** Russian (RU)
- **Action:** No translation needed

#### Step 2: Document Retrieval
- **Agent:** LawRetriever (FAISS)
- **Query:** "вернуть товар без чека"
- **Retrieved Articles:**
  1. Статья 22. Отсутствие кассового или товарного чека (relevance: 0.892)
  2. Статья 21. Обмен товара надлежащего качества (relevance: 0.756)
  3. Статья 23. Права потребителя при обнаружении недостатков (relevance: 0.721)

#### Step 3: Legal Interpretation
- **Agent:** Legal Expert
- **Input:** Query + Retrieved articles
- **Output:** 
```
Согласно статье 22 Гражданского кодекса КР, отсутствие у потребителя 
кассового или товарного чека либо иного документа, удостоверяющих факт 
и условия покупки товара, не является основанием для отказа в 
удовлетворении его требований.

Это означает, что вы имеете право вернуть товар даже без чека. 
Потребитель вправе ссылаться на свидетельские показания в 
подтверждение заключения договора и его условий.
```

#### Step 4: Quality Review
- **Agent:** Reviewer
- **Checks:**
  - ✓ Response length: adequate (267 chars)
  - ✓ Legal context: contains keywords (статья, закон, право)
  - ✓ Relevance: shares keywords with query
  - ✓ Accuracy: cites correct article
- **Result:** APPROVED

#### Step 5: Summarization
- **Agent:** Summarizer
- **Check:** 267 chars < 4000 chars
- **Action:** No summarization needed

#### Step 6: Translation
- **Agent:** Translator
- **Action:** Not needed (response in Russian, query in Russian)

#### Step 7: UI Formatting
- **Agent:** UserInterfaceAgent
- **Final Response:**

```markdown
⚖️ **Юридическая консультация**

**Ваш вопрос:**
_Могу ли я вернуть товар без чека?_

**Ответ:**
Согласно статье 22 Гражданского кодекса КР, отсутствие у потребителя 
кассового или товарного чека либо иного документа, удостоверяющих факт 
и условия покупки товара, не является основанием для отказа в 
удовлетворении его требований.

Это означает, что вы имеете право вернуть товар даже без чека. 
Потребитель вправе ссылаться на свидетельские показания в 
подтверждении заключения договора и его условий.

📚 **Правовая основа:**
1. Статья 22. Отсутствие кассового или товарного чека
Отсутствие у потребителя кассового или товарного чека либо иного документа, 
удостоверяющих факт и условия покупки товара, не является основанием...

💡 **Рекомендации:**
• Сохраняйте все документы о покупке
• Товар должен быть в надлежащем состоянии
• Соберите свидетельские показания если нет чека

⚠️ _Данная информация носит справочный характер. Для получения персональной 
юридической консультации обратитесь к квалифицированному юристу._

🤖 LegalBot+ | 12.10.2025 15:30
```

---

## Example 2: Contract Law - English Query

### User Query
```
What are the basic principles of contract law?
```

### Agent Pipeline

#### Step 1: Language Detection
- **Agent:** Translator
- **Detected:** English (EN)
- **Action:** Translate to Russian for retrieval

#### Step 2: Translation
- **Agent:** Translator (EN→RU)
- **Translated Query:** "Каковы основные принципы договорного права?"

#### Step 3: Document Retrieval
- **Agent:** LawRetriever
- **Retrieved Articles:**
  1. Статья 11. Свобода договора
  2. Статья 10. Понятие договора
  3. Статья 12. Исполнение договора

#### Step 4-6: Processing (same as Example 1)

#### Step 7: Back Translation
- **Agent:** Translator (RU→EN)
- **Action:** Translate interpretation to English

#### Step 8: Final Response
```markdown
⚖️ **Legal Consultation**

**Your question:**
_What are the basic principles of contract law?_

**Answer:**
According to Article 11 of the Civil Code of the Kyrgyz Republic, citizens 
and legal entities are free to conclude contracts. Coercion to conclude a 
contract is not permitted, except in cases where the obligation to conclude 
a contract is provided by the Code, law or voluntarily assumed obligation.

The contract must be performed properly in accordance with its terms and 
the requirements of the law...

📚 **Legal basis:**
1. Article 11. Freedom of contract
Citizens and legal entities are free to conclude contracts...

💡 **Recommendations:**
• Carefully read all terms and conditions of the contract
• Verify the presence of all signatures and seals
• Keep copies of all documents

⚠️ _This information is for reference only..._
```

---

## Example 3: Inheritance Law

### User Query
```
Кто является наследником первой очереди?
```

### Retrieved Articles
- Статья 30. Наследники по закону
- Статья 26. Основания наследования
- Статья 27. Открытие наследства

### Expert Interpretation
```
Согласно статье 30 Гражданского кодекса КР, наследниками первой 
очереди по закону являются дети, супруг и родители наследодателя. 
Внуки наследодателя и их потомки наследуют по праву представления.
```

### Practical Tips
```
💡 Рекомендации:
• Обратитесь к нотариусу в течение 6 месяцев
• Подготовьте документы, подтверждающие родство
• Узнайте о возможных долгах наследодателя
```

---

## Example 4: Using /law Command

### User Query
```
/law 22
```

### Direct Article Retrieval
```
📚 **Статья 22**

Статья 22. Отсутствие кассового или товарного чека

Отсутствие у потребителя кассового или товарного чека либо иного 
документа, удостоверяющих факт и условия покупки товара, не является 
основанием для отказа в удовлетворении его требований. Потребитель 
вправе ссылаться на свидетельские показания в подтверждение 
заключения договора и его условий.
```

---

## Example 5: Error Handling - Unclear Query

### User Query
```
помоги
```

### Review Result
- **Reviewer:** Query too vague, low quality retrieval
- **Action:** Request clarification

### Response
```
⚖️ К сожалению, ваш вопрос слишком общий.

Пожалуйста, уточните:
• О какой области права идет речь?
• Какая конкретная ситуация вас интересует?

Примеры хороших вопросов:
• "Могу ли я вернуть товар без чека?"
• "Кто является наследником первой очереди?"
• "Как расторгнуть трудовой договор?"

Используйте /help для подробной справки.
```

---

## Example 6: Multi-Turn Conversation with Memory

### Turn 1
**User:** Что такое договор аренды?

**Bot:** Согласно статье 37, по договору аренды арендодатель обязуется 
предоставить арендатору имущество за плату во временное владение и пользование...

*[Stored in memory]*

### Turn 2
**User:** А какие обязанности у арендатора?

**Bot:** *(Uses context from memory)* 
Согласно статье 39, арендатор обязан пользоваться арендованным имуществом 
в соответствии с условиями договора аренды...

---

## Example 7: Review and Correction Flow

### Initial Response (Failed Review)
```
Response: "Да."
Review: REJECTED - Response too short (3 chars)
```

### Corrected Response
```
Response: "Да, согласно статье 22 Гражданского кодекса КР, отсутствие 
кассового чека не является основанием для отказа..."
Review: APPROVED
```

---

## Performance Logs

### Example Timing (CPU)
```
[INFO] Processing query: Могу ли я вернуть товар без чека?
[INFO] Detected language: ru
[INFO] Retrieving relevant legal articles... (0.5s)
[INFO] Retrieved 3 articles
[INFO] Getting legal expert interpretation... (12.3s)
[INFO] Reviewing interpretation... (2.1s)
[INFO] Review approved
[INFO] Checking if summarization needed... (0.1s)
[INFO] No summarization needed
[INFO] Formatting response... (0.2s)
[INFO] ✓ Query processed successfully (15.2s total)
```

### Example Timing (GPU)
```
[INFO] Processing query: Могу ли я вернуть товар без чека?
[INFO] Detected language: ru
[INFO] Retrieving relevant legal articles... (0.2s)
[INFO] Retrieved 3 articles
[INFO] Getting legal expert interpretation... (3.8s)
[INFO] Reviewing interpretation... (0.9s)
[INFO] Review approved
[INFO] Checking if summarization needed... (0.1s)
[INFO] Formatting response... (0.1s)
[INFO] ✓ Query processed successfully (5.1s total)
```

---

## Agent Collaboration Diagram

```
User Query: "Могу ли я вернуть товар без чека?"
    │
    ▼
┌─────────────────┐
│   Translator    │  Detect: RU → No translation needed
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LawRetriever   │  FAISS search → 3 articles (0.892, 0.756, 0.721)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Legal Expert   │  Zephyr-7B → Interpretation in natural language
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Reviewer     │  Check: ✓ Length ✓ Context ✓ Relevance → APPROVED
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Summarizer     │  Check: 267 < 4000 → No action needed
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   UI Agent      │  Format with emoji, tips, disclaimer
└────────┬────────┘
         │
         ▼
    User receives formatted response
```

---

## Memory Example

### memory.json
```json
{
  "123456789": {
    "first_interaction": "2025-10-12T15:30:00",
    "queries": [
      {
        "timestamp": "2025-10-12T15:30:15",
        "query": "Могу ли я вернуть товар без чека?",
        "response": "⚖️ Юридическая консультация\n\nВаш вопрос:\n..."
      },
      {
        "timestamp": "2025-10-12T15:32:20",
        "query": "А если товар был в употреблении?",
        "response": "⚖️ Юридическая консультация\n\nВаш вопрос:\n..."
      }
    ]
  }
}
```

---

**End of Examples**

