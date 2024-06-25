from kivy.app import App
from kivy.core import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from data_training import DataTraining
import os
import datetime
import numpy as np
import cv2
import pickle
# import pandas as pd
import datetime
import smtplib
from password import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class RunApp():
    def __init__(self):
        pass

    def run(self):
        face = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
        # smile = cv2.CascadeClassifier('data/haarcascade_smile.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainner.yml")

        labels = {}

        final_data = []

        full_name = "unkown"
        detected_faces = {}

        with open("labels.pickles", 'rb') as f:
            labels = pickle.load(f)
            labels = {v: k for k, v in labels.items()}

        # print(labels[0])
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face.detectMultiScale(gray)
            # smiles = smile.detectMultiScale(gray)
            # print(detected_faces)

            for (x, y, w, h) in faces:
                roi_gary = gray[y:y+h, x:x+h]
                id_, conf = recognizer.predict(roi_gary)
                color = (66, 245, 209)
                if conf < 100:
                    # print(id_)
                    # print(labels[id_])
                    conf = " {0}%".format(round(100-conf))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    full_name = name
                    stroke = 2
                    cv2.putText(frame, name, (x, y-10), font, 1,
                                color, stroke, cv2.LINE_AA)
                    detected_faces[name] = datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")

                else:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    stroke = 2
                    cv2.putText(frame, "unkown", (x, y-10), font, 1,
                                color, stroke, cv2.LINE_AA)
                # color = (255, 0, 0)
                stroke = 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, stroke)

            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        tody = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S").replace(' ', '_').replace(':', '_')

        file = f'./absence_files/data_{tody}.csv'
        with open(file, 'w') as f:
            for key in detected_faces:
                f.write("%s,%s\n" % (key, detected_faces[key]))

        msg = MIMEMultipart()

        msg['From'] = SENDER
        msg['To'] = RECEIVER
        msg['Subject'] = "Absence"

        body = "testing ..."
        msg.attach(MIMEText(body, 'plain'))
        attach = open(file, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attach).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename='+file)

        msg.attach(part)
        text = msg.as_string()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, text)
            server.quit()
        # print(SENDER, PASSWORD)
        # print("Done")

        cap.release()
        cv2.destroyAllWindows()


class GetDataSet():
    def __init__(self, face_id):
        self.face_id = face_id

    def run(self):
        faceCascade = cv2.CascadeClassifier(
            'data/haarcascade_frontalface_alt2.xml')
        #recognizer = cv2.face.LBPHFaceRecognizer_create()

        video = cv2.VideoCapture(0)
        path = f'images/{str(self.face_id)}'
        os.mkdir(path)
        count = 0
        while True:
            check, frame = video.read()
            # print(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # cv2.imshow("capture2",frame)

            faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                nframe = frame
                count += 1

                cv2.imwrite(path+"/" + self.face_id + "." +
                            str(count) + ".png", nframe)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # cv2.imwrite(f'dataset/user{face_id}-')

            cv2.imshow("frame", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            elif count >= 10:  # Take 30 face sample and stop video
                break
        video.release()
        cv2.destroyAllWindows()


class MyApp(App):
    def build(self):
        self.btn_color = "#1D90DB"
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # add image
        self.window.add_widget(Image(source="logo.png", size_hint=(1, 0.8)))
        # label
        self.collect_data_btn = Button(text="Collect data", size_hint=(1, 0.5),
                                       bold=True,
                                       background_color=self.btn_color,
                                       background_normal="")
        self.training_btn = Button(text="Train the model", size_hint=(1, 0.5),
                                   bold=True,
                                   background_color="#1984CA",
                                   background_normal="")
        self.run_btn = Button(text="Run", size_hint=(1, 0.5),
                              bold=True,
                              background_color=self.btn_color,
                              background_normal="")
        self.mail = TextInput(text="Tappez votre E-mail",
                              multiline=False, size_hint=(1, 0.2))
        self.window.add_widget(self.mail)
        self.collect_data_btn.bind(on_press=self.CollectDataCallBack)
        self.training_btn.bind(on_press=self.TrainingModelCallBack)
        self.run_btn.bind(on_press=self.RunCallBack)

        self.window.add_widget(self.collect_data_btn)
        self.window.add_widget(self.training_btn)
        self.window.add_widget(self.run_btn)

        return self.window

    def CollectDataCallBack(self, instance):
        os.system('python collect_data.py')

    def TrainingModelCallBack(self, instance):
        DataTraining().train()
        # os.system('python notif.py')
        self.training_btn = Button(text="Train the model \n(Training Complet)", size_hint=(1, 0.5),
                                   bold=True,
                                   background_color=self.btn_color,
                                   background_normal="")

    def RunCallBack(self, instance):
        RECEIVER = self.mail.text
        RunApp().run()


if __name__ == '__main__':
    MyApp().run()
    # RunWindow().run()
