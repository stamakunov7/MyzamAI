"""
Unit tests for agent classes
Tests individual agent functionality without full pipeline
"""

import pytest
import os
import sys
from unittest.mock import Mock, MagicMock, patch

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)


@pytest.mark.unit
class TestLegalExpertAgent:
    """Tests for LegalExpertAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        from src.core.agents.legal_expert import LegalExpertAgent
        
        agent = LegalExpertAgent()
        assert agent is not None
        assert hasattr(agent, 'llm')
    
    def test_fallback_interpretation(self):
        """Test fallback when LLM is unavailable"""
        from src.core.agents.legal_expert import LegalExpertAgent
        
        agent = LegalExpertAgent()
        agent.llm = None
        
        query = "Могу ли я вернуть товар?"
        legal_text = "Статья 22. Текст статьи"
        
        result = agent.interpret(query, legal_text)
        
        assert result is not None
        assert len(result) > 0
        assert "Гражданского кодекса" in result or "статья" in result.lower()
    
    @patch('src.core.agents.legal_expert.llama')
    def test_interpret_with_llm(self, mock_llama):
        """Test interpretation with mocked LLM"""
        from src.core.agents.legal_expert import LegalExpertAgent
        
        # Mock LLM response
        mock_response = [{
            "generated_text": "Ответ: Да, можете. Основание: Статья 22."
        }]
        mock_llama.return_value = mock_response
        
        agent = LegalExpertAgent()
        agent.llm = Mock(return_value=mock_response)
        
        query = "Могу ли я вернуть товар?"
        legal_text = "Статья 22. Текст"
        
        result = agent.interpret(query, legal_text)
        
        assert result is not None
        assert len(result) > 0


@pytest.mark.unit
class TestReviewerAgent:
    """Tests for ReviewerAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        assert agent is not None
        assert hasattr(agent, 'llm')
        assert hasattr(agent, 'review_log')
        assert agent.review_log == []
    
    def test_basic_checks_empty_response(self):
        """Test basic checks with empty response"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        
        query = "Тест"
        legal_text = "Статья 1"
        response = ""  # Empty response
        
        result = agent.review(query, legal_text, response)
        
        assert result['approved'] == False
        assert 'короткий' in result['feedback'].lower() or 'пустой' in result['feedback'].lower()
    
    def test_basic_checks_short_response(self):
        """Test basic checks with very short response"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        
        query = "Могу ли я вернуть товар?"
        legal_text = "Статья 22. Текст статьи о возврате товара."
        response = "Да"  # Too short
        
        result = agent.review(query, legal_text, response)
        
        assert result['approved'] == False
    
    def test_basic_checks_no_legal_context(self):
        """Test basic checks with response lacking legal context"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        
        query = "Как дела?"
        legal_text = "Статья 1. Текст"
        response = "Хорошо, спасибо!"  # No legal context
        
        result = agent.review(query, legal_text, response)
        
        assert result['approved'] == False
    
    def test_basic_checks_valid_response(self):
        """Test basic checks with valid response"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        agent.llm = None  # Disable LLM for basic checks
        
        query = "Могу ли я вернуть товар?"
        legal_text = "Статья 22. Текст о возврате товара."
        response = "Да, согласно статье 22 Гражданского кодекса, вы можете вернуть товар без чека."
        
        result = agent.review(query, legal_text, response)
        
        # Should pass basic checks (but may fail LLM review if enabled)
        assert result is not None
        assert 'approved' in result
    
    def test_get_review_log(self):
        """Test getting review log"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        
        # Add some entries to log
        agent.review_log = [
            {'query': 'test1', 'response': 'resp1', 'issue': 'issue1'}
        ]
        
        log = agent.get_review_log()
        
        assert len(log) == 1
        assert log[0]['query'] == 'test1'
    
    def test_clear_log(self):
        """Test clearing review log"""
        from src.core.agents.reviewer_agent import ReviewerAgent
        
        agent = ReviewerAgent()
        agent.review_log = [{'test': 'entry'}]
        
        agent.clear_log()
        
        assert agent.review_log == []


@pytest.mark.unit
class TestSummarizerAgent:
    """Tests for SummarizerAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        from src.core.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        assert agent is not None
        assert hasattr(agent, 'llm')
    
    def test_summarize_short_text(self):
        """Test that short text is returned as-is"""
        from src.core.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        
        short_text = "Статья 1. Короткий текст."
        result = agent.summarize(short_text)
        
        assert result == short_text
    
    def test_extractive_summarize(self):
        """Test extractive summarization fallback"""
        from src.core.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        agent.llm = None
        
        long_text = "Статья 1. " + ". ".join([f"Предложение {i}." for i in range(10)])
        result = agent._extractive_summarize(long_text, max_length=100)
        
        assert result is not None
        assert len(result) <= 150  # Some tolerance
        assert "Статья 1" in result
    
    def test_condense_for_telegram_short(self):
        """Test condensing for Telegram with short text"""
        from src.core.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        
        short_text = "Короткий текст."
        result = agent.condense_for_telegram(short_text)
        
        assert result == short_text
    
    def test_condense_for_telegram_long(self):
        """Test condensing for Telegram with long text"""
        from src.core.agents.summarizer import SummarizerAgent
        
        agent = SummarizerAgent()
        agent.llm = None  # Use extractive summarization
        
        # Create text longer than 4000 chars
        long_text = "Статья 1. " + "Текст. " * 1000
        result = agent.condense_for_telegram(long_text)
        
        assert result is not None
        assert len(result) < len(long_text)


