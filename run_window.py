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

        file = f'data_{tody}.csv'
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
