from re import MULTILINE
from kivy.app import App
from kivy.core import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from getdataset import GetDataSet


class CollectWindow(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.4)
        self.color = (25, 132, 202)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # self.window.add_widget(Label(text='Tappez votre nom'))
        self.nom = TextInput(text="Tappez votre nom", multiline=False, padding_y=(
            30, 30), size_hint=(1, 0.3))
        self.window.add_widget(self.nom)
        # self.window.add_widget(Label(text='Tappez votre prénom'))
        self.prenom = TextInput(text="Tappez votre prénom", multiline=False, padding_y=(
            30, 30), size_hint=(1, 0.3))
        self.window.add_widget(self.prenom)
        # self.window.add_widget(Label(text='Tappez votre filière'))
        # self.filier = TextInput(text="Tappez votre filière", multiline=False,
        #                         padding_y=(20, 20), size_hint=(1, 0.3))
        # self.window.add_widget(self.filier)
        # self.window.add_widget(Label(text=''))
        self.btn = Button(text="Start", size_hint=(1, 0.3), bold=True,
                          background_color='#1984CA',
                          background_normal="")
        self.window.add_widget(self.btn)
        self.btn.bind(on_press=self.callBack)
        return self.window

    def callBack(self, instance):
        # os.system("python getdataset.py")
        fullname = f'{self.nom.text}_{self.prenom.text}'
        GetDataSet(fullname).run()


if __name__ == '__main__':
    CollectWindow().run()
