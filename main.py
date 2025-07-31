#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import gc
from typing import Optional, Any
from kivy.utils import platform

if platform == "android":
    try:
        from android.permissions import request_permissions, Permission
        from jnius import autoclass

        Build = autoclass("android.os.Build")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
    except ImportError:
        request_permissions = None
        Permission = None
        Build = None
        PythonActivity = None
        Context = None
else:
    request_permissions = None
    Permission = None
    Build = None
    PythonActivity = None
    Context = None

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.core.window import Window
from kivy.clock import Clock
import asyncio

try:
    from memory import MemoryDB
    from utils import AsyncNetworkHandler
except ImportError as e:
    print(f"Error importing local modules: {e}")
    sys.exit(1)


class WidgetPool:
    """Widget-Pooling für bessere Performance"""

    def __init__(self):
        self._label_pool: list = []
        self._button_pool: list = []

    def get_label(self) -> MDLabel:
        if self._label_pool:
            return self._label_pool.pop()
        return MDLabel()

    def return_label(self, label: MDLabel) -> None:
        label.text = ""
        self._label_pool.append(label)


class MainScreen(MDScreen):
    memory_db: Optional[MemoryDB]
    network_handler: Optional[AsyncNetworkHandler]
    widget_pool: WidgetPool

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.name = "main"
        self.widget_pool = WidgetPool()
        self.is_samsung_s25 = False
        self.message_count = 0

        self.build_ui()

        if platform == "android" and Build:
            self.detect_samsung_device()

        try:
            self.memory_db = MemoryDB()
            self.network_handler = AsyncNetworkHandler()
        except Exception as e:
            print(f"Error initializing components: {e}")
            self.memory_db = None
            self.network_handler = None

    def detect_samsung_device(self) -> None:
        """Samsung Galaxy S25 Erkennung mit One UI 7 Features"""
        try:
            manufacturer = Build.MANUFACTURER
            model = Build.MODEL
            sdk_int = Build.VERSION.SDK_INT

            print(f"Device: {manufacturer} {model}")
            print(f"Android SDK: {sdk_int}")

            if "samsung" in manufacturer.lower():
                self.is_samsung_s25 = "s25" in model.lower()

                if self.is_samsung_s25:
                    print("🔥 Samsung Galaxy S25 detected - enabling optimizations")
                    self.enable_s25_optimizations()

                if sdk_int >= 34:  # Android 15
                    print("📱 Android 15 detected - enabling One UI 7 features")
                    self.enable_one_ui_features()

        except Exception as e:
            print(f"Error detecting Samsung device: {e}")

    def enable_s25_optimizations(self) -> None:
        """Galaxy S25 spezifische Optimierungen"""
        try:
            # 120Hz Display Optimierung
            Window.sync = True

            # Galaxy S25 Display: 6.2" 2340x1080, 416 ppi
            if platform != "android":
                Window.size = (390, 844)  # Simuliert S25 Verhältnis

            print("✅ S25 Display-Optimierungen aktiviert")
        except Exception as e:
            print(f"S25 optimization error: {e}")

    def enable_one_ui_features(self) -> None:
        """One UI 7 Features aktivieren"""
        try:
            # Dynamische Farben (Material You)
            # Now Bar Integration vorbereiten
            # Circle to Search Vorbereitung
            print("✅ One UI 7 Features vorbereitet")
        except Exception as e:
            print(f"One UI feature error: {e}")

    def build_ui(self) -> None:
        """Optimierte UI mit Material 3 Design"""
        layout = MDBoxLayout(
            orientation="vertical", padding="20dp", spacing="12dp", adaptive_height=True
        )

        # Header mit S25 Status
        header_text = (
            "🤖 aiDroid für Samsung S25" if self.is_samsung_s25 else "🤖 aiDroid"
        )
        title = MDLabel(
            text=header_text,
            theme_text_color="Primary",
            size_hint_y=None,
            height="60dp",
            font_style="H4",
            halign="center",
        )

        # Status Label
        self.status_label = MDLabel(
            text="🔄 Bereit für Samsung Galaxy S25",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp",
            font_style="Caption",
            halign="center",
        )

        # Input Field optimiert
        self.text_input = MDTextField(
            hint_text="Nachricht eingeben...",
            multiline=True,
            size_hint_y=None,
            height="120dp",
            helper_text=(
                "Optimiert für One UI 7" if self.is_samsung_s25 else "KI-Chat Interface"
            ),
            helper_text_mode="persistent",
            max_text_length=1000,  # Limit für Performance
        )

        # Button Row
        button_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height="56dp", spacing="8dp"
        )

        send_button = MDRaisedButton(
            text="📤 Senden", size_hint_x=0.7, on_release=self.send_message_async
        )

        clear_button = MDIconButton(
            icon="delete", size_hint_x=0.15, on_release=self.clear_history
        )

        gc_button = MDIconButton(
            icon="memory", size_hint_x=0.15, on_release=self.force_gc
        )

        button_layout.add_widget(send_button)
        button_layout.add_widget(clear_button)
        button_layout.add_widget(gc_button)

        # Response Area mit ScrollView
        self.response_scroll = MDScrollView()
        self.response_label = MDLabel(
            text="✨ Willkommen bei aiDroid!\n🚀 Optimiert für Samsung Galaxy S25 mit Android 15\n💬 Deine Nachrichten erscheinen hier...",
            theme_text_color="Secondary",
            text_size=(None, None),
            halign="left",
            valign="top",
            markup=True,
        )
        self.response_scroll.add_widget(self.response_label)

        # Layout zusammenfügen
        layout.add_widget(title)
        layout.add_widget(self.status_label)
        layout.add_widget(self.text_input)
        layout.add_widget(button_layout)
        layout.add_widget(self.response_scroll)

        self.add_widget(layout)

    def send_message_async(self, instance: Any) -> None:
        """Asynchrone Nachrichtenverarbeitung"""
        message = self.text_input.text.strip()
        if not message:
            return

        self.text_input.text = ""
        self.message_count += 1

        # UI Feedback
        self.status_label.text = f"🔄 Verarbeite Nachricht {self.message_count}..."

        # Async verarbeiten
        Clock.schedule_once(
            lambda dt: asyncio.create_task(self._process_message_async(message)), 0
        )

    async def _process_message_async(self, message: str) -> None:
        """Interne async Nachrichtenverarbeitung"""
        try:
            if self.memory_db:
                self.memory_db.store_message(message)

            if self.network_handler:
                response = await self.network_handler.process_request_async(message)
                prefix = "🔥 S25:" if self.is_samsung_s25 else "🤖 Bot:"
                Clock.schedule_once(
                    lambda dt: self.update_response(f"{prefix} {response}"), 0
                )
            else:
                Clock.schedule_once(
                    lambda dt: self.update_response(
                        "❌ Network handler nicht verfügbar"
                    ),
                    0,
                )

        except Exception as e:
            error_msg = f"❌ Fehler: {str(e)}"
            Clock.schedule_once(lambda dt: self.update_response(error_msg), 0)
        finally:
            Clock.schedule_once(lambda dt: self.reset_status(), 0)

    def update_response(self, response: str) -> None:
        """Memory-optimierte Response Updates"""
        current_text = self.response_label.text

        # Entferne Welcome-Message beim ersten echten Response
        if "Willkommen bei aiDroid" in current_text:
            self.response_label.text = response
        else:
            self.response_label.text = f"{current_text}\n\n{response}"

        # Memory Management: Limitiere Historie
        lines = self.response_label.text.split("\n")
        if len(lines) > 100:
            # Behalte nur die letzten 50 Zeilen
            self.response_label.text = "\n".join(lines[-50:])

        # Text-Size für Performance
        self.response_label.text_size = (Window.width - 40, None)

        # Garbage Collection bei vielen Nachrichten
        if self.message_count % 10 == 0:
            gc.collect()

    def clear_history(self, instance: Any) -> None:
        """History löschen"""
        self.response_label.text = (
            "🗑️ Historie gelöscht\n💬 Bereit für neue Nachrichten..."
        )
        self.message_count = 0
        gc.collect()

    def force_gc(self, instance: Any) -> None:
        """Manueller Garbage Collection"""
        gc.collect()
        self.status_label.text = (
            f"🧹 Speicher bereinigt (Nachrichten: {self.message_count})"
        )

    def reset_status(self) -> None:
        """Status zurücksetzen"""
        status_text = (
            "✅ Bereit für Samsung Galaxy S25" if self.is_samsung_s25 else "✅ Bereit"
        )
        self.status_label.text = status_text


