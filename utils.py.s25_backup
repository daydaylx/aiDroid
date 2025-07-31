#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
import time
from kivy.utils import platform

if platform == 'android':
    try:
        from jnius import autoclass, cast
        Environment = autoclass('android.os.Environment')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except ImportError:
        print("Android-specific modules not available")
        Environment = None
        PythonActivity = None
else:
    Environment = None
    PythonActivity = None

class NetworkHandler:
    def __init__(self):
        """Initialize network handler"""
        self.session = requests.Session()
        self.cache_dir = self._get_cache_dir()
        self.base_url = "https://api.example.com"  # Replace with actual API
        self.timeout = 30
        
        # Ensure cache directory exists
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_dir(self):
        """Get platform-specific cache directory"""
        try:
            if platform == 'android' and PythonActivity:
                # Android: Use app's cache directory
                activity = PythonActivity.mActivity
                cache_dir = activity.getCacheDir().getPath()
                app_cache = os.path.join(cache_dir, "aidroid")
                print(f"Android cache dir: {app_cache}")
                return app_cache
            else:
                # Desktop: Use local cache directory
                cache_dir = os.path.join(os.getcwd(), "cache")
                print(f"Desktop cache dir: {cache_dir}")
                return cache_dir
        except Exception as e:
            print(f"Error getting cache directory: {e}")
            # Fallback to current directory
            return os.path.join(os.getcwd(), "cache")

    def process_request(self, message):
        """Process a user request"""
        try:
            # Check cache first
            cached_response = self.get_cached_response(message)
            if cached_response:
                return f"[Cached] {cached_response}"
            
            # Make actual request
            response = self.make_api_request(message)
            
            # Cache the response
            self.cache_response(message, response)
            
            return response
            
        except Exception as e:
            print(f"Error processing request: {e}")
            return f"Error: {str(e)}"

    def make_api_request(self, message):
        """Make API request (mock implementation)"""
        try:
            # This is a mock implementation
            # Replace with actual API calls
            
            # Simulate API delay
            time.sleep(1)
            
            # Mock responses based on message content
            if "hello" in message.lower():
                return "Hello! How can I help you today?"
            elif "weather" in message.lower():
                return "I'm sorry, I don't have access to weather data yet."
            elif "time" in message.lower():
                return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                return f"You said: {message}. I'm still learning how to respond!"
                
        except Exception as e:
            print(f"Error making API request: {e}")
            return "Sorry, I couldn't process your request right now."

    def get_cached_response(self, message):
        """Get cached response for a message"""
        try:
            cache_file = self._get_cache_filename(message)
            
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # Check if cache is still valid (1 hour)
                cache_time = cache_data.get('timestamp', 0)
                if time.time() - cache_time < 3600:
                    return cache_data.get('response')
                    
        except Exception as e:
            print(f"Error getting cached response: {e}")
            
        return None

    def cache_response(self, message, response):
        """Cache a response"""
        try:
            cache_file = self._get_cache_filename(message)
            
            cache_data = {
                'message': message,
                'response': response,
                'timestamp': time.time()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
            print(f"Response cached to: {cache_file}")
            
        except Exception as e:
            print(f"Error caching response: {e}")

    def _get_cache_filename(self, message):
        """Generate cache filename for a message"""
        import hashlib
        
        # Create hash of message for filename
        message_hash = hashlib.md5(message.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f"cache_{message_hash}.json")

    def clear_cache(self):
        """Clear all cached responses"""
        try:
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    if filename.startswith('cache_') and filename.endswith('.json'):
                        file_path = os.path.join(self.cache_dir, filename)
                        os.remove(file_path)
                        
                print("Cache cleared successfully")
                
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def clear_old_cache(self, max_age_hours=24):
        """Clear cache files older than specified hours"""
        try:
            current_time = time.time()
            
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    if filename.startswith('cache_') and filename.endswith('.json'):
                        file_path = os.path.join(self.cache_dir, filename)
                        
                        # Check file age
                        file_age = current_time - os.path.getmtime(file_path)
                        if file_age > (max_age_hours * 3600):
                            os.remove(file_path)
                            print(f"Removed old cache file: {filename}")
                            
        except Exception as e:
            print(f"Error clearing old cache: {e}")

    def get_cache_info(self):
        """Get cache information"""
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
            
        except Exception as e:
            print(f"Error getting cache info: {e}")
            return {}

class ConfigManager:
    def __init__(self):
        """Initialize configuration manager"""
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Ensure config directory exists
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
        
        self.config = self.load_config()

    def _get_config_dir(self):
        """Get platform-specific config directory"""
        try:
            if platform == 'android' and PythonActivity:
                # Android: Use app's files directory
                activity = PythonActivity.mActivity
                files_dir = activity.getFilesDir().getPath()
                config_dir = os.path.join(files_dir, "config")
                return config_dir
            else:
                # Desktop: Use local config directory
                return os.path.join(os.getcwd(), "config")
        except Exception as e:
            print(f"Error getting config directory: {e}")
            return os.path.join(os.getcwd(), "config")

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Default configuration
                default_config = {
                    'api_url': 'https://api.example.com',
                    'timeout': 30,
                    'cache_enabled': True,
                    'cache_max_age': 24,
                    'theme': 'light'
                }
                self.save_config(default_config)
                return default_config
                
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self, config=None):
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
            print(f"Config saved to: {self.config_file}")
            
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

if __name__ == "__main__":
    # Test the utility classes
    try:
        print("Testing NetworkHandler...")
        net_handler = NetworkHandler()
        
        # Test cache info
        cache_info = net_handler.get_cache_info()
        print(f"Cache info: {cache_info}")
        
        # Test request processing
        response = net_handler.process_request("hello")
        print(f"Response: {response}")
        
        print("\nTesting ConfigManager...")
        config_manager = ConfigManager()
        
        # Test config operations
        config_manager.set('test_key', 'test_value')
        value = config_manager.get('test_key')
        print(f"Config test: {value}")
        
    except Exception as e:
        print(f"Error testing utilities: {e}")
EOF

