"""
Legal Expert Agent - Interprets legal articles and provides analysis
Uses centralized Meta Llama 3 from llm_manager
"""

import logging
from core.llm_manager import llama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalExpertAgent:
    """
    Agent that interprets legal texts and provides expert analysis
    Uses shared Meta Llama 3 pipeline
    """
    
    def __init__(self):
        """
        Initialize Legal Expert Agent
        Uses centralized Llama 3 pipeline from llm_manager
        """
        self.llm = llama
        logger.info("Legal Expert Agent initialized with Meta Llama 3")
    
    def interpret(self, query: str, legal_texts: str) -> str:
        """
        Interpret legal texts in the context of user query
        
        Args:
            query: User's question
            legal_texts: Retrieved legal articles
            
        Returns:
            Expert interpretation
        """
        if self.llm is None:
            logger.error("Llama 3 model not available")
            return self._fallback_interpretation(query, legal_texts)
        
        # Ultra-strict prompt for concise legal answers
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Ты — опытный юрист-консультант, специализирующийся на гражданском праве Кыргызской Республики.
Отвечай кратко (3–5 предложений максимум), строго по закону, используя только статьи из контекста ниже.
Используй официальную юридическую терминологию: "взаимное согласие сторон", "в соответствии с", "правовые основания".

❗Правила:
- Не повторяй вопрос
- Не включай нерелевантные статьи
- Не дублируй одинаковые мысли
- Не пиши «вопрос требует уточнения» — дай общий юридический ответ
- Не вставляй "Вопрос:", "Статьи:" или любые заголовки в теле ответа
- Пиши только одну статью, если она релевантна
- НЕ используй скобки или другие символы разметки

🚨 ВАЖНО: Если вопрос НЕ относится к Гражданскому кодексу (уголовное право, налоги, семейное право и т.д.):
Ответ: Этот вопрос не относится к гражданскому праву КР. Обратитесь к [название кодекса] для получения информации.
Совет: рекомендуется проконсультироваться с юристом по [тип права]
[НЕ указывай "Основание" для вопросов вне компетенции!]

⚙️ Формат ответа (строго):
Ответ: краткий юридический ответ, максимум 2 предложения
Основание: Статья номер, краткое описание правовой нормы [ТОЛЬКО если вопрос по ГК КР!]
Совет: короткая практическая рекомендация, не более 15 слов

✅ Пример правильного ответа (вопрос по ГК):
Ответ: Трудовой договор может быть расторгнут досрочно при наличии взаимного согласия сторон. Изменение или прекращение договора допускается только по соглашению работника и работодателя.
Основание: Статья 35 ГК КР регулирует порядок изменения условий трудового договора на основании взаимного согласия сторон
Совет: рекомендуется оформить расторжение в письменной форме

✅ Пример для вопроса ВНЕ компетенции:
Ответ: Кража является уголовным преступлением и регулируется Уголовным кодексом КР, а не Гражданским кодексом.
Совет: обратитесь к Уголовному кодексу КР или проконсультируйтесь с адвокатом<|eot_id|><|start_header_id|>user<|end_header_id|>

Вопрос: {query}

Статьи Гражданского кодекса КР:
{legal_texts}

Ответ:<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        
        try:
            logger.info("Generating legal interpretation with Meta Llama 3...")
            response = self.llm(prompt)
            
            # Extract generated text
            result = response[0]["generated_text"]
            
            # Extract only the assistant's response
            if "<|start_header_id|>assistant<|end_header_id|>" in result:
                answer = result.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            else:
                answer = result.split(prompt)[-1].strip()
            
            # Clean up any remaining tags
            answer = answer.replace("<|eot_id|>", "").strip()
            
            logger.info("✓ Interpretation generated")
            return answer
            
        except Exception as e:
            logger.error(f"Error in interpretation: {e}")
            return self._fallback_interpretation(query, legal_texts)
    
    def _fallback_interpretation(self, query: str, legal_texts: str) -> str:
        """
        Simple rule-based fallback if LLM fails
        
        Args:
            query: User query
            legal_texts: Legal texts
            
        Returns:
            Basic interpretation
        """
        return f"""На основе представленных статей Гражданского кодекса:

{legal_texts}

Эти положения закона применимы к вашему вопросу: "{query}"

Рекомендуется проконсультироваться с юристом для получения детальной правовой консультации."""


def main():
    """
    Test the Legal Expert Agent with Meta Llama 3
    """
    agent = LegalExpertAgent()
    
    query = "Могу ли я вернуть товар без чека?"
    legal_text = """Статья 22. Отсутствие кассового или товарного чека
Отсутствие у потребителя кассового или товарного чека либо иного документа, удостоверяющих факт и условия покупки товара, не является основанием для отказа в удовлетворении его требований."""
    
    result = agent.interpret(query, legal_text)
    print("=" * 60)
    print("Legal Expert Response (Meta Llama 3):")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()

