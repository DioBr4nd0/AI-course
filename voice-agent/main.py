import logging
import threading
import queue
import time
import numpy as np

from audio_manager import AudioManager
from speech_to_text import SpeechToText
from llm_handler import LLMHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VoiceAgent:
    def __init__(self):
        logger.info("[INIT] Initializing Voice Agent...")
        
        self.audio_manager = AudioManager(sample_rate=16000)
        self.stt = SpeechToText(model_size="base")
        self.llm = LLMHandler(model="llama3.2")
        
        self.audio_queue = queue.Queue()
        self.running = False
        
        self.listen_thread = None
        self.processing = False
        
        logger.info("[INIT] Voice Agent ready")

    def _listen_loop(self):
        logger.info("[LISTEN] Listen thread started")
        
        while self.running:
            try:
                audio_data = self.audio_manager.record_audio(max_duration=10)
                
                if audio_data is not None and len(audio_data) > 0:
                    self.audio_queue.put(audio_data)
                    logger.info(f"[LISTEN] Audio captured ({len(audio_data)/16000:.2f}s)")
                    
            except Exception as e:
                logger.error(f"[LISTEN] Error in listen loop: {e}")
                time.sleep(1)

    def _process_loop(self):
        logger.info("[PROCESS] Process thread started")
        
        while self.running:
            try:
                audio_data = self.audio_queue.get(timeout=1)
                
                if self.processing:
                    continue
                
                self.processing = True
                
                logger.info("[STT] Transcribing...")
                text = self.stt.transcribe(audio_data)
                
                if text and len(text) > 2:
                    logger.info(f"[USER] {text}")
                    
                    logger.info("[OLLAMA] Generating response...")
                    response = self.llm.generate(text)
                    
                    logger.info(f"[ASSISTANT] {response}")
                    
                    logger.info("[TTS] Speaking response...")
                    self.audio_manager.speak(response)
                else:
                    logger.info("[STT] No speech detected")
                
                self.processing = False
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"[PROCESS] Error: {e}")
                self.processing = False
                time.sleep(0.5)

    def start(self):
        logger.info("[START] Starting Voice Agent...")
        
        self.running = True
        
        self.audio_manager.start_listening()
        
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        
        self.listen_thread.start()
        self.process_thread.start()
        
        logger.info("[START] Voice Agent is running!")
        logger.info("[START] Say something to begin...")

    def stop(self):
        logger.info("[STOP] Stopping Voice Agent...")
        self.running = False
        self.audio_manager.stop_listening()
        
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        if self.process_thread:
            self.process_thread.join(timeout=2)
        
        logger.info("[STOP] Voice Agent stopped")

    def run_forever(self):
        try:
            self.start()
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("[MAIN] Interrupted by user")
        finally:
            self.stop()

if __name__ == "__main__":
    agent = VoiceAgent()
    agent.run_forever()
