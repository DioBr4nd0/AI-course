#!/bin/bash

echo "=========================================="
echo "  Voice Agent Setup Script"
echo "=========================================="
echo ""
echo "PREREQUISITES:"
echo "You need to install the following system dependencies manually:"
echo ""
echo "  Ubuntu/Debian:"
echo "    sudo apt-get update"
echo "    sudo apt-get install -y ffmpeg libportaudio2"
echo ""
echo "  Fedora/RHEL:"
echo "    sudo dnf install -y ffmpeg portaudio-devel"
echo ""
echo "  Arch Linux:"
echo "    sudo pacman -S ffmpeg portaudio"
echo ""
echo "  macOS:"
echo "    brew install ffmpeg portaudio"
echo ""
echo "=========================================="
echo ""

read -p "Have you installed the system dependencies? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please install the dependencies first, then run this script again."
    exit 1
fi

echo "[SETUP] Creating virtual environment..."
python3 -m venv venv

echo "[SETUP] Activating virtual environment..."
source venv/bin/activate

echo "[SETUP] Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "To start the Voice Agent:"
echo "  1. Activate the venv: source venv/bin/activate"
echo "  2. Start Ollama: ollama serve &"
echo "  3. Run the agent: python main.py"
echo ""
echo "Note: Make sure Ollama is running with llama3.2 model:"
echo "  ollama pull llama3.2"
echo ""
