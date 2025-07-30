import os
import sys
import threading
from pathlib import Path

os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.logger import Logger
from kivy.clock import Clock
from utils import fetch_models, generate_code_stream_with_memory, generate_code, clear_cache
from memory import memory

Window.size = (420, 750)
Window.clearcolor = (0.08, 0.08, 0.12, 1)

class CodeGenApp(App):
    api_key = StringProperty("")
    system_prompt = StringProperty("Du bist ein erfahrener Python-Entwickler. Schreibe sauberen, gut dokumentierten Code mit Fehlerbehandlung.")
    user_prompt = StringProperty("")
    output_text = StringProperty("Hier erscheint der generierte Code...\n\n💡 Tipp: Gib zuerst deinen OpenRouter API Key ein und lade die verfügbaren Modelle.")
    models = ListProperty([])
    selected_model = StringProperty("")
    is_loading = BooleanProperty(False)
    is_streaming = BooleanProperty(False)
    status_text = StringProperty("Bereit")
    streaming_enabled = BooleanProperty(True)
    memory_enabled = BooleanProperty(True)
    project_context = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stop_event = threading.Event()
        self.current_thread = None

    def build(self):
        self.title = "🤖 OpenRouter CodeGen Pro"
        return Builder.load_file("kv/main.kv")

    def on_start(self):
        self.load_cached_api_key()
        if self.api_key:
            Clock.schedule_once(lambda dt: self.load_models_async(), 1.0)

    def load_cached_api_key(self):
        try:
            cache_file = Path.home() / ".cache" / "openrouter" / "api_key.txt"
            if cache_file.exists():
                self.api_key = cache_file.read_text().strip()
        except Exception: pass

    def save_api_key(self):
        try:
            cache_dir = Path.home() / ".cache" / "openrouter"
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file = cache_dir / "api_key.txt"
            cache_file.write_text(self.api_key)
        except Exception: pass

    def load_models_async(self):
        if not self.api_key.strip():
            self.show_popup("❌ Fehler", "Bitte zuerst einen gültigen OpenRouter API Key eingeben!")
            return
        if self.is_loading:
            return
        self.is_loading = True
        self.status_text = "Lade Modelle..."
        self.save_api_key()
        def load_task():
            try:
                models = fetch_models(self.api_key)
                Clock.schedule_once(lambda dt: self._update_models(models), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self._handle_model_error(str(e)), 0)
        thread = threading.Thread(target=load_task, daemon=True)
        thread.start()

    def _update_models(self, models):
        self.models = models
        self.is_loading = False
        self.status_text = f"✅ {len(models)} Modelle geladen"
        if models and not self.selected_model:
            self.selected_model = models[0]
        self.show_popup("✅ Erfolg", f"{len(models)} Modelle erfolgreich geladen!\n\nTop-Modell: {models[0] if models else 'Keine'}")

    def _handle_model_error(self, error_msg):
        self.is_loading = False
        self.status_text = "❌ Fehler beim Laden"
        self.show_popup("❌ API Fehler", f"Modelle konnten nicht geladen werden:\n\n{error_msg}\n\nPrüfe deinen API Key und Internetverbindung.")

    def toggle_streaming(self):
        self.streaming_enabled = not self.streaming_enabled
        self.status_text = f"Modus: {'Streaming' if self.streaming_enabled else 'Normal'}"
        Clock.schedule_once(lambda dt: setattr(self, 'status_text', 'Bereit'), 2.0)

    def toggle_memory(self):
        self.memory_enabled = not self.memory_enabled
        self.status_text = f"🧠 {'Memory AN' if self.memory_enabled else 'Memory AUS'}"
        Clock.schedule_once(lambda dt: setattr(self, 'status_text', 'Bereit'), 2.0)

    def generate_async(self):
        if not self.api_key.strip():
            self.show_popup("❌ Fehler", "API Key fehlt!")
            return
        if not self.user_prompt.strip():
            self.show_popup("❌ Fehler", "Bitte einen Prompt eingeben!")
            return
        if not self.selected_model:
            self.show_popup("❌ Fehler", "Bitte ein Modell auswählen!")
            return
        if self.is_loading or self.is_streaming:
            return
        self.stop_generation()
        self.is_loading = True
        self.is_streaming = self.streaming_enabled
        self.stop_event.clear()

        if self.streaming_enabled:
            self.status_text = "🔄 Streaming..." + (" + 🧠 Memory" if self.memory_enabled else "")
            self.output_text = "🔄 Streaming startet...\n\n"
            def stream_task():
                try:
                    def stream_callback(chunk):
                        Clock.schedule_once(lambda dt: self._append_stream_chunk(chunk), 0)
                    result = generate_code_stream_with_memory(
                        self.api_key,
                        self.selected_model,
                        self.system_prompt,
                        self.user_prompt,
                        stream_callback,
                        self.stop_event,
                        use_context=self.memory_enabled,
                        project_context=self.project_context,
                        save_to_memory=self.memory_enabled
                    )
                    Clock.schedule_once(lambda dt: self._finish_stream_generation(result), 0)
                except Exception as e:
                    Clock.schedule_once(lambda dt: self._handle_generate_error(str(e)), 0)
            self.current_thread = threading.Thread(target=stream_task, daemon=True)
            self.current_thread.start()
        else:
            self.status_text = "Generiere Code..." + (" + 🧠 Memory" if self.memory_enabled else "")
            self.output_text = "⏳ Generiere Code...\n\nBitte warten, das kann bis zu 30 Sekunden dauern."
            def generate_task():
                try:
                    result = generate_code(
                        self.api_key,
                        self.selected_model,
                        self.system_prompt,
                        self.user_prompt
                    )
                    Clock.schedule_once(lambda dt: self._update_output(result), 0)
                except Exception as e:
                    Clock.schedule_once(lambda dt: self._handle_generate_error(str(e)), 0)
            self.current_thread = threading.Thread(target=generate_task, daemon=True)
            self.current_thread.start()

    def _append_stream_chunk(self, chunk):
        if self.output_text.startswith("🔄 Streaming startet..."):
            self.output_text = chunk
        else:
            self.output_text += chunk

    def _finish_stream_generation(self, full_result):
        self.is_loading = False
        self.is_streaming = False
        self.status_text = "✅ Streaming abgeschlossen" + (" + 🧠 Memory" if self.memory_enabled else "")

    def _update_output(self, result):
        self.output_text = result
        self.is_loading = False
        self.status_text = "✅ Code generiert" + (" + 🧠 Memory" if self.memory_enabled else "")

    def _handle_generate_error(self, error_msg):
        self.output_text = f"❌ Fehler bei der Code-Generierung:\n\n{error_msg}\n\nVersuche es mit einem anderen Modell oder vereinfache deinen Prompt."
        self.is_loading = False
        self.is_streaming = False
        self.status_text = "❌ Generierung fehlgeschlagen"

    def stop_generation(self):
        if self.stop_event:
            self.stop_event.set()
        self.is_loading = False
        self.is_streaming = False
        self.status_text = "⏹️ Generation gestoppt"

    def show_memory_history(self):
        conversations = memory.get_recent_conversations(limit=5)
        if not conversations:
            self.show_popup("🧠 Memory", "Noch keine Konversationen gespeichert.")
            return
        history_text = "🧠 LETZTE KONVERSATIONEN:\n\n"
        for i, conv in enumerate(conversations, 1):
            timestamp = conv['timestamp'][:16].replace('T', ' ')
            history_text += f"{i}. [{timestamp}] {conv['model_used']}\n"
            history_text += f"   User: {conv['user_prompt'][:80]}{'...' if len(conv['user_prompt']) > 80 else ''}\n"
            history_text += f"   Code: {conv['generated_code'][:100]}{'...' if len(conv['generated_code']) > 100 else ''}\n\n"

        stats = memory.get_statistics()
        history_text += f"📊 STATISTIKEN:\n"
        history_text += f"• Gesamt: {stats['total_conversations']} Konversationen\n"
        history_text += f"• Heute: {stats['conversations_today']} Konversationen\n"
        history_text += f"• Snippets: {stats['total_snippets']}\n"
        history_text += f"• Projekte: {stats['total_projects']}"

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=10)
        scroll = ScrollView()
        history_label = Label(
            text=history_text,
            text_size=(350, None),
            halign="left",
            valign="top",
            font_size='11sp'
        )
        history_label.bind(texture_size=history_label.setter('size'))
        scroll.add_widget(history_label)
        content.add_widget(scroll)

        clear_btn = Button(
            text="🗑️ Memory löschen",
            size_hint_y=None,
            height='40dp',
            background_color=(0.8, 0.3, 0.3, 1)
        )
        clear_btn.bind(on_release=lambda x: self.clear_memory())
        content.add_widget(clear_btn)

        popup = Popup(
            title="🧠 Conversation Memory",
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=True
        )
        popup.open()

    def clear_memory(self):
        deleted = memory.cleanup_old_conversations(days_to_keep=0)
        self.status_text = f"🧠 Memory gelöscht ({deleted} Konversationen)"
        Clock.schedule_once(lambda dt: setattr(self, 'status_text', 'Bereit'), 3.0)

    def copy_output(self):
        if self.output_text and not self.output_text.startswith(("Hier erscheint", "⏳", "❌", "🔄")):
            Clipboard.copy(self.output_text)
            self.status_text = "📋 Code kopiert!"
            Clock.schedule_once(lambda dt: setattr(self, 'status_text', 'Bereit'), 2.0)
        else:
            self.show_popup("❌ Fehler", "Kein Code zum Kopieren vorhanden!")

    def clear_all(self):
        self.stop_generation()
        self.user_prompt = ""
        self.output_text = "Hier erscheint der generierte Code..."
        self.status_text = "Bereit"

    def refresh_models(self):
        clear_cache()
        self.models = []
        self.selected_model = ""
        self.load_models_async()

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(
                text=message,
                text_size=(300, None),
                halign="center",
                valign="middle"
            ),
            size_hint=(0.9, 0.6),
            auto_dismiss=True
        )
        popup.open()

if __name__ == "__main__":
    CodeGenApp().run()
