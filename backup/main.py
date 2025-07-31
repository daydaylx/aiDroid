#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from kivy.utils import platform

# Platform-specific imports
if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from jnius import autoclass, cast
    except ImportError:
        print("Android-specific modules not available")
        request_permissions = None
        Permission = None
else:
    request_permissions = None
    Permission = None

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Import local modules
try:
    from memory import MemoryDB
    from utils import NetworkHandler
except ImportError as e:
    print(f"Error importing local modules: {e}")
    sys.exit(1)

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.build_ui()
        
        # Initialize components
        try:
            self.memory_db = MemoryDB()
            self.network_handler = NetworkHandler()
        except Exception as e:
            print(f"Error initializing components: {e}")
            self.memory_db = None
            self.network_handler = None

    def build_ui(self):
        """Build the user interface"""
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding="20dp",
            spacing="10dp"
        )

        # Title
        title = MDLabel(
            text="aiDroid",
            theme_text_color="Primary",
            size_hint_y=None,
            height="60dp",
            font_style="H4",
            halign="center"
        )
        
        # Input field
        self.text_input = MDTextField(
            hint_text="Enter your message...",
            multiline=True,
            size_hint_y=None,
            height="100dp"
        )
        
        # Send button
        send_button = MDRaisedButton(
            text="Send",
            size_hint_y=None,
            height="50dp",
            on_release=self.send_message
        )
        
        # Response area
        self.response_scroll = MDScrollView()
        self.response_label = MDLabel(
            text="Responses will appear here...",
            theme_text_color="Secondary",
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        self.response_scroll.add_widget(self.response_label)
        
        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(send_button)
        main_layout.add_widget(self.response_scroll)
        
        self.add_widget(main_layout)

    def send_message(self, instance):
        """Handle message sending"""
        message = self.text_input.text.strip()
        if not message:
            return
            
        # Clear input
        self.text_input.text = ""
        
        # Process message
        try:
            if self.memory_db:
                self.memory_db.store_message(message)
            
            if self.network_handler:
                response = self.network_handler.process_request(message)
                self.update_response(response)
            else:
                self.update_response("Network handler not available")
                
        except Exception as e:
            self.update_response(f"Error: {str(e)}")

    def update_response(self, response):
        """Update the response display"""
        current_text = self.response_label.text
        if current_text == "Responses will appear here...":
            self.response_label.text = response
        else:
            self.response_label.text = f"{current_text}\n\n{response}"
        
        # Update text size for proper wrapping
        self.response_label.text_size = (Window.width - 40, None)

class aiDroidApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "aiDroid"
        
    def build(self):
        """Build the app"""
        # Request permissions on Android
        if platform == 'android' and request_permissions and Permission:
            self.request_android_permissions()
        
        # Set window size for desktop
        if platform in ['win', 'linux', 'macosx']:
            Window.size = (400, 600)
            
        return MainScreen()

    def request_android_permissions(self):
        """Request necessary Android permissions"""
        try:
            permissions = [
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACCESS_WIFI_STATE
            ]
            request_permissions(permissions)
            print("Android permissions requested")
        except Exception as e:
            print(f"Error requesting permissions: {e}")

    def on_start(self):
        """Called when the app starts"""
        print("aiDroid app started successfully")
        
    def on_stop(self):
        """Called when the app stops"""
        print("aiDroid app stopped")

if __name__ == "__main__":
    try:
        app = aiDroidApp()
        app.run()
    except Exception as e:
        print(f"Error starting app: {e}")
        sys.exit(1)
EOF

