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
        self.past_frame = None

    def __del__(self):
        self.video.release()

    def get_frame(self):
        try:
            ret, frame = self.video.read()
            frame = cv2.flip(frame, 1)

            faces = face_detector.detectMultiScale(frame, 1.3, 5)

            for (x, y, w, h) in faces:
                roi = frame[y:y+h, x:x+w]
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                roi = cv2.resize(roi, (48, 48))
                roi = np.reshape(roi, (48, 48, 1))
                roi = np.expand_dims(roi, axis=0)
                roi = roi/255.0
                pred = fermodel.predict(roi)

                cv2.putText(frame, pred, (int((x+w)/2), y-10),
                            font, 1, (255, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)

            frame = cv2.resize(frame, (640, 480))
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()

            if frame_bytes is not None:
                self.past_frame = frame_bytes

            return frame_bytes

        except Exception as e:
            print(e)

            return self.past_frame
