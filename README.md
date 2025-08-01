# aiDroid S25 Pro

**Die ultimative KI-Chat-App für Samsung Galaxy S25 und Android 15.**

---

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Features](#features)
- [Architektur](#architektur)
- [Kompatibilität](#kompatibilität)
- [Screenshots](#screenshots)
- [Installationsanleitung (Android)](#installationsanleitung-android)
- [Entwicklung & Tests (Linux/Desktop)](#entwicklung--tests-linuxdesktop)
- [Build und CI/CD](#build-und-cicd)
- [Fehlerbehebung & Troubleshooting](#fehlerbehebung--troubleshooting)
- [FAQ](#faq)
- [Mitwirkende & Lizenz](#mitwirkende--lizenz)

---

## Über das Projekt

**aiDroid S25 Pro** ist eine moderne, KI-basierte Messaging-App, speziell optimiert für Samsung Galaxy S25 Smartphones mit Android 15 und One UI 7. Sie bietet:
- Schnellen, asynchronen KI-Chat
- Effizientes Memory-Management & Kontext-Memory
- Material Design UI im One-UI-Stil
- Robustheit und Performance, speziell abgestimmt für High-End-Geräte

Der gesamte Build läuft vollautomatisch über GitHub Actions, installiert werden kann die App bequem per .apk.

---

## Features

- **Chat-KI** mit asynchroner Verarbeitung
- **Optimierte UI** für One UI 7 (Samsung S25)
- **Performance-Tuning** (120Hz, RAM-Effizienz, Thread-Pooling)
- **Lokale Sprach- & Systemantworten** (Offline-Basismodul)
- **Context-Memory System** (Chat-Verlauf, Speicherlimits)
- **Smart Caching** (für schnelle Wiederholungen)
- **Galaxy S25-Erkennung** und S25-spezifische Features im Interface
- **Sichere Konfiguration** (Berechtigungen, Storage, Verschlüsselung)
- **Kompatibilität zu Android 10–15**  
- **Open Source, CI/CD ready** (vollautomatischer Android-Build, Upload als Artefakt)

---

## Architektur

**Tech-Stack:**
- **Python 3.x**: Kernlogik, Kivy-App
- **Kivy / KivyMD**: UI mit Material 3/One UI Design
- **Buildozer, python-for-android**: Android-Packaging  
- **SQLite (MemoryDB)**: lokaler Kontext-Speicher
- **requests**: Netzwerk, API-Aufrufe
- **asyncio, ThreadPoolExecutor**: asynchrone Kommunikation
- **GitHub Actions**: CI/CD, Auto-Build, Testing

**Verzeichnis-Struktur:**
aiDroid/
├─ main.py # Main UI/Logik (Kivy/KivyMD)
├─ utils.py # Netzwerk, Caching, Secure Config
├─ memory.py # SQLite MemoryDB
├─ buildozer.spec # Android Build-Konfiguration
├─ requirements.txt # (optional, Desktop-Quicktest)
├─ README.md
│
├─ kv/ # Kivy UI-Dateien (optional)
│
├─ tests/ # Unit Tests, Pytest-kompatibel
├─ .github/workflows/ # CI/CD-Workflows (Build, Test)

text

---

## Kompatibilität

- **Empfohlen:**  
  - Samsung Galaxy S25, S25+, S25 Ultra (Android 15, One UI 7)
  - Andere Samsung-Modelle mit Android 13+
  - Generische Android-Geräte ab Android 10
- **Desktop/Entwicklung:**  
  - Ubuntu/Mint, Windows, macOS (Tests, nicht Production)

---

## Screenshots

> Screenshots können hier eingefügt/verlinkt werden:
>
> ![aiDroid S25 Startscreen](screenshots/start.png)
>
> ![aiDroid S25 Chat](screenshots/chat.png)

---

## Installationsanleitung (Android)

### Variante 1: Release-APK aus GitHub Actions laden

1. **Neueste APK im [Actions-Bereich](https://github.com/daydaylx/aiDroid/actions) finden**  
   (im jeweiligen Build-Job unter "Artifacts").
2. **APK aufs Gerät kopieren**  
   z.B. via USB, Cloud oder direkt herunterladen.
3. **Unbekannte Quellen in Android zulassen**  
   (Einstellungen → Sicherheit → Unbekannte Apps installieren).
4. **APK installieren**
adb install -r aiDroid-S25-APK-<version>.apk

text
5. **App starten und genießen!**

### Variante 2: Selbst bauen

**Voraussetzungen:**
- Linux (empfohlen: Ubuntu/Mint)
- Python 3.x, pip, git, Java JDK 11+
- adb (Android Debug Bridge)
- Buildozer:  
pip install buildozer

text
- Android SDK/NDK werden von Buildozer automatisch bezogen.

**Build:**
git clone https://github.com/daydaylx/aiDroid.git
cd aiDroid
buildozer android debug

text

APK findest du anschließend im `bin/` Verzeichnis.

---

## Entwicklung & Tests (Linux/Desktop)

Für schnelle UI-Entwicklung und Testing:
pip install kivy kivymd
python main.py

text
**Unit-Tests:**
pip install pytest
pytest tests/

text

---

## Build und CI/CD

**Automatisiertes Buildsystem:**
- Jeder Push auf `main` erzeugt automatisch einen frischen APK-Build via GitHub Actions.
- Fehlgeschlagene Builds erzeugen Log-Artefakte.
- Alle Assets werden im Workflow erzeugt, keine Images nötig.

**Workflow-Datei:**  
`.github/workflows/build-apk.yml`

---

## Fehlerbehebung & Troubleshooting

- **“NDK ... too old”**:  
  Kontrolliere `android.ndk = 25b` in der buildozer.spec!
- **“No APK generated”**:  
  Fehlerlogs ansehen (`.buildozer/`, im Artifact).
- **“Permission denied” beim Push?**  
  Prüfe GitHub-Berechtigungen.
- **"ImportError: kivy/KivyMD not found"**  
  Liegt meist an virtuellem Environment oder veralteten pip-Versionen.
- **App startet leer auf Android**  
  Prüfe, ob alle Assets (`icon.png`, `presplash.png`) generiert wurden.

**Tipp:**  
Fehler im Build anzeigen lassen mit:  
buildozer android debug deploy run logcat

text

---

## FAQ

**Q:** Welche Python-/NDK-/Android-Versionen sind kompatibel?  
**A:** Empfehlung: Python 3.10+, Android API 30-34, NDK mind. 25b

**Q:** Läuft das auch auf Nicht-Samsung-Geräten?  
**A:** Ja, aber ohne spezielle One UI Features

**Q:** Wie syncen sich Memory und Caching?  
**A:** SQLite speichert alle Chat-Kontexte, Caching (utils.py) hält die letzten KI-Antworten für 60 min im lokalen Cache (Dateisystem oder Android Cache-Dir).

**Q:** Wie kann man eigene KI-APIs/Keys nutzen?  
**A:** Im Source-Code (`utils.py` / SecureConfigManager) können API-URLs und Keys per Config-File abgelegt/verschlüsselt gespeichert werden.

---

## Mitwirkende & Lizenz

- **Lead Dev:** daydaylx
- **Idee, Testing:** David und Community
- **Buildozer/CI-Pipelines:** [@ArtemSBulgakov](https://github.com/ArtemSBulgakov)  
- **UI/UX-Optimierung:** KI/Manual

**Lizenz:**  
MIT License (siehe LICENSE-Datei im Repository)

---

**Feedback/Bugs:**  
Gerne als Issue in GitHub melden oder per PR beitragen!

---
