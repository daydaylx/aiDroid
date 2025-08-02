from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.clock import Clock

class ChatBubble(Label):
    """Einzelne Sprechblase mit Stil je nach Rolle."""
    def __init__(self, role, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint_y = None
        self.padding = [dp(12), dp(8)]
        self.font_size = '16sp'
        self.markup = True
        self.color = (.95, .95, .95, 1)
        self.text_size = (self.width, None)
        self.halign = 'right' if role == 'user' else 'left'
        self.valign = 'middle'
        self.role = role
        Clock.schedule_once(lambda _: self._resize(), 0)

    def _resize(self, *args):
        self.texture_update()
        self.height = self.texture_size[1] + dp(16)
        self.text_size = (self.width * 0.9, None)

    def append_token(self, token):
        self.text += token
        self._resize()


class ChatArea(ScrollView):
    """Container für alle Sprechblasen + Autoscroll."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_layout = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.add_widget(self.chat_layout)
        self.bubbles = []

    def add_bubble(self, role, text):
        bubble = ChatBubble(role, text, size_hint_x=0.9)
        self.chat_layout.add_widget(bubble)
        self.bubbles.append(bubble)
        Clock.schedule_once(lambda *_: self.scroll_to(bubble), 0.01)

    def stream_token(self, role, token):
        if not self.bubbles or self.bubbles[-1].role != role:
            self.add_bubble(role, "")
        self.bubbles[-1].append_token(token)
