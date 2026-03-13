import logging
import ollama
import queue
import time

logger = logging.getLogger(__name__)

HALLUCINATIONS = [
    "thank you for watching",
    "am i speaking",
    "speech recognition",
    "thank you for listening",
    "you are now listening",
]

class LLMHandler:
    def __init__(self, model="llama3.2:3b", system_prompt=None):
        self.model = model
        self.conversation_history = []
        
        if system_prompt is None:
            system_prompt = """You are a helpful voice AI assistant. Keep responses concise and natural, as they will be spoken aloud. 
Avoid long lists or complex formatting. Respond as if having a conversation."""
        
        self.system_prompt = system_prompt
        self._add_to_history("system", system_prompt)

    def _add_to_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        if len(self.conversation_history) > 20:
            self.conversation_history = [{"role": "system", "content": self.system_prompt}] + self.conversation_history[-19:]

    def _is_hallucination(self, text):
        text_lower = text.lower()
        return any(h in text_lower for h in HALLUCINATIONS)

    def generate(self, user_input, max_retries=3, backoff=2.0):
        logger.info(f"[Ollama] Generating response for: {user_input[:50]}...")
        
        self._add_to_history("user", user_input)
        
        for attempt in range(max_retries):
            try:
                response = ollama.chat(
                    model=self.model,
                    messages=self.conversation_history,
                    options={
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                )
                
                response_text = response['message']['content'].strip()
                
                if self._is_hallucination(response_text):
                    logger.warning("[Ollama] Filtering out hallucination")
                    response_text = "I didn't catch that. Could you repeat?"
                
                self._add_to_history("assistant", response_text)
                logger.info(f"[Ollama] Response: {response_text[:50]}...")
                return response_text
                
            except ConnectionError as e:
                logger.warning(f"[Ollama] Connection error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    wait_time = backoff * (2 ** attempt)
                    logger.info(f"[Ollama] Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error("[Ollama] Failed to connect after retries")
                    return "Sorry, I'm having trouble connecting to the AI. Please try again."
                    
            except Exception as e:
                logger.error(f"[Ollama] Unexpected error: {e}")
                return "Sorry, something went wrong. Please try again."
        
        return "Sorry, I couldn't generate a response."

    def clear_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        logger.info("[Ollama] Conversation history cleared")
