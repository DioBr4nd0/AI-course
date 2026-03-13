import logging
import numpy as np
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, model_size="base", device="cpu"):
        logger.info(f"[STT] Loading Whisper model: {model_size}...")
        
        compute_type = "float16" if device == "cuda" else "int8"
        
        try:
            self.model = WhisperModel(
                model_size,
                device=device,
                compute_type=compute_type
            )
            logger.info("[STT] Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"[STT] Failed to load model: {e}")
            raise

    def transcribe(self, audio_data, language="en"):
        if audio_data is None or len(audio_data) == 0:
            return None
        
        try:
            segments, info = self.model.transcribe(
                audio_data,
                language=language,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            text_segments = []
            for segment in segments:
                text_segments.append(segment.text)
            
            if not text_segments:
                return None
            
            full_text = " ".join(text_segments).strip()
            
            if full_text:
                logger.info(f"[STT] Transcribed: {full_text}")
                return full_text
                
        except Exception as e:
            logger.error(f"[STT] Transcription error: {e}")
        
        return None
