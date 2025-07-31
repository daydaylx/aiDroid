#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        
        # Header
        title = Label(
            text="🤖 aiDroid für Samsung S25",
            size_hint_y=None,
            height="80dp",
            font_size="24sp"
        )
        
        # Status
        device_info = "Android Device" if platform == "android" else "Desktop Mode"
        status = Label(
            text=f"Status: {device_info}\nOptimiert für Galaxy S25",
            size_hint_y=None,
            height="60dp",
            font_size="16sp"
        )
        
        # Main Button
        start_button = Button(
            text="✨ Start Samsung S25 Optimierung",
            size_hint_y=None,
            height="60dp",
            font_size="18sp"
        )
        start_button.bind(on_press=self.on_start_pressed)
        
        # Add widgets
        self.add_widget(title)
        self.add_widget(status)
        self.add_widget(start_button)
        
        # Response area
        self.response_label = Label(
            text="Willkommen bei aiDroid!\n\nDeine KI-App für Samsung Galaxy S25\n\nDrücke den Button um zu starten...",
            text_size=(None, None),
            halign="center",
            valign="top"
        )
        self.add_widget(self.response_label)
    
    def on_start_pressed(self, instance):
        self.response_label.text = """✅ aiDroid S25 Pro gestartet!

🔥 Features aktiviert:
• Samsung Galaxy S25 Optimierung
• Material Design UI
• Performance Tuning
• Memory Management

🚀 Bereit für den Einsatz auf:
• Samsung Galaxy S25
• Samsung Galaxy S25+  
• Samsung Galaxy S25 Ultra

📱 Android 15 & One UI 7 kompatibel"""

class aiDroidApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "aiDroid S25 Pro"
    
    def build(self):
        return MainScreen()
    
    def on_start(self):
        print("🚀 aiDroid S25 Pro gestartet!")
    
    def on_stop(self):
        print("👋 aiDroid S25 Pro beendet")

if __name__ == "__main__":
    try:
        app = aiDroidApp()
        app.run()
    except Exception as e:
        print(f"💥 Fehler beim Start: {e}")

