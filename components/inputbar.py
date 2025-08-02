from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class InputBar(BoxLayout):
    """Eingabezeile mit Textfeld und Senden-Button."""
    on_send = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(6)

        self.input = TextInput(
            multiline=False,
            size_hint_x=0.85,
            padding=[dp(10), dp(10)],
            font_size='16sp',
            hint_text='Nachricht eingeben…',
            background_normal='',
            background_active='',
            background_color=(.15, .15, .15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )

        self.button = Button(
            text='Senden',
            size_hint_x=0.15,
            bold=True,
            background_color=(.1, .5, .8, 1),
            color=(1, 1, 1, 1)
        )

        self.button.bind(on_release=self._send_msg)
        self.input.bind(on_text_validate=self._send_msg)

        self.add_widget(self.input)
        self.add_widget(self.button)

    def _send_msg(self, *_):
        msg = self.input.text.strip()
        if msg:
            if self.on_send:
                self.on_send(msg)
            Clock.schedule_once(lambda _: self.input.setter("text")(self.input, ""), 0.05)
