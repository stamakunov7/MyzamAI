"""
Translator Agent - Translates between Russian and English
"""

from transformers import pipeline, MarianMTModel, MarianTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranslatorAgent:
    """
    Agent that translates legal texts between Russian and English
    """
    
    def __init__(self):
        """
        Initialize Translator Agent
        """
        self.ru_to_en_model = "Helsinki-NLP/opus-mt-ru-en"
        self.en_to_ru_model = "Helsinki-NLP/opus-mt-en-ru"
        self.ru_en_pipe = None
        self.en_ru_pipe = None
        logger.info("Translator Agent initialized")
    
    def load_ru_to_en(self):
        """
        Load Russian to English translation model
        """
        if self.ru_en_pipe is None:
            logger.info(f"Loading RU→EN translation model: {self.ru_to_en_model}")
            try:
                self.ru_en_pipe = pipeline(
                    "translation",
                    model=self.ru_to_en_model,
                )
                logger.info("✓ RU→EN model loaded")
            except Exception as e:
                logger.error(f"Failed to load RU→EN model: {e}")
                self.ru_en_pipe = None
    
    def load_en_to_ru(self):
        """
        Load English to Russian translation model
        """
        if self.en_ru_pipe is None:
            logger.info(f"Loading EN→RU translation model: {self.en_to_ru_model}")
            try:
                self.en_ru_pipe = pipeline(
                    "translation",
                    model=self.en_to_ru_model,
                )
                logger.info("✓ EN→RU model loaded")
            except Exception as e:
                logger.error(f"Failed to load EN→RU model: {e}")
                self.en_ru_pipe = None
    
    def translate_ru_to_en(self, text: str) -> str:
        """
        Translate Russian text to English
        
        Args:
            text: Russian text
            
        Returns:
            English translation
        """
        self.load_ru_to_en()
        
        if self.ru_en_pipe is None:
            logger.warning("Translation model not available")
            return text
        
        try:
            # Split long texts into chunks (MarianMT has token limits)
            chunks = self._chunk_text(text, max_length=400)
            translations = []
            
            for chunk in chunks:
                result = self.ru_en_pipe(chunk, max_length=512)
                translations.append(result[0]['translation_text'])
            
            translated = ' '.join(translations)
            logger.info("✓ Translated RU→EN")
            return translated
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def translate_en_to_ru(self, text: str) -> str:
        """
        Translate English text to Russian
        
        Args:
            text: English text
            
        Returns:
            Russian translation
        """
        self.load_en_to_ru()
        
        if self.en_ru_pipe is None:
            logger.warning("Translation model not available")
            return text
        
        try:
            chunks = self._chunk_text(text, max_length=400)
            translations = []
            
            for chunk in chunks:
                result = self.en_ru_pipe(chunk, max_length=512)
                translations.append(result[0]['translation_text'])
            
            translated = ' '.join(translations)
            logger.info("✓ Translated EN→RU")
            return translated
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def _chunk_text(self, text: str, max_length: int = 400) -> list:
        """
        Split text into chunks for translation
        
        Args:
            text: Text to chunk
            max_length: Maximum chunk length
            
        Returns:
            List of chunks
        """
        if len(text) <= max_length:
            return [text]
        
        # Split by sentences
        sentences = text.replace('。', '.').split('.')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_length:
                if current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection (Russian vs English)
        
        Args:
            text: Text to analyze
            
        Returns:
            'ru' or 'en'
        """
        # Simple heuristic: count Cyrillic characters
        cyrillic_count = sum(1 for char in text if '\u0400' <= char <= '\u04FF')
        total_alpha = sum(1 for char in text if char.isalpha())
        
        if total_alpha == 0:
            return 'unknown'
        
        cyrillic_ratio = cyrillic_count / total_alpha
        
        return 'ru' if cyrillic_ratio > 0.5 else 'en'


def main():
    """
    Test the Translator Agent
    """
    agent = TranslatorAgent()
    
    ru_text = "Отсутствие чека не является основанием для отказа в возврате товара."
    
    print("=" * 60)
    print("Original (RU):", ru_text)
    print("=" * 60)
    
    en_translation = agent.translate_ru_to_en(ru_text)
    print("Translation (EN):", en_translation)
    print("=" * 60)
    
    # Test language detection
    print("Detected language:", agent.detect_language(ru_text))


if __name__ == "__main__":
    main()

