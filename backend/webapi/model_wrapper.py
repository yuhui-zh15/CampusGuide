#encoding=utf-8
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from keras import backend as K

from utils import load_config, id2building
from model import model_fn


class ModelWrapper(object):
    config = load_config()
    model = model_fn(config)
    model_path = '../model/%s-%d' % (config.model_name, 1)
    model.load_weights(model_path)
    # Hack: This fixes a keras bug with TF backend in async environment,
    # see https://github.com/keras-team/keras/issues/2397 for details.
    graph = tf.get_default_graph()
    print 'successfully loaded model from: %s' % model_path

    
    @staticmethod
    def normalize(img):
        img = (cv2.resize(img, (360, 640)) - 128.0) / 255.0
        cv2.imwrite('.debug/norm.png', )
        return np.array([img])


    @classmethod
    def predict(cls, img):
        with cls.graph.as_default():
            X = cls.normalize(img)
            return id2building[np.argmax(cls.model.predict(X)[0])]


if __name__ == '__main__':
    # img_name = '../images/test/1_qingfen_mini/qingfen_1.png'
    img_name = '.debug/input.jpg'
    img = cv2.imread(img_name)
    print img.dtype
    img = np.array([(cv2.resize(img, (360, 640)) - 128.0) / 255.0])
    print id2building[np.argmax(ModelWrapper.model.predict(img)[0])]

