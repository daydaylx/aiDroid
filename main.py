#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from kivy.utils import platform

if platform == 'android':
    try:
        from android.permissions import request_permissions, Permission
        from jnius import autoclass
        Build = autoclass('android.os.Build')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except ImportError:
        request_permissions = None
        Permission = None
        Build = None
else:
    request_permissions = None
    Permission = None
    Build = None

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window

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

        if platform == 'android' and Build:
            self.detect_samsung_device()

        try:
            self.memory_db = MemoryDB()
            self.network_handler = NetworkHandler()
        except Exception as e:
            print(f"Error initializing components: {e}")
            self.memory_db = None
            self.network_handler = None

    def detect_samsung_device(self):
        try:
            manufacturer = Build.MANUFACTURER
            model = Build.MODEL
            sdk_int = Build.VERSION.SDK_INT
            print(f"Device: {manufacturer} {model}")
            print(f"Android SDK: {sdk_int}")
            if "samsung" in manufacturer.lower() and "s25" in model.lower():
                print("Samsung Galaxy S25 detected - enabling optimizations")
        except Exception as e:
            print(f"Error detecting Samsung device: {e}")

    def build_ui(self):
        layout = MDBoxLayout(orientation="vertical", padding="20dp", spacing="10dp")

        title = MDLabel(text="aiDroid for Samsung S25",
                        theme_text_color="Primary",
                        size_hint_y=None,
                        height="60dp",
                        font_style="H4",
                        halign="center")

        self.text_input = MDTextField(hint_text="Enter your message...",
                                      multiline=True,
                                      size_hint_y=None,
                                      height="120dp",
                                      helper_text="Optimized for Samsung Galaxy S25",
                                      helper_text_mode="persistent")

        send_button = MDRaisedButton(text="Send Message",
                                    size_hint_y=None,
                                    height="56dp",
                                    on_release=self.send_message)

        self.response_scroll = MDScrollView()
        self.response_label = MDLabel(text="Welcome to aiDroid on Samsung Galaxy S25!\nResponses will appear here...",
                                     theme_text_color="Secondary",
                                     text_size=(None, None),
                                     halign="left",
                                     valign="top")
        self.response_scroll.add_widget(self.response_label)

        layout.add_widget(title)
        layout.add_widget(self.text_input)
        layout.add_widget(send_button)
        layout.add_widget(self.response_scroll)

        self.add_widget(layout)

    def send_message(self, instance):
        message = self.text_input.text.strip()
        if not message:
            return

        self.text_input.text = ""
        try:
            if self.memory_db:
                self.memory_db.store_message(message)
            if self.network_handler:
                response = self.network_handler.process_request(message)
                self.update_response(f"✓ Samsung S25: {response}")
            else:
                self.update_response("Network handler not available")
        except Exception as e:
            self.update_response(f"Error: {str(e)}")

    def update_response(self, response):
        current_text = self.response_label.text
        if "Welcome to aiDroid" in current_text:
            self.response_label.text = response
        else:
            self.response_label.text = f"{current_text}\n\n{response}"
        if platform == 'android':
            self.response_label.text_size = (Window.width - 40, None)
        else:
            self.response_label.text_size = (Window.width - 40, None)

class aiDroidApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "aiDroid - Samsung S25"

    def build(self):
        if platform == 'android' and request_permissions and Permission:
            self.request_permissions()
        if platform in ['win', 'linux', 'macosx']:
            # Simuliere S25 Aspect Ratio desktopseitig
            Window.size = (400, 800)
        return MainScreen()

    def request_permissions(self):
        perms = [
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.ACCESS_WIFI_STATE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_MEDIA_AUDIO,
            Permission.READ_MEDIA_VIDEO
        ]
        try:
            request_permissions(perms)
            print("Requested Android runtime permissions")
        except Exception as e:
            print(f"Permission request error: {e}")

    def on_start(self):
        if platform == 'android' and Build:
            print(f"aiDroid started on {Build.MODEL}")
        else:
            print("aiDroid app started (non-Android)")

    def on_stop(self):
        print("aiDroid app stopped")

if __name__ == "__main__":
    try:
        app = aiDroidApp()
        app.run()
    except Exception as e:
        print(f"App start error: {e}")
        sys.exit(1)
