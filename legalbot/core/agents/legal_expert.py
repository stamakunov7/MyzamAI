"""
Legal Expert Agent - Interprets legal articles and provides analysis
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LegalExpertAgent:
    """
    Agent that interprets legal texts and provides expert analysis
    """
    
    def __init__(self, model_name: str = "HuggingFaceH4/zephyr-7b-beta"):
        """
        Initialize Legal Expert Agent
        
        Args:
            model_name: HuggingFace model for text generation
        """
        self.model_name = model_name
        self.pipe = None
        logger.info(f"Initializing Legal Expert Agent with model: {model_name}")
        
    def load_model(self):
        """
        Load the LLM model (lazy loading)
        """
        if self.pipe is None:
            logger.info(f"Loading model: {self.model_name}")
            
            try:
                # Load with reduced precision for better performance
                self.pipe = pipeline(
                    "text-generation",
                    model=self.model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                )
                logger.info("✓ Model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                # Fallback to smaller model if main model fails
                logger.info("Attempting fallback to smaller model...")
                self.model_name = "microsoft/phi-2"
                self.pipe = pipeline(
                    "text-generation",
                    model=self.model_name,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.7,
                )
                logger.info("✓ Fallback model loaded")
    
    def interpret(self, query: str, legal_texts: str) -> str:
        """
        Interpret legal texts in the context of user query
        
        Args:
            query: User's question
            legal_texts: Retrieved legal articles
            
        Returns:
            Expert interpretation
        """
        self.load_model()
        
        prompt = f"""<|system|>
Ты юридический эксперт по гражданскому праву Кыргызской Республики. Твоя задача - дать четкий и понятный ответ на основе предоставленных законодательных статей.
</s>
<|user|>
Вопрос: {query}

Релевантные статьи из Гражданского кодекса:
{legal_texts}

Предоставь юридический анализ, используя эти статьи. Объясни простым языком, что говорит закон по данному вопросу.
</s>
<|assistant|>
"""
        
        try:
            logger.info("Generating legal interpretation...")
            response = self.pipe(
                prompt,
                max_new_tokens=400,
                num_return_sequences=1,
                pad_token_id=self.pipe.tokenizer.eos_token_id,
            )
            
            # Extract generated text
            generated = response[0]['generated_text']
            
            # Extract only the assistant's response
            if "<|assistant|>" in generated:
                answer = generated.split("<|assistant|>")[-1].strip()
            else:
                answer = generated.split(prompt)[-1].strip()
            
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
    Test the Legal Expert Agent
    """
    agent = LegalExpertAgent()
    
    query = "Могу ли я вернуть товар без чека?"
    legal_text = """Статья 22. Отсутствие кассового или товарного чека
Отсутствие у потребителя кассового или товарного чека либо иного документа, удостоверяющих факт и условия покупки товара, не является основанием для отказа в удовлетворении его требований."""
    
    result = agent.interpret(query, legal_text)
    print("=" * 60)
    print("Legal Expert Response:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()

