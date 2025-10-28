"""
MyzamAI Main Telegram Bot
Multi-agent orchestration for legal question answering
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)

# Import configuration with .env support
try:
    import config.config as config
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
except (ImportError, ValueError) as e:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TELEGRAM_BOT_TOKEN:
        print(f"Configuration error: {e}")

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ChatAction

from src.core.law_retriever import LawRetriever
from src.core.agents import (
    LegalExpertAgent,
    SummarizerAgent,
    TranslatorAgent,
    ReviewerAgent,
    UserInterfaceAgent
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class LegalBotOrchestrator:
    """
    Orchestrates multi-agent system for legal question answering
    """
    
    def __init__(self, index_dir: str):
        """
        Initialize the orchestrator with all agents
        
        Args:
            index_dir: Directory containing FAISS index
        """
        logger.info("Initializing MyzamAI Orchestrator...")
        
        # Initialize all agents
        self.retriever = LawRetriever(index_dir)
        self.legal_expert = LegalExpertAgent()
        self.summarizer = SummarizerAgent()
        self.translator = TranslatorAgent()
        self.reviewer = ReviewerAgent()
        self.ui_agent = UserInterfaceAgent()
        
        # Memory for conversation history
        self.memory_file = os.path.join(os.path.dirname(index_dir), '..', 'storage', 'memory.json')
        self.memory = self._load_memory()
        
        logger.info("✓ All agents initialized successfully")
    
    def _load_memory(self) -> dict:
        """
        Load conversation memory from file
        
        Returns:
            Memory dictionary
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading memory: {e}")
        
        return {}
    
    def _save_memory(self):
        """
        Save conversation memory to file
        """
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def _update_user_history(self, user_id: str, query: str, response: str):
        """
        Update user conversation history
        
        Args:
            user_id: User ID
            query: User query
            response: Bot response
        """
        if user_id not in self.memory:
            self.memory[user_id] = {
                'first_interaction': datetime.now().isoformat(),
                'queries': []
            }
        
        self.memory[user_id]['queries'].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response[:500]  # Store truncated response
        })
        
        # Keep only last 20 queries per user
        if len(self.memory[user_id]['queries']) > 20:
            self.memory[user_id]['queries'] = self.memory[user_id]['queries'][-20:]
        
        self._save_memory()
    
    async def process_query(self, query: str, user_id: str = None) -> str:
        """
        Process user query through multi-agent pipeline
        
        Args:
            query: User question
            user_id: User ID for memory
            
        Returns:
            Formatted response
        """
        try:
            logger.info(f"Processing query: {query}")
            
            # Step 1: Detect language
            detected_lang = self.translator.detect_language(query)
            logger.info(f"Detected language: {detected_lang}")
            
            # Step 2: Check language support
            if detected_lang != 'ru':
                return self.ui_agent.format_error(
                    "Извините, я работаю только на русском языке. Пожалуйста, задайте вопрос на русском языке."
                )
            
            query_ru = query
            
            # Step 3: Retrieve relevant legal articles
            logger.info("Retrieving relevant legal articles...")
            search_results = self.retriever.search(query_ru, top_k=3)
            
            if not search_results:
                return self.ui_agent.format_error("Не найдено релевантных статей закона")
            
            # Extract articles
            articles = [article for article, _ in search_results]
            legal_texts = "\n\n".join(articles)
            
            logger.info(f"Retrieved {len(articles)} articles")
            
            # Step 4: Legal Expert interpretation
            logger.info("Getting legal expert interpretation...")
            interpretation = self.legal_expert.interpret(query_ru, legal_texts)
            
            # Step 5: Review the interpretation
            logger.info("Reviewing interpretation...")
            review_result = self.reviewer.review(query_ru, legal_texts, interpretation)
            
            if not review_result['approved']:
                logger.warning(f"Review not approved: {review_result['feedback']}")
                # Use corrected response or fallback
                interpretation = review_result.get('corrected_response', interpretation)
            
            # Step 6: Summarize if too long
            logger.info("Checking if summarization needed...")
            interpretation = self.summarizer.condense_for_telegram(interpretation)
            
            # Step 7: Translate back to English if needed
            if detected_lang == 'en':
                logger.info("Translating response to English...")
                interpretation = self.translator.translate_ru_to_en(interpretation)
                articles = [self.translator.translate_ru_to_en(a[:300]) for a in articles]
            
            # Step 8: Format for user interface
            logger.info("Formatting response...")
            formatted_response = self.ui_agent.format_response(
                query=query,
                legal_interpretation=interpretation,
                source_articles=articles
            )
            
            # Step 9: Update memory
            if user_id:
                self._update_user_history(user_id, query, formatted_response)
            
            logger.info("✓ Query processed successfully")
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            return self.ui_agent.format_error(str(e))
    
    def get_article_by_number(self, article_num: int) -> Optional[str]:
        """
        Get specific article by number
        
        Args:
            article_num: Article number
            
        Returns:
            Article text or None
        """
        try:
            # Load chunks directly and search for exact match
            if not hasattr(self.retriever, 'chunks') or self.retriever.chunks is None:
                self.retriever.load()
            
            # Collect all parts of the article with STRICT matching
            article_parts = []
            for chunk in self.retriever.chunks:
                chunk_clean = chunk.strip()
                # STRICT: Must start with exact "Статья {article_num}" pattern
                if chunk_clean.startswith(f"Статья {article_num}"):
                    # Additional validation: ensure it's not a partial match
                    # Check that the next character after the number is not a digit
                    pattern = f"Статья {article_num}"
                    if len(chunk_clean) > len(pattern):
                        next_char = chunk_clean[len(pattern)]
                        if next_char.isdigit():
                            # This is a partial match (e.g., "Статья 37" matches "Статья 379")
                            continue
                    article_parts.append(chunk_clean)
            
            if article_parts:
                # Combine all parts and clean up
                full_article = self._combine_article_parts(article_parts)
                # Final validation: ensure the result starts with the correct article
                if full_article.strip().startswith(f"Статья {article_num}"):
                    return full_article
                else:
                    logger.warning(f"Article {article_num} found but validation failed")
                    return None
            
            # If not found, try FAISS search as fallback with STRICT validation
            results = self.retriever.search(f"Статья {article_num}", top_k=20)
            for chunk, score in results:
                chunk_clean = chunk.strip()
                # STRICT validation for FAISS results too
                if chunk_clean.startswith(f"Статья {article_num}"):
                    # Additional validation for FAISS results
                    pattern = f"Статья {article_num}"
                    if len(chunk_clean) > len(pattern):
                        next_char = chunk_clean[len(pattern)]
                        if next_char.isdigit():
                            continue
                    # Final check: ensure it's the exact article
                    if chunk_clean.startswith(f"Статья {article_num}"):
                        logger.info(f"Found article {article_num} via FAISS search with score {score}")
                        return chunk_clean
            
            logger.warning(f"Article {article_num} not found in database")
            return None
        except Exception as e:
            logger.error(f"Error retrieving article {article_num}: {e}")
            return None
    
    def _combine_article_parts(self, parts: list) -> str:
        """
        Combine article parts and clean up formatting
        
        Args:
            parts: List of article parts
            
        Returns:
            Clean combined article text
        """
        if not parts:
            return ""
        
        # Use only the first complete part to avoid duplication
        # The first part should contain the complete article
        combined = parts[0]
        
        # Clean up the combined text
        combined = self._clean_article_text(combined)
        return combined
    
    def _clean_article_text(self, text: str) -> str:
        """
        Clean up article text by removing extra separators and formatting
        
        Args:
            text: Raw article text
            
        Returns:
            Cleaned article text
        """
        import re
        
        # Remove multiple consecutive separators
        text = re.sub(r'=+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove bullet points that might be artifacts
        text = re.sub(r'^•\s*', '', text, flags=re.MULTILINE)
        
        # Remove duplicate content by finding repeated patterns
        # Split by common patterns and keep only unique parts
        lines = text.split('.')
        unique_lines = []
        seen_content = set()
        
        for line in lines:
            line = line.strip()
            if line and line not in seen_content:
                # Check if this line is not a duplicate of previous content
                is_duplicate = False
                for seen in seen_content:
                    if len(line) > 20 and line in seen:
                        is_duplicate = True
                        break
                    if len(seen) > 20 and seen in line:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_lines.append(line)
                    seen_content.add(line)
        
        # Rejoin the unique content
        text = '. '.join(unique_lines)
        
        # Clean up the text
        text = text.strip()
        
        return text


class TelegramBot:
    """
    Telegram bot interface for MyzamAI
    """
    
    def __init__(self, token: str, orchestrator: LegalBotOrchestrator):
        """
        Initialize Telegram bot
        
        Args:
            token: Telegram bot token
            orchestrator: LegalBot orchestrator
        """
        self.token = token
        self.orchestrator = orchestrator
        self.application = Application.builder().token(token).build()
        
        # Register handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("law", self.law_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("✓ Telegram bot initialized")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command
        """
        welcome_message = self.orchestrator.ui_agent.format_welcome()
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command
        """
        help_message = self.orchestrator.ui_agent.format_help()
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def law_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /law <number> command to get specific article
        """
        try:
            if not context.args:
                await update.message.reply_text(
                    "Использование: /law <номер статьи>\nПример: /law 22"
                )
                return
            
            article_num = int(context.args[0])
            article = self.orchestrator.get_article_by_number(article_num)
            
            if article:
                # Format article beautifully with structure
                response = self._format_article_response(article_num, article)
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    f"❌ Статья {article_num} не найдена в базе данных."
                )
        
        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, укажите номер статьи числом.\nПример: /law 22"
            )
        except Exception as e:
            logger.error(f"Error in law command: {e}")
            await update.message.reply_text("❌ Произошла ошибка при получении статьи.")
    
    def _format_article_response(self, article_num: int, article_text: str) -> str:
        """
        Format article response with beautiful structure
        
        Args:
            article_num: Article number
            article_text: Full article text
            
        Returns:
            Formatted article response
        """
        # Clean up the article text
        article_text = article_text.strip()
        
        # Remove the article header if it's duplicated
        if article_text.startswith(f"Статья {article_num}"):
            # Find the first period after the title
            first_period = article_text.find('.', len(f"Статья {article_num}"))
            if first_period != -1:
                # Extract title and content
                title_part = article_text[:first_period + 1]
                content_part = article_text[first_period + 1:].strip()
                
                # Format beautifully
                response_parts = []
                response_parts.append(f"📚 **{title_part}**")
                response_parts.append("")  # Empty line
                
                # Format content with proper paragraph breaks
                if content_part:
                    # Split by numbered points (1., 2., etc.)
                    import re
                    parts = re.split(r'(\d+\.)', content_part)
                    
                    formatted_content = []
                    for i, part in enumerate(parts):
                        if part.strip():
                            if re.match(r'^\d+\.$', part.strip()):
                                # This is a number, add it with proper spacing
                                formatted_content.append(f"\n\n{part.strip()}")
                            else:
                                # This is content, add it
                                formatted_content.append(part.strip())
                    
                    content_text = ''.join(formatted_content).strip()
                    response_parts.append(content_text)
                
                # Add separator with proper spacing
                response_parts.append("")  # Empty line before separator
                response_parts.append("━━━━━━━━━━━━━━━━━━━")
                
                return '\n'.join(response_parts)
        
        # Fallback: simple formatting
        return f"📚 **Статья {article_num}**\n\n{article_text}"
    
    def _extract_article_number(self, text: str) -> Optional[int]:
        """
        Extract article number from user query
        
        Args:
            text: User query text
            
        Returns:
            Article number if found, None otherwise
        """
        import re
        
        # Patterns to match article numbers - comprehensive list
        patterns = [
            # Basic patterns
            r'статья\s+(\d+)',  # "статья 851"
            r'статья\s*(\d+)',  # "статья851" or "статья 851"
            r'статья\s*№\s*(\d+)',  # "статья №851"
            r'статья\s+номер\s+(\d+)',  # "статья номер 851"
            
            # Action verbs with optional "мне"
            r'дай\s+(?:мне\s+)?статью\s+(\d+)',  # "дай статью 851" or "дай мне статью 851"
            r'покажи\s+(?:мне\s+)?статью\s+(\d+)',  # "покажи статью 851" or "покажи мне статью 851"
            r'найди\s+(?:мне\s+)?статью\s+(\d+)',  # "найди статью 851" or "найди мне статью 851"
            
            # Conversational patterns
            r'дайка\s+(?:мне\s+)?статью\s+(\d+)',  # "дайка статью 851" or "дайка мне статью 851"
            r'покажи-ка\s+(?:мне\s+)?статью\s+(\d+)',  # "покажи-ка статью 851" or "покажи-ка мне статью 851"
            r'что\s+там\s+со\s+статьей\s+(\d+)',  # "что там со статьей 851"
            r'что\s+там\s+в\s+статье\s+(\d+)',  # "что там в статье 851"
            
            # Question patterns
            r'где\s+статья\s+(\d+)\?',  # "где статья 851?"
            r'что\s+в\s+статье\s+(\d+)\?',  # "что в статье 851?"
            r'что\s+говорит\s+статья\s+(\d+)\?',  # "что говорит статья 851?"
            r'что\s+написано\s+в\s+статье\s+(\d+)\?',  # "что написано в статье 851?"
            r'можно\s+ли\s+посмотреть\s+статью\s+(\d+)\?',  # "можно ли посмотреть статью 851?"
            
            # Formal requests
            r'пожалуйста,\s+покажите\s+статью\s+(\d+)',  # "пожалуйста, покажите статью 851"
            r'не\s+могли\s+бы\s+вы\s+показать\s+статью\s+(\d+)\?',  # "не могли бы вы показать статью 851?"
            r'можно\s+ли\s+получить\s+статью\s+(\d+)\?',  # "можно ли получить статью 851?"
            
            # Context patterns
            r'мне\s+нужна\s+статья\s+(\d+)',  # "мне нужна статья 851"
            r'хочу\s+посмотреть\s+статью\s+(\d+)',  # "хочу посмотреть статью 851"
            r'интересует\s+статья\s+(\d+)',  # "интересует статья 851"
            r'расскажи\s+про\s+статью\s+(\d+)',  # "расскажи про статью 851"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return None

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle user messages
        """
        user_query = update.message.text
        user_id = str(update.effective_user.id)
        
        logger.info(f"Received query from user {user_id}: {user_query}")
        
        # Send typing indicator
        await update.message.chat.send_action(ChatAction.TYPING)
        
        # Check if this is a request for a specific article
        article_num = self._extract_article_number(user_query)
        if article_num:
            logger.info(f"Detected article request: {article_num}")
            # Simulate /law command with the extracted article number
            context.args = [str(article_num)]
            await self.law_command(update, context)
            return
        
        # Process query through orchestrator
        response = await self.orchestrator.process_query(user_query, user_id)
        
        # Send response
        try:
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            # Fallback without markdown if parsing fails
            logger.warning(f"Markdown parsing failed: {e}")
            await update.message.reply_text(response)
    
    def run(self):
        """
        Start the bot
        """
        logger.info("🚀 Starting MyzamAI...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """
    Main entry point
    """
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    index_dir = os.path.join(project_root, 'storage', 'faiss_index')
    
    # Check if FAISS index exists
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        logger.error(
            "FAISS index not found! Please run scripts/build_faiss_index.py first."
        )
        sys.exit(1)
    
    # Check if bot token is available
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not found!")
        logger.info("Please set your token in .env file or as environment variable")
        logger.info("\nFor testing without Telegram, you can use the orchestrator directly:")
        
        # Demo mode
        print("\n" + "="*60)
        print("DEMO MODE - Testing orchestrator directly")
        print("="*60 + "\n")
        
        orchestrator = LegalBotOrchestrator(index_dir)
        
        import asyncio
        test_query = "Могу ли я вернуть товар без чека?"
        print(f"Test Query: {test_query}\n")
        
        response = asyncio.run(orchestrator.process_query(test_query))
        print(response)
        
        return
    
    # Initialize orchestrator and bot
    orchestrator = LegalBotOrchestrator(index_dir)
    bot = TelegramBot(TELEGRAM_BOT_TOKEN, orchestrator)
    
    # Run bot
    bot.run()


if __name__ == "__main__":
    main()

