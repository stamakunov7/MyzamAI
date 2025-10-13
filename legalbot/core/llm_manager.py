"""
Centralized LLM Manager for Meta Llama 3
Uses Hugging Face Inference API (no local model loading)
All agents share this single pipeline instance
"""

import os
import logging
from huggingface_hub import InferenceClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"  # Using Llama 3 via API

# Get Hugging Face API token from environment
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if not HF_TOKEN:
    logger.warning("⚠️  HUGGINGFACE_API_TOKEN not found!")
    logger.warning("The bot will not work without API token.")
    logger.info("\n📝 To fix this:")
    logger.info("1. Go to https://huggingface.co/settings/tokens")
    logger.info("2. Create a new token (Write or Read access)")
    logger.info("3. Add to .env file: HUGGINGFACE_API_TOKEN=hf_your_token_here")
    logger.info("4. Restart the bot\n")
    llama = None
else:
    logger.info(f"✅ Using Hugging Face API with model: {MODEL_NAME}")
    logger.info("🚀 Model will run on HF servers (no local GPU/CPU load)")
    
    try:
        # Initialize Hugging Face Inference Client
        client = InferenceClient(token=HF_TOKEN)
        
        # Create a wrapper class that mimics the pipeline interface
        class LlamaAPIWrapper:
            """Wrapper to make HF Inference API compatible with pipeline interface"""
            
            def __init__(self, client, model_name):
                self.client = client
                self.model_name = model_name
                logger.info(f"✓ Llama 3 API client initialized for model: {model_name}")
            
            def __call__(self, prompt, max_new_tokens=200, temperature=0.2, top_p=0.9):
                """
                Generate text using Hugging Face Inference API (Chat Completion)
                Returns format compatible with transformers pipeline
                """
                try:
                    # Llama 3 uses chat completion API, not text generation
                    # We need to convert the prompt to chat format
                    
                    logger.info("📤 Converting prompt to chat format...")
                    
                    # Extract system and user messages from Llama 3 prompt format
                    if "<|start_header_id|>system<|end_header_id|>" in prompt:
                        # Parse Llama 3 formatted prompt
                        parts = prompt.split("<|start_header_id|>")
                        
                        system_message = ""
                        user_message = ""
                        
                        for part in parts:
                            if part.startswith("system<|end_header_id|>"):
                                system_message = part.split("<|end_header_id|>")[1].split("<|eot_id|>")[0].strip()
                            elif part.startswith("user<|end_header_id|>"):
                                user_message = part.split("<|end_header_id|>")[1].split("<|eot_id|>")[0].strip()
                        
                        messages = [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message}
                        ]
                        logger.info(f"✓ Parsed system message ({len(system_message)} chars)")
                        logger.info(f"✓ Parsed user message ({len(user_message)} chars)")
                    else:
                        # Fallback: treat entire prompt as user message
                        messages = [{"role": "user", "content": prompt[:1000]}]  # Limit length
                        logger.info("✓ Using fallback format (simple user message)")
                    
                    logger.info(f"📤 Calling Hugging Face API (max_tokens={max_new_tokens})...")
                    
                    # Call Hugging Face Chat Completion API with timeout
                    import time
                    start_time = time.time()
                    
                    response = self.client.chat_completion(
                        messages=messages,
                        model=self.model_name,
                        max_tokens=max_new_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        stream=False  # Disable streaming
                    )
                    
                    elapsed = time.time() - start_time
                    logger.info(f"✅ API response received in {elapsed:.2f}s")
                    
                    # Extract generated text from response
                    generated_text = response.choices[0].message.content
                    logger.info(f"✓ Generated text length: {len(generated_text)} chars")
                    
                    # Return in pipeline format: [{"generated_text": "..."}]
                    # Include full prompt + generated text for compatibility
                    full_response = prompt + generated_text
                    
                    return [{"generated_text": full_response}]
                    
                except Exception as e:
                    logger.error(f"❌ API call failed: {type(e).__name__}: {e}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    
                    # Return fallback response
                    return [{"generated_text": prompt + "\n\nИзвините, произошла ошибка при обращении к модели. Пожалуйста, попробуйте позже."}]
        
        # Create the wrapper instance
        llama = LlamaAPIWrapper(client, MODEL_NAME)
        
        logger.info("✅ Llama 3 API wrapper ready!")
        logger.info("💡 Your computer will not be loaded - all processing happens on HF servers")
        
    except Exception as e:
        logger.error(f"Failed to initialize Hugging Face API client: {e}")
        logger.warning("LLM pipeline will not be available")
        llama = None
