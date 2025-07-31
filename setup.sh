#!/bin/bash
set -e

echo "🔧 aiDroid S25 - Erweiterte Setup-Umgebung"
echo "============================================="

# System packages für Ubuntu/Mint
echo "📦 Installiere System-Abhängigkeiten..."
sudo apt update
sudo apt install -y \
    python3.11 python3.11-venv python3.11-dev \
    build-essential ccache git unzip zip \
    openjdk-17-jdk \
    libffi-dev libssl-dev libsqlite3-dev \
    zlib1g-dev libjpeg-dev libpng-dev \
    adb fastboot \
    sqlite3

# Python Virtual Environment
echo "🐍 Erstelle Python 3.11 Virtual Environment..."
python3.11 -m venv venv
source venv/bin/activate

# Python Packages installieren
echo "📚 Installiere Python-Pakete..."
pip install --upgrade pip setuptools wheel
pip install -r requirements-dev.txt

# Pre-commit hooks installieren
echo "🔗 Installiere Pre-commit Hooks..."
pre-commit install

# Buildozer initialisieren
echo "🔨 Buildozer Setup..."
buildozer init || echo "Buildozer bereits initialisiert"

# Berechtigungen für ADB
echo "📱 ADB-Berechtigungen konfigurieren..."
sudo usermod -a -G plugdev $USER

echo ""
echo "✅ Setup komplett!"
echo ""
echo "🚀 Nächste Schritte:"
echo "1. source venv/bin/activate"
echo "2. python main.py                    # Desktop-Test"
echo "3. buildozer android debug          # APK bauen"
echo "4. adb install bin/*.apk            # Auf S25 installieren"
echo ""
echo "🔧 Development:"
echo "• ruff check .                       # Code linting"
echo "• black .                           # Code formatting"  
echo "• pytest                           # Tests ausführen"
echo "• pre-commit run --all-files       # Alle Hooks"
