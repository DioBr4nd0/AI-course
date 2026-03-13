# Voice Agent

A 100% local, real-time voice-to-voice AI assistant built in Python.

## Features

- **Voice Activity Detection (VAD)** - Automatically detects when you start/stop speaking
- **Speech-to-Text** - Uses Faster-Whisper for local transcription
- **LLM Inference** - Uses Ollama with llama3.2 for local AI responses
- **Text-to-Speech** - Uses Edge-TTS for natural speech output
- **Fault Tolerance** - Self-healing audio devices and Ollama connections
- **Conversation History** - Maintains context across interactions

## Prerequisites

### System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg libportaudio2

# Fedora/RHEL
sudo dnf install -y ffmpeg portaudio-devel

# Arch Linux
sudo pacman -S ffmpeg portaudio

# macOS
brew install ffmpeg portaudio
```

### Ollama

1. Install Ollama: https://github.com/ollama/ollama
2. Pull the llama3.2 model:
```bash
ollama pull llama3.2
```

## Installation

```bash
# Run setup script
bash setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Start Ollama (in another terminal or background)
ollama serve &

# Run the voice agent
python main.py
```

## Project Structure

```
voice-agent/
├── audio_manager.py    # Audio capture, VAD, TTS playback
├── speech_to_text.py  # Faster-Whisper transcription
├── llm_handler.py     # Ollama LLM integration
├── main.py            # Main orchestrator loop
├── requirements.txt   # Python dependencies
└── setup.sh          # Setup script
```

## Controls

- Simply speak naturally - the system detects speech automatically
- Press Ctrl+C to stop the agent

## Troubleshooting

**PortAudio not found**
- Install libportaudio2 (see system dependencies above)

**Ollama connection errors**
- Make sure Ollama is running: `ollama serve`
- Check the model is installed: `ollama list`

**Audio device errors**
- Check your microphone is connected and working
- Try restarting the audio service