@pytest.mark.unit
class TestTranslatorAgent:
    """Tests for TranslatorAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        assert agent is not None
        assert hasattr(agent, 'ru_to_en_model')
        assert hasattr(agent, 'en_to_ru_model')
    
    def test_detect_language_russian(self):
        """Test Russian language detection"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        
        ru_text = "Статья 22. Отсутствие чека не является основанием."
        result = agent.detect_language(ru_text)
        
        assert result == 'ru'
    
    def test_detect_language_english(self):
        """Test English language detection"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        
        en_text = "Article 22. Absence of receipt is not a basis."
        result = agent.detect_language(en_text)
        
        assert result == 'en'
    
    def test_detect_language_mixed(self):
        """Test language detection with mixed text"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        
        # More Cyrillic than Latin
        mixed_text = "Статья 22. Article text here but больше русских букв."
        result = agent.detect_language(mixed_text)
        
        assert result == 'ru'
    
    def test_chunk_text_short(self):
        """Test chunking with short text"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        
        short_text = "Короткий текст."
        chunks = agent._chunk_text(short_text, max_length=400)
        
        assert len(chunks) == 1
        assert chunks[0] == short_text
    
    def test_chunk_text_long(self):
        """Test chunking with long text"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        
        long_text = ". ".join([f"Предложение {i}" for i in range(20)])
        chunks = agent._chunk_text(long_text, max_length=100)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 120 for chunk in chunks)  # Some tolerance
    
    def test_translate_ru_to_en_no_model(self):
        """Test translation when model is not loaded"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        agent.ru_en_pipe = None
        
        ru_text = "Статья 22."
        result = agent.translate_ru_to_en(ru_text)
        
        # Should return original text if model unavailable
        assert result == ru_text
    
    def test_translate_en_to_ru_no_model(self):
        """Test translation when model is not loaded"""
        from src.core.agents.translator import TranslatorAgent
        
        agent = TranslatorAgent()
        agent.en_ru_pipe = None
        
        en_text = "Article 22."
        result = agent.translate_en_to_ru(en_text)
        
        # Should return original text if model unavailable
        assert result == en_text


@pytest.mark.unit
class TestUserInterfaceAgent:
    """Tests for UserInterfaceAgent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        assert agent is not None
    
    def test_format_response_structured(self):
        """Test formatting structured response"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Могу ли я вернуть товар?"
        interpretation = """Ответ: Да, можете вернуть товар без чека.
Основание: Статья 22 Гражданского кодекса.
Совет: Сохраните все документы о покупке."""
        sources = ["Статья 22"]
        
        result = agent.format_response(query, interpretation, sources)
        
        assert "Ответ" in result
        assert "Основание" in result
        assert "Совет" in result
        assert len(result) > 0
    
    def test_format_response_unstructured(self):
        """Test formatting unstructured response"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Тест"
        interpretation = "Простой ответ без структуры."
        sources = ["Статья 1"]
        
        result = agent.format_response(query, interpretation, sources)
        
        assert "Ответ" in result or "Простой ответ" in result
        assert len(result) > 0
    
    def test_format_error(self):
        """Test error message formatting"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        error = "Test error message"
        result = agent.format_error(error)
        
        assert "ошибка" in result.lower() or "error" in result.lower()
        assert "MyzamAI" in result
    
    def test_format_error_language(self):
        """Test error formatting for language errors"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        error = "Я работаю только на русском языке"
        result = agent.format_error(error)
        
        assert "Языковая" in result or "язык" in result.lower()
        assert "/start" in result or "/help" in result
    
    def test_format_welcome(self):
        """Test welcome message formatting"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        result = agent.format_welcome()
        
        assert "MyzamAI" in result
        assert "Добро пожаловать" in result or "welcome" in result.lower()
        assert "/start" in result or "/help" in result
    
    def test_format_help(self):
        """Test help message formatting"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        result = agent.format_help()
        
        assert "MyzamAI" in result
        assert "команды" in result.lower() or "commands" in result.lower()
        assert "/law" in result
    
    def test_generate_tips_return(self):
        """Test tip generation for return queries"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Могу ли я вернуть товар?"
        interpretation = "Да, можете."
        
        tips = agent._generate_tips(query, interpretation)
        
        assert "документ" in tips.lower() or "чек" in tips.lower()
    
    def test_generate_tips_contract(self):
        """Test tip generation for contract queries"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Как заключить договор?"
        interpretation = "Текст ответа"
        
        tips = agent._generate_tips(query, interpretation)
        
        assert "договор" in tips.lower() or "документ" in tips.lower()
    
    def test_format_response_length_limit(self):
        """Test that response respects Telegram length limits"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Тест"
        # Create very long interpretation
        interpretation = "Ответ: " + "Текст. " * 1000
        sources = ["Статья 1"]
        
        result = agent.format_response(query, interpretation, sources)
        
        # Should be under 4100 chars (Telegram limit)
        assert len(result) <= 4100
    
    def test_format_response_out_of_scope(self):
        """Test formatting for out-of-scope questions"""
        from src.core.agents.user_interface_agent import UserInterfaceAgent
        
        agent = UserInterfaceAgent()
        
        query = "Какая статья за кражу?"
        interpretation = "Этот вопрос не относится к гражданскому праву. Обратитесь к Уголовному кодексу."
        sources = []
        
        result = agent.format_response(query, interpretation, sources)
        
        # Should indicate it's informational, not legal advice
        assert "Информация" in result or "информационно" in result.lower()

