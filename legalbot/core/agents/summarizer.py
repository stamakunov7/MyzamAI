"""
Summarizer Agent - Condenses long legal texts into concise summaries
"""

import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SummarizerAgent:
    """
    Agent that summarizes long legal texts for better readability
    """
    
    def __init__(self, model_name: str = "HuggingFaceH4/zephyr-7b-beta"):
        """
        Initialize Summarizer Agent
        
        Args:
            model_name: HuggingFace model for summarization
        """
        self.model_name = model_name
        self.pipe = None
        logger.info("Summarizer Agent initialized")
    
    def load_model(self):
        """
        Load the summarization model (lazy loading)
        """
        if self.pipe is None:
            logger.info(f"Loading summarization model: {self.model_name}")
            
            try:
                self.pipe = pipeline(
                    "text-generation",
                    model=self.model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    max_new_tokens=300,
                )
                logger.info("✓ Summarization model loaded")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.pipe = None
    
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
        
        self.load_model()
        
        if self.pipe is None:
            logger.warning("Model not available, using extractive summarization")
            return self._extractive_summarize(text, max_length)
        
        prompt = f"""<|system|>
Ты помощник, который создает краткие и точные резюме юридических текстов. Сохраняй все важные детали и юридические термины.
</s>
<|user|>
Сократи следующий текст, сохранив все ключевые юридические положения:

{text}

Краткое резюме:
</s>
<|assistant|>
"""
        
        try:
            logger.info("Generating summary...")
            response = self.pipe(
                prompt,
                max_new_tokens=max_length,
                num_return_sequences=1,
                pad_token_id=self.pipe.tokenizer.eos_token_id,
            )
            
            generated = response[0]['generated_text']
            
            if "<|assistant|>" in generated:
                summary = generated.split("<|assistant|>")[-1].strip()
            else:
                summary = generated.split(prompt)[-1].strip()
            
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

