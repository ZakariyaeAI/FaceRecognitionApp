from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class Appnot(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size = (1, 0.1)
        self.window.add_widget(Label(text='training complet'))
        return self.window


if __name__ == "__main__":
    Appnot().run()
