#encoding=utf-8
import numpy as np
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
        img = img[:, :, ::-1]   # BGR -> RGB
        img = Image.fromarray(img)
        std_width, std_height = 360, 640
        width, height = img.size
        scale_x = std_width / float(width)
        scale_y = std_height / float(height)
        scale = max(scale_x, scale_y)
        img = img.resize((int(width * scale + 0.5), int(height * scale + 0.5)), 
                Image.ANTIALIAS)
        width, height = img.size
        left = (width - std_width) / 2
        top = (height - std_height) / 2
        right = (width + std_width) / 2
        bottom = (height + std_height) / 2
        img = img.crop((left, top, right, bottom))
        img.save('a.png')
        X = np.array(img)
        return np.array([X - 128.0 / 255.0])


    @classmethod
    def predict(cls, img):
        with cls.graph.as_default():
            X = cls.normalize(img)
            y = cls.model.predict(X)

            #*******************DEBUG*********************
            inputs = cls.model.input
            outputs = [layer.output for layer in cls.model.layers]
            functors = [K.function([inputs], [out]) for out in outputs]
            layer_outs = [func([X]) for func in functors]
            print layer_outs
            #*******************DEBUG*********************

            predicted = np.argmax(y, axis=1)[0]
            building = id2building[predicted]
            return building
