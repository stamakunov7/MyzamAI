"""
Summarizer Agent - Condenses long legal texts into concise summaries
Uses centralized Meta Llama 3 from llm_manager
"""

import logging
from core.llm_manager import llama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SummarizerAgent:
    """
    Agent that summarizes long legal texts for better readability
    Uses shared Meta Llama 3 pipeline
    """
    
    def __init__(self):
        """
        Initialize Summarizer Agent
        Uses centralized Llama 3 pipeline from llm_manager
        """
        self.llm = llama
        logger.info("Summarizer Agent initialized with Meta Llama 3")
    
    def summarize(self, text: str, max_length: int = 250) -> str:
        """
        Summarize long text into concise form
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summarized text
        """
        # If text is already short, return as is
        if len(text) < 500:
            logger.info("Text is already concise, skipping summarization")
            return text
        
        if self.llm is None:
            logger.warning("Llama 3 not available, using extractive summarization")
            return self._extractive_summarize(text, max_length)
        
        # Strict editor prompt for legal summaries
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Ты — редактор юридических ответов.
Твоя задача — сократить текст до 3–5 предложений, сохранив юридическую суть и формулировки закона.
Удали дубли, воду и все не относящиеся фразы.
Не меняй структуру "Ответ:", "Основание:", "Совет:".
Сделай язык простым, но профессиональным.
Используй официальную юридическую терминологию: "взаимное согласие сторон", "в соответствии с законом", "правовые основания".
НЕ добавляй скобки, кавычки или другие символы разметки.<|eot_id|><|start_header_id|>user<|end_header_id|>

Текст:
{text}

Краткое резюме:<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        
        try:
            logger.info("Generating summary with Meta Llama 3...")
            response = self.llm(prompt)
            
            # Extract generated text
            result = response[0]["generated_text"]
            
            if "<|start_header_id|>assistant<|end_header_id|>" in result:
                summary = result.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            else:
                summary = result.split(prompt)[-1].strip()
            
            # Clean up tags
            summary = summary.replace("<|eot_id|>", "").strip()
            
            # Truncate if needed
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            
            logger.info("✓ Summary generated")
            return summary
            
        except Exception as e:
            logger.error(f"Error in summarization: {e}")
            return self._extractive_summarize(text, max_length)
    
    def _extractive_summarize(self, text: str, max_length: int = 250) -> str:
        """
        Simple extractive summarization fallback
        
        Args:
            text: Text to summarize
            max_length: Maximum length
            
        Returns:
            Extracted summary
        """
        # Split into sentences
        sentences = text.replace('。', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Take first few sentences that fit in max_length
        summary = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) > max_length:
                break
            summary.append(sentence)
            current_length += len(sentence)
        
        result = '. '.join(summary)
        if not result.endswith('.'):
            result += '.'
        
        logger.info("✓ Extractive summary created")
        return result
    
    def condense_for_telegram(self, text: str) -> str:
        """
        Condense text specifically for Telegram's character limits
        Telegram messages should be under 4096 characters
        
        Args:
            text: Text to condense
            
        Returns:
            Condensed text suitable for Telegram
        """
        if len(text) <= 4000:
            return text
        
        logger.info("Text exceeds Telegram limit, condensing...")
        return self.summarize(text, max_length=3500)


def main():
    """
    Test the Summarizer Agent
    """
    agent = SummarizerAgent()
    
    long_text = """Статья 22. Отсутствие кассового или товарного чека
Отсутствие у потребителя кассового или товарного чека либо иного документа, удостоверяющих факт и условия покупки товара, не является основанием для отказа в удовлетворении его требований. Потребитель вправе ссылаться на свидетельские показания в подтверждение заключения договора и его условий.

Статья 23. Права потребителя при обнаружении недостатков товара
Потребитель, которому продан товар ненадлежащего качества, если это не было оговорено продавцом, вправе по своему выбору потребовать: замены на товар аналогичной марки; замены на такой же товар другой марки с соответствующим перерасчетом покупной цены."""
    
    summary = agent.summarize(long_text)
    
    print("=" * 60)
    print("Original Length:", len(long_text))
    print("Summary Length:", len(summary))
    print("=" * 60)
    print("Summary:")
    print(summary)


if __name__ == "__main__":
    main()