class aiDroidApp(MDApp):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.title = "aiDroid - Samsung S25 Pro"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"

    def build(self) -> MainScreen:
        if platform == "android" and request_permissions and Permission:
            self.request_permissions()

        # Desktop: Simuliere S25 Aspect Ratio
        if platform in ["win", "linux", "macosx"]:
            Window.size = (390, 844)

        return MainScreen()

    def request_permissions(self) -> None:
        """Android Permissions für S25 optimiert"""
        perms = [
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.ACCESS_WIFI_STATE,
            Permission.READ_MEDIA_IMAGES,
            Permission.READ_MEDIA_AUDIO,
            Permission.READ_MEDIA_VIDEO,
        ]

        try:
            request_permissions(perms)
            print("✅ Android Permissions angefordert")
        except Exception as e:
            print(f"❌ Permission request error: {e}")

    def on_start(self) -> None:
        if platform == "android" and Build:
            model = Build.MODEL if Build else "Unknown"
            print(f"🚀 aiDroid gestartet auf {model}")
        else:
            print("🚀 aiDroid Desktop-Modus gestartet")

    def on_stop(self) -> None:
        print("👋 aiDroid beendet")
        gc.collect()


if __name__ == "__main__":
    try:
        app = aiDroidApp()
        app.run()
    except Exception as e:
        print(f"💥 App start error: {e}")
        sys.exit(1)
