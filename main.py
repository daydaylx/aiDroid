#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class SimpleApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        title = Label(
            text="aiDroid S25 Pro\nSamsung Galaxy Optimierung", font_size="20sp"
        )

        button = Button(
            text="Samsung S25 Features aktivieren", size_hint_y=None, height="50dp"
        )

        layout.add_widget(title)
        layout.add_widget(button)

        return layout


if __name__ == "__main__":
    SimpleApp().run()
