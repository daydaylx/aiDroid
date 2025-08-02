from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from controller.network import OpenRouterClient
import asyncio

class ModelDropdown(Spinner):
    """
    Dynamisch gefüllte Dropdown-Liste aller OpenRouter-Modelle.
    Meldet Auswahl via `on_model_selected(model_id)`
    """
    on_model_selected = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Modelle laden…"
        self.values = []
        Clock.schedule_once(lambda _: self.load_models(), 1)

    def load_models(self):
        async def fetch():
            client = OpenRouterClient()
            try:
                models = await client.fetch_models()
                choices = sorted(set(m["id"] for m in models))
                self.values = choices
                self.text = "Modell wählen"
            except Exception:
                self.text = "Fehler beim Laden"

        asyncio.ensure_future(fetch())

    def on_text(self, instance, value):
        if self.on_model_selected and value not in ("Modelle laden…", "Modell wählen"):
            self.on_model_selected(value)
