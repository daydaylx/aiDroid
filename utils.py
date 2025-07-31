#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import time
from kivy.utils import platform

if platform == 'android':
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except ImportError:
        PythonActivity = None
else:
    PythonActivity = None

class NetworkHandler:
    def __init__(self):
        self.session = requests.Session()
        self.cache_dir = self._get_cache_dir()
        self.base_url = "https://api.example.com"  # Platzhalter-URL
        self.timeout = 30
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_dir(self):
        try:
            if platform == 'android' and PythonActivity:
                cache_dir = PythonActivity.mActivity.getCacheDir().getPath()
                app_cache = os.path.join(cache_dir, "aidroid")
                return app_cache
            else:
                return os.path.join(os.getcwd(), "cache")
        except Exception:
            return os.path.join(os.getcwd(), "cache")

    def process_request(self, message):
        try:
            cached_response = self.get_cached_response(message)
            if cached_response:
                return f"[Cached] {cached_response}"
            response = self.make_api_request(message)
            self.cache_response(message, response)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def make_api_request(self, message):
        try:
            time.sleep(1)
            if "hello" in message.lower():
                return "Hello! How can I help you today?"
            elif "samsung" in message.lower():
                return "Du nutzt offenbar ein Galaxy S25 – geiles Gerät!"
            elif "time" in message.lower():
                return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                return f"Du hast gesagt: {message}. Ich bin noch am Lernen."
        except Exception as e:
            return "Sorry, ich konnte deine Anfrage nicht bearbeiten."

    def get_cached_response(self, message):
        try:
            cache_file = self._get_cache_filename(message)
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                if time.time() - cache_data.get('timestamp', 0) < 3600:
                    return cache_data.get('response')
        except Exception:
            pass
        return None

    def cache_response(self, message, response):
        try:
            cache_file = self._get_cache_filename(message)
            cache_data = {
                'message': message,
                'response': response,
                'timestamp': time.time()
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_cache_filename(self, message):
        import hashlib
        message_hash = hashlib.md5(message.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f"cache_{message_hash}.json")

    def clear_cache(self):
        try:
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    if filename.startswith('cache_') and filename.endswith('.json'):
                        os.remove(os.path.join(self.cache_dir, filename))
        except Exception:
            pass

    def get_cache_info(self):
        try:
            if not os.path.exists(self.cache_dir):
                return {'cache_dir': self.cache_dir, 'file_count': 0, 'total_size': 0}
            file_count = 0
            total_size = 0
            for filename in os.listdir(self.cache_dir):
                if filename.startswith('cache_') and filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    file_count += 1
                    total_size += os.path.getsize(file_path)
            return {
                'cache_dir': self.cache_dir,
                'file_count': file_count,
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
        except Exception:
            return {}

class ConfigManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        self.config = self.load_config()

    def _get_config_dir(self):
        try:
            if platform == 'android' and PythonActivity:
                files_dir = PythonActivity.mActivity.getFilesDir().getPath()
                config_dir = os.path.join(files_dir, "config")
                return config_dir
            else:
                return os.path.join(os.getcwd(), "config")
        except Exception:
            return os.path.join(os.getcwd(), "config")

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                default_config = {
                    'api_url': 'https://api.example.com',
                    'timeout': 30,
                    'cache_enabled': True,
                    'cache_max_age': 24,
                    'theme': 'light'
                }
                self.save_config(default_config)
                return default_config
        except Exception:
            return {}

    def save_config(self, config=None):
        try:
            if config is None:
                config = self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

if __name__ == "__main__":
    net_handler = NetworkHandler()
    response = net_handler.process_request("Hallo Samsung S25!")
    print(f"Response: {response}")
    print(net_handler.get_cache_info())
    config_manager = ConfigManager()
    config_manager.set('test_key', 's25 success')
    print(config_manager.get('test_key'))
