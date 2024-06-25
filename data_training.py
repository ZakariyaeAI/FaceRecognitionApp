import os
from PIL import Image
import numpy as np
import cv2
import pickle


class DataTraining():
    def __init__(self):
        pass

    def train(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, 'images')

        face = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        id = 0
        label_ids = {}
        y_labels = []
        x_train = []

        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg'):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()
                    # print(label, path)
                    if not label in label_ids:
                        label_ids[label] = id
                        id += 1
                    idc = label_ids[label]

                    pil_img = Image.open(path).convert('L')
                    size = (550, 550)
                    final_image = pil_img.resize(size, Image.ANTIALIAS)
                    image_array = np.array(final_image, 'uint8')
                    # print(image_array)
                    faces = face.detectMultiScale(image_array)
                    for (x, y, w, h) in faces:
                        roi = image_array[y:y+w+10, x:x+h]
                        x_train.append(roi)
                        y_labels.append(idc)
        with open('labels.pickles', 'wb') as f:
            pickle.dump(label_ids, f)
        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("trainner.yml")
