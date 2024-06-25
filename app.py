from kivy.app import App
# from kivy.uix.widget import Widget
from kivy.lang import Builder

# Designate Our .kv design file
kv = Builder.load_file('builder.kv')


class AwesomeApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    AwesomeApp().run()
