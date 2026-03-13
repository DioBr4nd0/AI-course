import logging
import queue
import threading
import numpy as np
import sounddevice as sd
import asyncio
import edge_tts
import pygame
import io

logger = logging.getLogger(__name__)

class AudioManager:
    def __init__(self, sample_rate=16000, frame_duration=30, channels=1):
        self.sample_rate = sample_rate
        self.frame_duration = frame_duration
        self.channels = channels
        self.frame_size = int(sample_rate * frame_duration / 1000)
        
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.stream = None
        
        self.speaking = False
        self.silence_threshold = 15
        self.silence_frames = 0
        self.max_silence_frames = 30
        
        pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=512)

    def start_listening(self):
        self.is_listening = True
        self._start_capture()
        logger.info("[VAD] Listening for speech...")

    def _start_capture(self):
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"[VAD] Audio callback status: {status}")
            
            audio_data = indata[:, 0]
            self.audio_queue.put(audio_data.tobytes())

        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='float32',
                blocksize=self.frame_size,
                callback=audio_callback
            )
            self.stream.start()
        except Exception as e:
            logger.error(f"[VAD] Failed to start audio stream: {e}")
            self._restart_stream()

    def _restart_stream(self):
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            self.stream = None
            self._start_capture()
            logger.info("[VAD] Audio stream restarted")
        except Exception as e:
            logger.error(f"[VAD] Failed to restart stream: {e}")

    def get_audio_chunk(self, timeout=0.1):
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop_listening(self):
        self.is_listening = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    async def speak_async(self, text):
        self.speaking = True
        logger.info(f"[TTS] Generating speech for: {text[:50]}...")
        
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        audio_buffer = io.BytesIO()
        
        try:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
            
            audio_buffer.seek(0)
            
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            logger.error(f"[TTS] Error playing audio: {e}")
        finally:
            self.speaking = False
            logger.info("[TTS] Speech finished")

    def speak(self, text):
        asyncio.run(self.speak_async(text))

    def record_audio(self, max_duration=10):
        frames = []
        silent_frames = 0
        speaking_detected = False
        
        logger.info("[VAD] Recording audio...")
        
        while self.is_listening:
            chunk = self.get_audio_chunk()
            if chunk is None:
                continue
            
            audio_data = np.frombuffer(chunk, dtype=np.float32)
            rms = np.sqrt(np.mean(audio_data ** 2))
            
            is_speech = rms > 0.01
            
            if is_speech:
                speaking_detected = True
                silent_frames = 0
                frames.append(chunk)
            elif speaking_detected:
                silent_frames += 1
                if silent_frames < self.silence_threshold:
                    frames.append(chunk)
                else:
                    break
            
            if len(frames) * self.frame_size / self.sample_rate > max_duration:
                break
        
        if not frames:
            return None
        
        audio_bytes = b''.join(frames)
        return np.frombuffer(audio_bytes, dtype=np.float32)
