import tensorflow as tf
from tensorflow.python.keras.backend import set_session
import numpy as np


config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.15
session = tf.compat.v1.Session(config=config)
set_session(session)


class FERModel(object):

    classes = ['😠 Angry', '🤢 Disgust', '😨 Fear',
               '😃 Happy', '😞 Sad', '😲 Surprise', '😐 Neutral']

    def __init__(self, model_path):
        self.emonet = tf.keras.models.load_model(model_path)

    def predict(self, image):
        global session
        set_session(session)
        self.preds = self.emonet.predict(image)

        return FERModel.classes[np.argmax(self.preds)]
