#!/bin/bash
set -e

echo "🔧 OpenRouter CodeGen - System Setup"
echo "====================================="

# System packages
echo "📦 Installiere System-Abhängigkeiten..."
sudo apt update
sudo apt install -y \
    python3.11 python3.11-venv python3.11-dev \
    build-essential ccache git unzip zip \
    openjdk-17-jdk \
    libffi-dev libssl-dev libsqlite3-dev \
    zlib1g-dev libjpeg-dev libpng-dev \
    adb

# Python venv mit 3.11
echo "🐍 Erstelle Python 3.11 venv..."
python3.11 -m venv buildozer-venv
source buildozer-venv/bin/activate

# Python packages
echo "📚 Installiere Python-Pakete..."
pip install --upgrade pip setuptools==65.5.1 wheel
pip install buildozer cython requests kivy

echo "✅ Setup komplett!"
echo ""
echo "Nächste Schritte:"
echo "1. source buildozer-venv/bin/activate"
echo "2. Deine OpenRouter API Key in apikey.txt speichern"
echo "3. python3 main.py (Desktop-Test)"
echo "4. buildozer android debug (APK bauen)"
