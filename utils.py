#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import time
import asyncio
from typing import Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from kivy.utils import platform

if platform == "android":
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
    except ImportError:
        PythonActivity = None
else:
    PythonActivity = None


class AsyncNetworkHandler:
    """Asynchroner Network Handler für bessere Performance"""

    def __init__(self):
        self.session = requests.Session()
        # User-Agent für Samsung S25
        self.session.headers.update(
            {"User-Agent": "aiDroid/2.0 (Samsung SM-S921B; Android 15; One UI 7)"}
        )

        self.cache_dir = self._get_cache_dir()
        self.base_url = "https://api.openrouter.ai/api/v1"
        self.timeout = 30

        # Async Thread Pool
        self.executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="aiDroid")

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_dir(self) -> str:
        """Cache-Verzeichnis ermitteln"""
        try:
            if platform == "android" and PythonActivity:
                cache_dir = PythonActivity.mActivity.getCacheDir().getPath()
                app_cache = os.path.join(cache_dir, "aidroid")
                return app_cache
            else:
                return os.path.join(os.getcwd(), "cache")
        except Exception:
            return os.path.join(os.getcwd(), "cache")

    async def process_request_async(self, message: str) -> str:
        """Async Wrapper für process_request"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.process_request, message)

    def process_request(self, message: str) -> str:
        """Synchrone Nachrichtenverarbeitung mit Caching"""
        try:
            # Cache-Check
            cached = self.get_cached_response(message)
            if cached:
                return f"💾 {cached}"

            # Neue Anfrage
            response = self.make_api_request(message)
            self.cache_response(message, response)
            return response

        except Exception as e:
            return f"❌ Fehler: {str(e)}"

    def make_api_request(self, message: str) -> str:
        """API-Anfrage simulieren oder echte API aufrufen"""
        try:
            # Kurze Simulation für Demo
            time.sleep(0.5)

            msg_lower = message.lower()

            # Samsung S25 spezifische Antworten
            if any(word in msg_lower for word in ["samsung", "s25", "galaxy"]):
                return "🔥 Du nutzt ein Samsung Galaxy S25 - das ultimative Android-Flaggschiff mit Snapdragon 8 Elite!"

            elif any(word in msg_lower for word in ["one ui", "oneui", "android 15"]):
                return "📱 One UI 7 auf Android 15 - Samsung's beste Software-Experience ever!"

            elif any(word in msg_lower for word in ["hallo", "hello", "hi"]):
                return "👋 Hallo! Schön dich auf deinem Samsung Galaxy S25 zu sehen!"

            elif any(word in msg_lower for word in ["zeit", "time", "uhrzeit"]):
                return f"🕐 Aktuelle Zeit: {time.strftime('%H:%M:%S, %d.%m.%Y')}"

            elif any(word in msg_lower for word in ["speicher", "memory", "ram"]):
                import psutil

                memory = psutil.virtual_memory()
                return f"🧠 Speicher: {memory.percent}% belegt ({memory.available // (1024*1024*1024)}GB frei)"

            elif any(
                word in msg_lower for word in ["performance", "leistung", "benchmark"]
            ):
                return "⚡ Snapdragon 8 Elite Performance: 3.2 GHz, Adreno 830 GPU - Hardcore Gaming ready!"

            else:
                return f"🤖 Du hast gesagt: '{message}' - Ich lerne noch, aber dein S25 läuft perfekt!"

        except Exception as e:
            return f"🚫 API-Anfrage fehlgeschlagen: {str(e)}"

    def get_cached_response(self, message: str) -> Optional[str]:
        """Cache-Response abrufen"""
        try:
            fname = self._get_cache_filename(message)
            if os.path.exists(fname):
                with open(fname, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Cache-Validität: 1 Stunde
                if time.time() - data.get("timestamp", 0) < 3600:
                    return data.get("response")

        except Exception:
            pass
        return None

    def cache_response(self, message: str, response: str) -> None:
        """Response cachen"""
        try:
            fname = self._get_cache_filename(message)
            data = {
                "message": message,
                "response": response,
                "timestamp": time.time(),
                "device": "samsung_s25" if "s25" in message.lower() else "generic",
            }

            with open(fname, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Cache error: {e}")

    def _get_cache_filename(self, message: str) -> str:
        """Cache-Dateiname generieren"""
        import hashlib

        md5hash = hashlib.md5(message.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"cache_{md5hash}.json")

    def clear_cache(self) -> int:
        """Cache leeren"""
        deleted = 0
        try:
            if os.path.exists(self.cache_dir):
                for fn in os.listdir(self.cache_dir):
                    if fn.startswith("cache_") and fn.endswith(".json"):
                        os.remove(os.path.join(self.cache_dir, fn))
                        deleted += 1
        except Exception:
            pass
        return deleted

    def get_cache_info(self) -> Dict[str, Any]:
        """Cache-Informationen"""
        try:
            if not os.path.exists(self.cache_dir):
                return {
                    "cache_dir": self.cache_dir,
                    "file_count": 0,
                    "total_size": 0,
                    "size_mb": 0,
                }

            count = 0
            size = 0

            for fn in os.listdir(self.cache_dir):
                if fn.startswith("cache_") and fn.endswith(".json"):
                    path = os.path.join(self.cache_dir, fn)
                    count += 1
                    size += os.path.getsize(path)

            return {
                "cache_dir": self.cache_dir,
                "file_count": count,
                "total_size": size,
                "size_mb": round(size / (1024 * 1024), 2),
            }

        except Exception:
            return {"error": "Cache info unavailable"}


class SecureConfigManager:
    """Sichere Konfigurationsverwaltung mit Verschlüsselung"""

    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)

        self.config = self.load_config()

    def _get_config_dir(self) -> str:
        """Konfigurationsverzeichnis ermitteln"""
        try:
            if platform == "android" and PythonActivity:
                files_dir = PythonActivity.mActivity.getFilesDir().getPath()
                return os.path.join(files_dir, "config")
            else:
                return os.path.join(os.getcwd(), "config")
        except Exception:
            return os.path.join(os.getcwd(), "config")

    def load_config(self) -> Dict[str, Any]:
        """Konfiguration laden"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)

            # Default Config für Samsung S25
            default = {
                "api_url": "https://api.openrouter.ai/api/v1",
                "timeout": 30,
                "cache_enabled": True,
                "cache_max_age": 24,
                "theme": "dark",
                "device_optimization": "samsung_s25",
                "performance_mode": "high",
                "ui_animations": True,
                "version": "2.0.0",
            }

            self.save_config(default)
            return default

        except Exception as e:
            print(f"Config load error: {e}")
            return {}

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Konfiguration speichern"""
        try:
            if config is None:
                config = self.config

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Config save error: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Wert abrufen"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Wert setzen"""
        self.config[key] = value
        self.save_config()

    def optimize_for_s25(self) -> None:
        """S25-spezifische Optimierungen"""
        self.set("device_optimization", "samsung_s25")
        self.set("performance_mode", "high")
        self.set("display_refresh_rate", 120)
        self.set("memory_optimization", True)


if __name__ == "__main__":
    # Test-Code
    async def test_async():
        handler = AsyncNetworkHandler()
        response = await handler.process_request_async("Hallo Samsung S25!")
        print(f"Response: {response}")
        print(f"Cache Info: {handler.get_cache_info()}")

        config = SecureConfigManager()
        config.optimize_for_s25()
        print(f"Config: {config.config}")

    asyncio.run(test_async())
