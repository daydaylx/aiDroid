import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

kivy.require('2.2.1') # replace with your current Kivy version

Builder.load_file('kv/main.kv')

class MainWidget(BoxLayout):
    pass

class aiDroidApp(App):
    def build(self):
        return MainWidget()

if __name__ == '__main__':
    aiDroidApp().run()
