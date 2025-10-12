"""
User Interface Agent - Formats responses for Telegram interface
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserInterfaceAgent:
    """
    Agent that formats legal responses for optimal user experience in Telegram
    """
    
    def __init__(self):
        """
        Initialize User Interface Agent
        """
        logger.info("User Interface Agent initialized")
    
    def format_response(self, 
                       query: str,
                       legal_interpretation: str,
                       source_articles: list = None,
                       include_disclaimer: bool = True) -> str:
        """
        Format the complete response for Telegram
        
        Args:
            query: Original user query
            legal_interpretation: Legal expert's interpretation
            source_articles: List of source article references
            include_disclaimer: Whether to include legal disclaimer
            
        Returns:
            Formatted message for Telegram
        """
        logger.info("Formatting response for user...")
        
        # Build the response
        response_parts = []
        
        # Header with emoji
        response_parts.append("⚖️ **Юридическая консультация**\n")
        
        # Question recap
        response_parts.append(f"**Ваш вопрос:**\n_{query}_\n")
        
        # Main interpretation
        response_parts.append(f"**Ответ:**\n{legal_interpretation}\n")
        
        # Source references
        if source_articles and len(source_articles) > 0:
            response_parts.append("\n📚 **Правовая основа:**")
            for i, article in enumerate(source_articles[:3], 1):
                # Extract article number if present
                article_preview = article[:150] + "..." if len(article) > 150 else article
                response_parts.append(f"{i}. {article_preview}")
            response_parts.append("")
        
        # Practical tips
        response_parts.append("💡 **Рекомендации:**")
        tips = self._generate_tips(query, legal_interpretation)
        response_parts.append(tips)
        
        # Legal disclaimer
        if include_disclaimer:
            response_parts.append("\n⚠️ _Данная информация носит справочный характер. Для получения персональной юридической консультации обратитесь к квалифицированному юристу._")
        
        # Footer
        response_parts.append(f"\n🤖 LegalBot+ | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        
        formatted_response = "\n".join(response_parts)
        
        # Ensure Telegram message length limit (4096 characters)
        if len(formatted_response) > 4000:
            formatted_response = formatted_response[:3900] + "\n\n... [текст сокращен]\n\n" + response_parts[-2] + "\n" + response_parts[-1]
        
        logger.info("✓ Response formatted successfully")
        return formatted_response
    
    def _generate_tips(self, query: str, interpretation: str) -> str:
        """
        Generate practical tips based on query context
        
        Args:
            query: User query
            interpretation: Legal interpretation
            
        Returns:
            Practical tips text
        """
        query_lower = query.lower()
        
        # Context-aware tips
        if 'возврат' in query_lower or 'вернуть' in query_lower:
            return "• Сохраняйте все документы о покупке\n• Товар должен быть в надлежащем состоянии\n• Соберите свидетельские показания если нет чека"
        
        elif 'договор' in query_lower:
            return "• Внимательно читайте все условия договора\n• Проверяйте наличие всех подписей и печатей\n• Сохраняйте копии всех документов"
        
        elif 'наследство' in query_lower or 'наследник' in query_lower:
            return "• Обратитесь к нотариусу в течение 6 месяцев\n• Подготовьте документы, подтверждающие родство\n• Узнайте о возможных долгах наследодателя"
        
        elif 'работ' in query_lower or 'трудов' in query_lower:
            return "• Требуйте письменное оформление трудового договора\n• Знайте свои права согласно трудовому законодательству\n• Сохраняйте все документы, связанные с работой"
        
        elif 'аренд' in query_lower:
            return "• Заключите письменный договор аренды\n• Зафиксируйте состояние имущества при передаче\n• Соблюдайте сроки оплаты"
        
        else:
            return "• Проконсультируйтесь с профессиональным юристом\n• Соберите все относящиеся к делу документы\n• Действуйте в установленные законом сроки"
    
    def format_error(self, error_message: str) -> str:
        """
        Format error message for user
        
        Args:
            error_message: Error description
            
        Returns:
            User-friendly error message
        """
        return f"""❌ **Ошибка**

К сожалению, произошла ошибка при обработке вашего запроса.

**Детали:** {error_message}

Пожалуйста, попробуйте:
• Переформулировать вопрос
• Использовать команду /help для справки
• Попробовать позже

Если проблема сохраняется, обратитесь в поддержку.

🤖 LegalBot+"""
    
    def format_welcome(self) -> str:
        """
        Format welcome message
        
        Returns:
            Welcome message
        """
        return """👋 **Добро пожаловать в LegalBot+**

Я ваш AI-помощник по гражданскому праву Кыргызской Республики.

**Что я умею:**
⚖️ Отвечать на юридические вопросы
📚 Находить релевантные статьи закона
💡 Давать практические рекомендации
🔄 Работать на русском и английском языках

**Как пользоваться:**
Просто напишите ваш вопрос, например:
_"Могу ли я вернуть товар без чека?"_

**Команды:**
/start - начать работу
/help - справка
/law <номер> - получить конкретную статью

⚠️ Помните: бот предоставляет справочную информацию, не заменяющую профессиональную юридическую консультацию.

🤖 Готов ответить на ваши вопросы!"""
    
    def format_help(self) -> str:
        """
        Format help message
        
        Returns:
            Help message
        """
        return """📖 **Справка по использованию LegalBot+**

**Основные команды:**
/start - перезапустить бота
/help - показать эту справку
/law <номер> - получить текст конкретной статьи

**Как задавать вопросы:**
✅ Хорошие вопросы:
• "Какие права у покупателя при возврате товара?"
• "Можно ли расторгнуть трудовой договор досрочно?"
• "Что нужно для вступления в наследство?"

❌ Плохие вопросы:
• "Помоги" (слишком общий)
• "!!!" (не информативно)

**Языки:**
Бот понимает русский и английский языки.

**Ограничения:**
• Бот основан на Гражданском кодексе КР
• Информация носит справочный характер
• Не заменяет консультацию юриста

**Поддержка:**
По вопросам и предложениям: @support

🤖 LegalBot+ v1.0"""


def main():
    """
    Test the User Interface Agent
    """
    agent = UserInterfaceAgent()
    
    query = "Могу ли я вернуть товар без чека?"
    interpretation = "Согласно статье 22 Гражданского кодекса КР, отсутствие кассового чека не является основанием для отказа в удовлетворении требований потребителя."
    sources = ["Статья 22. Отсутствие кассового или товарного чека..."]
    
    print("=" * 60)
    print("Formatted Response:")
    print("=" * 60)
    print(agent.format_response(query, interpretation, sources))
    
    print("\n" + "=" * 60)
    print("Welcome Message:")
    print("=" * 60)
    print(agent.format_welcome())


if __name__ == "__main__":
    main()

