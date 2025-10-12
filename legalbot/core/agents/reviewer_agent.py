"""
Reviewer Agent - Checks quality and accuracy of legal responses
"""

import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReviewerAgent:
    """
    Agent that reviews legal responses for accuracy and completeness
    Performs self-correction loop if needed
    """
    
    def __init__(self, model_name: str = "HuggingFaceH4/zephyr-7b-beta"):
        """
        Initialize Reviewer Agent
        
        Args:
            model_name: HuggingFace model for review
        """
        self.model_name = model_name
        self.pipe = None
        self.review_log = []
        logger.info("Reviewer Agent initialized")
    
    def load_model(self):
        """
        Load the review model (lazy loading)
        """
        if self.pipe is None:
            logger.info(f"Loading review model: {self.model_name}")
            
            try:
                self.pipe = pipeline(
                    "text-generation",
                    model=self.model_name,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    max_new_tokens=300,
                )
                logger.info("✓ Review model loaded")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.pipe = None
    
    def review(self, query: str, legal_texts: str, response: str) -> dict:
        """
        Review the generated response for accuracy and completeness
        
        Args:
            query: Original user query
            legal_texts: Retrieved legal texts
            response: Generated response to review
            
        Returns:
            dict with 'approved', 'feedback', and 'corrected_response'
        """
        logger.info("Reviewing response...")
        
        # Rule-based checks first
        basic_checks = self._basic_checks(query, legal_texts, response)
        
        if not basic_checks['passed']:
            logger.warning(f"Basic checks failed: {basic_checks['reason']}")
            self.review_log.append({
                'query': query,
                'response': response,
                'issue': basic_checks['reason']
            })
            return {
                'approved': False,
                'feedback': basic_checks['reason'],
                'corrected_response': response
            }
        
        # Deep review using LLM (optional, can be disabled for performance)
        if self.pipe:
            llm_review = self._llm_review(query, legal_texts, response)
            return llm_review
        
        # If LLM not available, approve if basic checks passed
        return {
            'approved': True,
            'feedback': 'Response passed basic validation checks',
            'corrected_response': response
        }
    
    def _basic_checks(self, query: str, legal_texts: str, response: str) -> dict:
        """
        Perform basic rule-based checks
        
        Args:
            query: User query
            legal_texts: Legal texts
            response: Generated response
            
        Returns:
            dict with 'passed' and 'reason'
        """
        # Check 1: Response is not empty
        if not response or len(response.strip()) < 20:
            return {'passed': False, 'reason': 'Ответ слишком короткий или пустой'}
        
        # Check 2: Response should mention legal context
        legal_keywords = ['статья', 'закон', 'кодекс', 'право', 'договор', 'суд']
        has_legal_context = any(keyword in response.lower() for keyword in legal_keywords)
        
        if not has_legal_context and len(legal_texts) > 0:
            return {'passed': False, 'reason': 'Ответ не содержит юридического контекста'}
        
        # Check 3: Response should be relevant to query
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        common_words = query_words & response_words
        
        # At least 2 common words (excluding stop words)
        stop_words = {'я', 'в', 'на', 'и', 'с', 'по', 'к', 'о', 'у', 'из', 'за', 'до', 'от'}
        meaningful_common = common_words - stop_words
        
        if len(meaningful_common) < 2 and len(query_words) > 3:
            return {'passed': False, 'reason': 'Ответ может не соответствовать вопросу'}
        
        return {'passed': True, 'reason': 'All basic checks passed'}
    
    def _llm_review(self, query: str, legal_texts: str, response: str) -> dict:
        """
        Deep review using LLM
        
        Args:
            query: User query
            legal_texts: Legal texts
            response: Generated response
            
        Returns:
            Review result dict
        """
        self.load_model()
        
        prompt = f"""<|system|>
Ты эксперт по контролю качества юридических консультаций. Оцени предоставленный ответ на юридический вопрос.
</s>
<|user|>
Вопрос пользователя: {query}

Юридические статьи:
{legal_texts[:500]}...

Предоставленный ответ:
{response}

Оцени этот ответ по следующим критериям:
1. Точность (соответствует ли ответ законодательству?)
2. Полнота (отвечает ли на вопрос?)
3. Ясность (понятен ли ответ?)

Ответь в формате:
ОДОБРЕНО: Да/Нет
ЗАМЕЧАНИЯ: [если есть]
</s>
<|assistant|>
"""
        
        try:
            result = self.pipe(
                prompt,
                max_new_tokens=150,
                num_return_sequences=1,
                pad_token_id=self.pipe.tokenizer.eos_token_id,
            )
            
            generated = result[0]['generated_text']
            
            if "<|assistant|>" in generated:
                review_text = generated.split("<|assistant|>")[-1].strip()
            else:
                review_text = generated.split(prompt)[-1].strip()
            
            # Parse review
            approved = 'да' in review_text.lower()[:100] or 'одобрено: да' in review_text.lower()
            
            logger.info(f"✓ LLM review completed. Approved: {approved}")
            
            return {
                'approved': approved,
                'feedback': review_text,
                'corrected_response': response
            }
            
        except Exception as e:
            logger.error(f"LLM review error: {e}")
            return {
                'approved': True,
                'feedback': 'Review system unavailable, accepting response',
                'corrected_response': response
            }
    
    def get_review_log(self) -> list:
        """
        Get log of problematic responses
        
        Returns:
            List of review log entries
        """
        return self.review_log
    
    def clear_log(self):
        """
        Clear the review log
        """
        self.review_log = []
        logger.info("Review log cleared")


def main():
    """
    Test the Reviewer Agent
    """
    agent = ReviewerAgent()
    
    query = "Могу ли я вернуть товар без чека?"
    legal_text = """Статья 22. Отсутствие кассового или товарного чека
Отсутствие у потребителя кассового или товарного чека не является основанием для отказа."""
    response = "Да, согласно статье 22, вы можете вернуть товар без чека, используя свидетельские показания."
    
    review_result = agent.review(query, legal_text, response)
    
    print("=" * 60)
    print("Review Result:")
    print("=" * 60)
    print(f"Approved: {review_result['approved']}")
    print(f"Feedback: {review_result['feedback']}")


if __name__ == "__main__":
    main()

