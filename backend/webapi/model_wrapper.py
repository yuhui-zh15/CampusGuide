#encoding=utf-8
import numpy as np
import cv2
import tensorflow as tf

from utils import load_config, id2building
from model import model_fn
from webapi import imutils


class ModelWrapper(object):
    config = load_config()
    model = model_fn(config)
    model_path = '../model/%s-%d' % (config.model_name, 5)
    model.load_weights(model_path)
    # Hack: This fixes a keras bug with TF backend in async environment,
    # see https://github.com/keras-team/keras/issues/2397 for details.
    graph = tf.get_default_graph()
    print 'successfully loaded model from: %s' % model_path

    
    @staticmethod
    def normalize(img):
        """
        cropping and zero-centering
        """
        img = imutils.crop(img, std_size=(360, 640))
        img = (img - 128.0) / 255.0
        return np.array([img])


    @classmethod
    def predict(cls, img):
        with cls.graph.as_default():
            X = cls.normalize(img)
            return id2building[np.argmax(cls.model.predict(X)[0])]


if __name__ == '__main__':
    img_name = '.debug/qingfen.jpg'
    img = cv2.imread(img_name)
    img = ModelWrapper.normalize(img)
    print ModelWrapper.predict(img)

