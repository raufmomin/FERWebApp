import cv2
import numpy as np
from model import FERModel

face_detector = cv2.CascadeClassifier(
    './models/haarcascade_frontalface_default.xml')
fermodel = FERModel(
    './models/emonet.h5')
font = cv2.FONT_HERSHEY_DUPLEX


class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        faces = face_detector.detectMultiScale(frame, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = frame[y:y+h, x:x+w]
            roi = cv2.resize(roi, (48, 48))
            roi = np.expand_dims(roi, axis=0)
            pred = fermodel.predict(roi)

            cv2.putText(frame, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
