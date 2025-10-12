# 🏗️ LegalBot+ Architecture

Detailed technical architecture of the multi-agent legal chatbot system.

---

## 📐 System Overview

LegalBot+ is built on a **multi-agent architecture** where specialized AI agents collaborate to provide accurate legal consultations. The system uses:

- **RAG (Retrieval-Augmented Generation)** for grounding responses in legal documents
- **FAISS vector database** for efficient similarity search
- **Open-source LLMs** from Hugging Face for natural language processing
- **Agent orchestration** for coordinated information processing

---

## 🔧 Core Components

### 1. Document Processing Pipeline

```
Civil Code Text → Chunking → Embedding → FAISS Index
```

**Implementation:** `core/build_faiss_index.py`

- **Input:** Legal text file (`data/civil_code.txt`)
- **Chunking Strategy:**
  - Base size: 700 characters
  - Overlap: 100 characters
  - Boundary-aware: Breaks at sentences/paragraphs
  - Article-aware: Keeps articles together when possible

- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
  - Dimension: 384
  - Multilingual support
  - Fast inference: ~1000 sentences/sec on CPU

- **Vector Database:** FAISS IndexFlatL2
  - Exact L2 distance search
  - In-memory index for fast retrieval
  - Persistent storage via serialization

---

### 2. Multi-Agent System

#### Agent 1: LawRetriever
**File:** `core/law_retriever.py`

**Responsibilities:**
- Load and manage FAISS index
- Convert queries to embeddings
- Perform similarity search
- Return top-k relevant articles

**Technology:**
- FAISS for vector search
- Sentence-transformers for encoding
- Pickle for chunk storage

**Performance:**
- Query time: ~0.2-0.5s on CPU
- Index size: ~100KB per 100 articles

---

#### Agent 2: LegalExpertAgent
**File:** `core/agents/legal_expert.py`

**Responsibilities:**
- Interpret legal articles
- Provide expert analysis
- Explain in simple language
- Answer user questions

**Technology:**
- Model: `HuggingFaceH4/zephyr-7b-beta` (7B params)
- Template: ChatML format
- Inference: FP16 (GPU) or FP32 (CPU)
- Fallback: `microsoft/phi-2` if main model fails

**Prompt Engineering:**
```
<|system|>
Ты юридический эксперт...
</s>
<|user|>
Вопрос: {query}
Статьи: {legal_texts}
</s>
<|assistant|>
```

**Performance:**
- Generation time: ~3-5s (GPU), ~10-30s (CPU)
- Token limit: 512 new tokens
- Temperature: 0.7 (balanced creativity)

---

#### Agent 3: SummarizerAgent
**File:** `core/agents/summarizer.py`

**Responsibilities:**
- Condense long responses
- Maintain key information
- Ensure Telegram limits (4096 chars)

**Technology:**
- Primary: LLM-based abstractive summarization
- Fallback: Extractive summarization (sentence selection)

**Strategy:**
- Only activates if text > 500 chars
- Preserves legal terminology
- Maintains logical flow

---

#### Agent 4: TranslatorAgent
**File:** `core/agents/translator.py`

**Responsibilities:**
- Detect query language
- Translate RU ↔ EN
- Handle bilingual responses

**Technology:**
- RU→EN: `Helsinki-NLP/opus-mt-ru-en`
- EN→RU: `Helsinki-NLP/opus-mt-en-ru`
- Language detection: Cyrillic ratio heuristic

**Chunking:**
- Max chunk: 400 chars
- Sentence-aware splitting
- Preserves context across chunks

---

#### Agent 5: ReviewerAgent
**File:** `core/agents/reviewer_agent.py`

**Responsibilities:**
- Validate response quality
- Check accuracy and relevance
- Perform self-correction
- Log problematic responses

**Validation Pipeline:**
1. **Basic Checks (Rule-based):**
   - Length check (min 20 chars)
   - Legal context check (keywords)
   - Relevance check (query-response overlap)

2. **LLM Review (Optional):**
   - Accuracy assessment
   - Completeness evaluation
   - Clarity verification

