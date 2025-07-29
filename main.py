from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.clipboard import Clipboard
from kivy.logger import Logger
from utils import fetch_models, generate_code
import os

Window.size = (400, 700)  # Desktop test
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class CodeGenApp(App):
    api_key = StringProperty("")
    system_prompt = StringProperty("Du bist ein erfahrener Python-Entwickler.")
    user_prompt = StringProperty("")
    output_text = StringProperty("Hier erscheint der generierte Code...")
    models = ListProperty([])
    selected_model = StringProperty("")
    is_loading = BooleanProperty(False)

    def build(self):
        self.title = "OpenRouter CodeGen"
        return Builder.load_file("kv/main.kv")

    def on_start(self):
        if self.api_key:
            self.load_models()

    def load_models(self):
        """Modelle von OpenRouter laden"""
        if not self.api_key.strip():
            self.show_popup("Fehler", "API Key fehlt")
            return
        try:
            models = fetch_models(self.api_key)
            if models:
                self.models = models
                if not self.selected_model and models:
                    self.selected_model = models[0]
            else:
                self.show_popup("Fehler", "Keine Modelle gefunden - API Key prüfen")
        except Exception as e:
            self.show_popup("API Fehler", str(e))

    def generate(self):
        """Code generieren"""
        if not self.api_key.strip():
            self.show_popup("Fehler", "API Key fehlt")
            return
        if not self.user_prompt.strip():
            self.show_popup("Fehler", "Prompt eingeben")
            return
        if not self.selected_model:
            self.show_popup("Fehler", "Modell auswählen")
            return

        self.is_loading = True
        self.output_text = "⏳ Generiere Code..."

        try:
            result = generate_code(
                self.api_key,
                self.selected_model,
                self.system_prompt,
                self.user_prompt
            )
            self.output_text = result
        except Exception as e:
            self.output_text = f"❌ Fehler: {str(e)}"
        finally:
            self.is_loading = False

    def copy_output(self):
        """Output in Zwischenablage"""
        if self.output_text and self.output_text != "Hier erscheint der generierte Code...":
            Clipboard.copy(self.output_text)
            self.show_popup("Kopiert", "Code wurde kopiert!")
        else:
            self.show_popup("Fehler", "Nichts zu kopieren")

    def clear_output(self):
        """Output löschen"""
        self.output_text = "Hier erscheint der generierte Code..."
        self.user_prompt = ""

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(250, None), halign="center"),
            size_hint=(0.8, 0.4),
            auto_dismiss=True
        )
        popup.open()

if __name__ == "__main__":
    CodeGenApp().run()

