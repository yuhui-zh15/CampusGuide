#encoding=utf-8
import numpy as np
import cv2
import tensorflow as tf

from utils import load_config, id2building
from model import model_fn


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
        std_width, std_height = 360, 640
        height, width, _ = img.shape
        scale_x = std_width / float(width)
        scale_y = std_height / float(height)
        scale = max(scale_x, scale_y)
        new_shape = (int(width * scale + 0.5), int(height * scale + 0.5))
        img = cv2.resize(img, new_shape)
        width, height = new_shape
        left = (width - std_width) / 2
        top = (height - std_height) / 2
        right = (width + std_width) / 2
        bottom = (height + std_height) / 2
        img = img[top:bottom, left:right, :]
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

