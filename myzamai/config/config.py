"""
Configuration file for MyzamAI
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "⚠️ TELEGRAM_BOT_TOKEN not found!\n"
        "Please set it in .env file or as environment variable.\n"
        "Get your token from @BotFather on Telegram."
    )

# Hugging Face API Configuration
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

if not HUGGINGFACE_API_TOKEN:
    print("⚠️  WARNING: HUGGINGFACE_API_TOKEN not found!")
    print("The bot will not work without Hugging Face API token.")
    print("\n📝 To fix this:")
    print("1. Go to https://huggingface.co/settings/tokens")
    print("2. Create a new token (Write or Read access)")
    print("3. Add to .env file: HUGGINGFACE_API_TOKEN=hf_your_token_here")
    print("4. Restart the bot\n")

# Model Configuration
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Paths
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up from config/ to myzamai/
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
FAISS_INDEX_DIR = os.path.join(PROJECT_ROOT, 'storage', 'faiss_index')
MEMORY_FILE = os.path.join(PROJECT_ROOT, 'storage', 'memory.json')

# Bot Settings
MAX_CONTEXT_LENGTH = 8192
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.2
TOP_P = 0.9

print(f"✅ Configuration loaded")
print(f"✅ Telegram Bot token: {'*' * 15}{TELEGRAM_BOT_TOKEN[-10:]}")
if HUGGINGFACE_API_TOKEN:
    print(f"✅ Hugging Face API token: {'*' * 15}{HUGGINGFACE_API_TOKEN[-10:]}")
    print(f"🚀 LLM will run on HF servers (no local load!)")
else:
    print(f"❌ Hugging Face API token: NOT SET")

