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
        
        # Parse the legal interpretation to extract structured parts
        # Expected format: "Ответ: ... Основание: ... Совет: ..."
        
        # Create clean formatted response for Telegram with bold/italic
        response_parts = []
        
        # Check if this is out-of-scope question (not civil law)
        is_out_of_scope = any(keyword in legal_interpretation.lower() for keyword in [
            "уголовн", "налог", "семейн", "не относится к гражданскому праву",
            "обратитесь к", "кодекс", "вне компетенции"
        ])
        
        # Header with emoji (bold) - Notion AI style
        if is_out_of_scope:
            response_parts.append("ℹ️ **Информация**\n")
        else:
            response_parts.append("⚖️ **Информационно-правовой ответ**\n")
        
        # Add separator line
        response_parts.append("━━━━━━━━━━━━━━━━━━━\n")
        
        # Check if the interpretation already has structure
        if "Ответ:" in legal_interpretation:
            # Parse structured response and format beautifully
            lines = legal_interpretation.split('\n')
            formatted_lines = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("Ответ:"):
                    # Clean up the answer text
                    answer_text = line.replace("Ответ:", "").strip()
                    formatted_lines.append("✅ **Ответ:**")
                    formatted_lines.append(answer_text)
                    formatted_lines.append("")  # Empty line
                elif line.startswith("Основание:"):
                    # Clean up the foundation text
                    foundation_text = line.replace("Основание:", "").strip()
                    formatted_lines.append("📚 **Основание:**")
                    formatted_lines.append(f"_{foundation_text}_")
                    formatted_lines.append("")  # Empty line
                elif line.startswith("Совет:"):
                    # Clean up the advice text and capitalize first letter
                    advice_text = line.replace("Совет:", "").strip()
                    # Capitalize first letter
                    if advice_text:
                        advice_text = advice_text[0].upper() + advice_text[1:]
                    formatted_lines.append("💡 **Совет:**")
                    formatted_lines.append(advice_text)
                elif line and not line.startswith("Ответ:") and not line.startswith("Основание:") and not line.startswith("Совет:"):
                    # Additional text that doesn't fit the structure
                    formatted_lines.append(line)
            
            response_parts.append("\n".join(formatted_lines))
        else:
            # Not structured, add basic formatting
            response_parts.append(f"**Ответ:**\n{legal_interpretation}\n")
            
            # Add source if provided
            if source_articles and len(source_articles) > 0:
                response_parts.append(f"\n📚 **Основание:**\n_{source_articles[0][:200]}_")
        
        # Add bottom separator
        response_parts.append("\n━━━━━━━━━━━━━━━━━━━")
        
        # Legal disclaimer (italic) - Notion AI style
        if include_disclaimer:
            response_parts.append("\n⚠️ _Ответ предоставлен в информационных целях и не является юридической консультацией._")
        
        # Footer with timestamp
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        response_parts.append(f"\n🤖 *MyzamAI | {timestamp}*")
        
        formatted_response = "\n".join(response_parts)
        
        # Ensure Telegram message length limit (4096 characters)
        if len(formatted_response) > 4000:
            formatted_response = formatted_response[:3900] + "\n\n⚠️ Ответ предоставлен в информационных целях и не является юридической консультацией.\n\n🤖 MyzamAI | " + timestamp
        
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
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        
        # Make error messages more user-friendly
        friendly_message = error_message
        if "работаю только на русском языке" in error_message:
            return f"""🌍 *Языковая поддержка*

{friendly_message}

💡 *Доступные команды:*
• `/start` - начать работу
• `/help` - справка по использованию
• `/law <номер>` - получить статью

🤖 *MyzamAI | {timestamp}*"""
        elif "Broken pipe" in error_message or "Errno 32" in error_message:
            friendly_message = "Временная проблема с подключением к сервису. Попробуйте через несколько секунд."
        elif "Conflict" in error_message or "getUpdates" in error_message:
            friendly_message = "Бот перезапускается. Подождите несколько секунд и попробуйте снова."
        elif "timeout" in error_message.lower():
            friendly_message = "Превышено время ожидания ответа. Попробуйте позже."
        
        return f"""❌ *Временная ошибка*

К сожалению, не удалось обработать ваш запрос.

*Причина:* {friendly_message}

💡 *Что делать:*
• Подождите 10-15 секунд и попробуйте снова
• Попробуйте переформулировать вопрос
• Используйте /help для справки

⚠️ Если проблема повторяется - бот может быть временно недоступен.

🤖 MyzamAI | {timestamp}"""
    
    def format_welcome(self) -> str:
        """
        Format welcome message
        
        Returns:
            Welcome message
        """
        return """👋 *Добро пожаловать в MyzamAI*

Я ваш AI-ассистент по гражданскому праву Кыргызской Республики. 

*Что я умею:*
⚖️ Отвечать на юридические вопросы
📚 Находить релевантные статьи закона
💡 Давать практические рекомендации
🔄 Работать на русском и английском языках

*Примеры вопросов:*
• "Как правильно заключить договор аренды?"
• "Можно ли расторгнуть трудовой договор досрочно?"
• "Какие права у покупателя при возврате товара?"

*Команды:*
/start - начать работу
/help - подробная справка
/law <номер> - получить конкретную статью

⚠️ *Важно:* Я специализируюсь на гражданском праве КР. Вопросы по уголовному, налоговому или семейному праву — вне моей компетенции.

🤖 MyzamAI v1.0 | Powered by Meta Llama 3"""
    
    def format_help(self) -> str:
        """
        Format help message
        
        Returns:
            Help message
        """
        return """📖 *Справка по использованию MyzamAI*

*Основные команды:*
/start - перезапустить бота
/help - показать эту справку
/law <номер> - получить текст конкретной статьи

*Как задавать вопросы:*
✅ Хорошие примеры:
• "Какие права у покупателя при возврате товара?"
• "Можно ли расторгнуть трудовой договор досрочно?"
• "Что нужно для вступления в наследство?"

❌ Плохие примеры:
• "Помоги" (слишком общий)
• "!!!" (не информативно)

*О боте:*
🤖 MyzamAI - AI-ассистент по гражданскому праву КР
⚡ Работает на базе Meta Llama 3
📚 База: Гражданский кодекс КР

*Важно:*
• Информация носит справочный характер
• Не заменяет консультацию юриста
• Вопросы по уголовному/семейному праву - вне компетенции

*Языки:*
Бот понимает русский и английский

🤖 MyzamAI v1.0 | Powered by Meta Llama 3"""


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

