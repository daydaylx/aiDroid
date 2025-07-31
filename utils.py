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
        self.base_url = "https://api.example.com"
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
            cached = self.get_cached_response(message)
            if cached:
                return f"[Cached] {cached}"
            response = self.make_api_request(message)
            self.cache_response(message, response)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def make_api_request(self, message):
        try:
            time.sleep(1)
            low = message.lower()
            if "hello" in low:
                return "Hello! How can I help you today?"
            elif "samsung" in low:
                return "Du nutzt ein Galaxy S25 – geiles Gerät!"
            elif "time" in low:
                return f"Aktuelle Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                return f"Du hast gesagt: {message}. Ich lerne noch."
        except Exception:
            return "API Anfrage nicht möglich."

    def get_cached_response(self, message):
        try:
            fname = self._get_cache_filename(message)
            if os.path.exists(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if time.time() - data.get('timestamp', 0) < 3600:
                    return data.get('response')
        except Exception:
            pass
        return None

    def cache_response(self, message, response):
        try:
            fname = self._get_cache_filename(message)
            data = {
                'message': message,
                'response': response,
                'timestamp': time.time()
            }
            with open(fname, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_cache_filename(self, message):
        import hashlib
        md5hash = hashlib.md5(message.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f"cache_{md5hash}.json")

    def clear_cache(self):
        try:
            if os.path.exists(self.cache_dir):
                for fn in os.listdir(self.cache_dir):
                    if fn.startswith("cache_") and fn.endswith(".json"):
                        os.remove(os.path.join(self.cache_dir, fn))
        except Exception:
            pass

    def get_cache_info(self):
        try:
            if not os.path.exists(self.cache_dir):
                return {'cache_dir': self.cache_dir, 'file_count': 0, 'total_size': 0}
            count = 0
            size = 0
            for fn in os.listdir(self.cache_dir):
                if fn.startswith("cache_") and fn.endswith(".json"):
                    path = os.path.join(self.cache_dir, fn)
                    count += 1
                    size += os.path.getsize(path)
            return {'cache_dir': self.cache_dir, 'file_count': count, 'total_size': size, 'size_mb': round(size/(1024*1024),2)}
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
                return os.path.join(files_dir, "config")
            else:
                return os.path.join(os.getcwd(), "config")
        except Exception:
            return os.path.join(os.getcwd(), "config")

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            default = {
                'api_url': 'https://api.example.com',
                'timeout': 30,
                'cache_enabled': True,
                'cache_max_age': 24,
                'theme': 'light'
            }
            self.save_config(default)
            return default
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
    nh = NetworkHandler()
    print(nh.process_request("Hallo Samsung S25!"))
    print(nh.get_cache_info())
    cm = ConfigManager()
    cm.set('test_key', 'alles klar')
    print(cm.get('test_key'))
