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

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import configuration with .env support
try:
    import config
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
except (ImportError, ValueError) as e:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TELEGRAM_BOT_TOKEN:
        logger.warning(f"Configuration error: {e}")

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ChatAction

from core.law_retriever import LawRetriever
from core.agents import (
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
        self.memory_file = os.path.join(os.path.dirname(index_dir), 'memory.json')
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
            
            # Step 2: Translate to Russian if needed
            query_ru = query
            if detected_lang == 'en':
                logger.info("Translating query to Russian...")
                query_ru = self.translator.translate_en_to_ru(query)
            
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
            # Search for article in chunks
            results = self.retriever.search(f"Статья {article_num}", top_k=1)
            if results:
                return results[0][0]
            return None
        except Exception as e:
            logger.error(f"Error retrieving article: {e}")
            return None


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
                response = f"📚 **Статья {article_num}**\n\n{article}"
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
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle user messages
        """
        user_query = update.message.text
        user_id = str(update.effective_user.id)
        
        logger.info(f"Received query from user {user_id}: {user_query}")
        
        # Send typing indicator
        await update.message.chat.send_action(ChatAction.TYPING)
        
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
    project_root = os.path.dirname(script_dir)
    index_dir = os.path.join(project_root, 'faiss_index')
    
    # Check if FAISS index exists
    if not os.path.exists(os.path.join(index_dir, 'faiss_index.bin')):
        logger.error(
            "FAISS index not found! Please run core/build_faiss_index.py first."
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

