import cv2
import os


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
            elif count >= 30:  # Take 30 face sample and stop video
                break

        print("\n [INFO] Exiting Program and cleanup stuff")
        video.release()
        cv2.destroyAllWindows()