**Logging:**
- Failed reviews stored in memory
- Used for system improvement

---

#### Agent 6: UserInterfaceAgent
**File:** `core/agents/user_interface_agent.py`

**Responsibilities:**
- Format responses for Telegram
- Add structure and emojis
- Generate contextual tips
- Include legal disclaimers

**Features:**
- Markdown formatting
- Context-aware recommendations
- Emoji indicators
- Timestamp inclusion

**Output Structure:**
```
⚖️ Header
📝 Question recap
💬 Main answer
📚 Legal sources
💡 Practical tips
⚠️ Disclaimer
🤖 Footer
```

---

### 3. Orchestration Layer

**File:** `bot/main.py` - `LegalBotOrchestrator`

**Responsibilities:**
- Initialize all agents
- Manage agent lifecycle
- Coordinate information flow
- Handle errors gracefully
- Maintain conversation memory

**Processing Pipeline:**
```python
async def process_query(query, user_id):
    1. Detect language (Translator)
    2. Translate if needed (Translator)
    3. Retrieve articles (LawRetriever)
    4. Generate interpretation (LegalExpert)
    5. Review response (Reviewer)
    6. Summarize if needed (Summarizer)
    7. Translate back if needed (Translator)
    8. Format for UI (UIAgent)
    9. Update memory
    return formatted_response
```

**Memory Management:**
- Stores last 20 queries per user
- Persistent JSON storage
- Includes timestamps and truncated responses

---

### 4. Telegram Bot Interface

**File:** `bot/main.py` - `TelegramBot`

**Responsibilities:**
- Handle Telegram API
- Process commands
- Send typing indicators
- Format messages with Markdown

**Commands:**
- `/start` - Welcome message
- `/help` - Usage instructions
- `/law <number>` - Retrieve specific article
- Text messages - Process as queries

**Features:**
- Async message handling
- Typing indicators
- Markdown fallback
- Error handling

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                          ↓                                   │
│                  [Telegram Message]                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   TELEGRAM BOT                               │
│  • Command routing                                           │
│  • Message parsing                                           │
│  • Response formatting                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                                │
│  • Agent coordination                                        │
│  • Error handling                                            │
│  • Memory management                                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
    ┌──────────────┐            ┌──────────────┐
    │ Translator   │            │ LawRetriever │
    │   Agent      │            │   (FAISS)    │
    └──────┬───────┘            └──────┬───────┘
           │                           │
           │                           ▼
           │                  ┌──────────────┐
           │                  │   Embedding  │
           │                  │    Model     │
           │                  └──────┬───────┘
           │                         │
           │                         ▼
           │                  [Top 3 Articles]
           │                         │
           └─────────┬───────────────┘
                     │
                     ▼
            ┌──────────────┐
            │ Legal Expert │
            │    Agent     │
            └──────┬───────┘
                   │
                   ▼
            [Interpretation]
                   │
                   ▼
            ┌──────────────┐
            │   Reviewer   │
            │    Agent     │
            └──────┬───────┘
                   │
              [Approved?]
                   │
                   ▼
            ┌──────────────┐
            │ Summarizer   │
            │    Agent     │
            └──────┬───────┘
                   │
                   ▼
            [Condensed Text]
                   │
                   ▼
            ┌──────────────┐
            │ Translator   │  (if EN query)
            │    Agent     │
            └──────┬───────┘
                   │
                   ▼
            ┌──────────────┐
            │  UI Agent    │
            └──────┬───────┘
                   │
                   ▼
          [Formatted Response]
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                      TELEGRAM USER                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Data Structures

### FAISS Index Structure
```
faiss_index/
├── faiss_index.bin          # Binary FAISS index
│   └── IndexFlatL2
│       ├── ntotal: number of vectors
│       ├── d: dimension (384)
│       └── vectors: float32[ntotal, 384]
│
└── chunks.pkl               # Pickled text chunks
    └── List[str]            # Original text chunks
```

### Memory Structure
```json
{
  "user_id": {
    "first_interaction": "ISO-8601 timestamp",
    "queries": [
      {
        "timestamp": "ISO-8601 timestamp",
        "query": "User question",
        "response": "Truncated bot response (500 chars)"
      }
    ]
  }
}
```

---

## 🚀 Scalability Considerations

### Current Limitations
- **Single-threaded processing** - One query at a time
- **In-memory FAISS** - Limited by RAM
- **Local LLM inference** - GPU-dependent speed

### Scaling Strategies

#### 1. Horizontal Scaling
```
Load Balancer
    ↓
┌───────┬───────┬───────┐
│ Bot 1 │ Bot 2 │ Bot 3 │  (Multiple instances)
└───┬───┴───┬───┴───┬───┘
    └───────┼───────┘
            ↓
    Shared FAISS Server
            ↓
    Shared LLM Server
```

#### 2. Model Optimization
- Use quantized models (4-bit, 8-bit)
- Implement model caching
- Batch processing for embeddings
- Use ONNX runtime for faster inference

#### 3. Database Scaling
- Use FAISS IVF index for larger datasets
- Implement sharding for multi-code support
- Add Redis for conversation memory
- Use vector databases (Pinecone, Weaviate)

---

## 🔒 Security Considerations

### Current Implementation
- ✅ No external API keys in code
- ✅ Local-only processing
- ✅ No PII stored (only user IDs)
- ✅ Input validation

### Recommended Additions
- [ ] Rate limiting per user
- [ ] Input sanitization
- [ ] Encrypted memory storage
- [ ] Audit logging
- [ ] GDPR compliance features

---

## 📊 Performance Benchmarks

### Embedding Generation
- **Model:** all-MiniLM-L6-v2
- **Batch size:** 32
- **Speed:** ~1000 sentences/sec (CPU)
- **Memory:** ~500MB

### FAISS Search
- **Index size:** 40 vectors (demo)
- **Query time:** 0.2-0.5s
- **Memory:** ~1MB

### LLM Inference
- **Model:** Zephyr-7B
- **Hardware:** RTX 3060 (12GB VRAM)
- **Speed:** ~3-5s per response
- **Memory:** ~8GB

### Total Pipeline
- **CPU-only:** 30-60s per query
- **With GPU:** 8-15s per query

---

## 🔧 Configuration Options

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN           # Required for Telegram
LLM_MODEL                    # Optional: Override default LLM
EMBEDDING_MODEL              # Optional: Override embeddings
USE_GPU                      # Optional: Force GPU usage
MAX_CONTEXT_LENGTH           # Optional: Token limit
```

### Model Configuration
Edit in respective agent files:
```python
# Legal Expert
model_name = "HuggingFaceH4/zephyr-7b-beta"

# Embeddings
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Translation
ru_to_en = "Helsinki-NLP/opus-mt-ru-en"
en_to_ru = "Helsinki-NLP/opus-mt-en-ru"
```

---

## 🧪 Testing Strategy

### Unit Tests
- Individual agent functionality
- FAISS index operations
- Translation accuracy
- UI formatting

### Integration Tests
- Full pipeline execution
- Multi-agent coordination
- Error handling
- Memory persistence

### Load Tests
- Concurrent user handling
- Memory leak detection
- Response time under load

**Run tests:**
```bash
python test_system.py
```

---

## 📈 Future Enhancements

### Short-term
- [ ] Add conversation context awareness
- [ ] Implement caching for repeated queries
- [ ] Add more legal documents
- [ ] Improve error messages

### Medium-term
- [ ] Fine-tune models on legal corpus
- [ ] Add voice message support
- [ ] Implement web interface
- [ ] Add multi-language support

### Long-term
- [ ] Deploy as microservices
- [ ] Implement federated learning
- [ ] Add case law analysis
- [ ] Create mobile app

---

## 📚 References

- **FAISS:** https://github.com/facebookresearch/faiss
- **Sentence Transformers:** https://www.sbert.net/
- **Zephyr:** https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
- **Python Telegram Bot:** https://python-telegram-bot.org/

---

**Document Version:** 1.0
**Last Updated:** October 2025

