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
        # img = cv2.resize(img, (360, 640))
        # img = Image.fromarray(img)
        # std_width, std_height = 360, 640
        # width, height = img.size
        # scale_x = std_width / float(width)
        # scale_y = std_height / float(height)
        # scale = max(scale_x, scale_y)
        # img = img.resize((int(width * scale + 0.5), int(height * scale + 0.5)), 
        #         Image.ANTIALIAS)
        # width, height = img.size
        # left = (width - std_width) / 2
        # top = (height - std_height) / 2
        # right = (width + std_width) / 2
        # bottom = (height + std_height) / 2
        # img = img.crop((left, top, right, bottom))
        # img.save('a.png')
        # X = np.array(img)
        # return np.array([img - 128.0 / 255.0])
        return np.array([(cv2.resize(img, (360, 640)) - 128.0) / 255.0])


    @classmethod
    def predict(cls, img):
        with cls.graph.as_default():
            X = cls.normalize(img)

            #*******************DEBUG*********************
            def print_layer(layer_idx):
                inputs_op = cls.model.input
                print cls.model.layers[layer_idx].name
                output_op = cls.model.layers[layer_idx].output
                output_fn = K.function([inputs_op], [output_op])
                output = output_fn([X])[0][0]
                print output.shape

                if output.ndim == 3:    # CNN layer
                    for channel_idx in xrange(output.shape[-1]):
                        channel = output[:, :, channel_idx]
                        mi, mx = np.min(channel), np.max(channel)
                        if mi == mx:
                            print 'layer:', layer_idx, 'channel:', channel_idx, 'value:', mx
                            continue
                        else:
                            print 'layer:', layer_idx, 'channel:', channel_idx, 'max:', mx, 'min:', mi, 'mean:', np.mean(channel)
                        channel = ((channel - mi) / float(mx - mi)) * 255
                        cv2.imwrite('.debug/%d-%d.png' % (layer_idx, channel_idx), channel)
                else:
                    print output
                print

            # print_layer(1)
            # print_layer(4)
            # print_layer(9)
            # print_layer(10)
            #*******************DEBUG*********************

            return id2building[np.argmax(cls.model.predict(X)[0])]


if __name__ == '__main__':
    # img_name = '../images/test/1_qingfen_mini/qingfen_1.png'
    img_name = '.debug/input.jpg'
    img = cv2.imread(img_name)
    print img.dtype
    img = np.array([(cv2.resize(img, (360, 640)) - 128.0) / 255.0])
    print id2building[np.argmax(ModelWrapper.model.predict(img)[0])]

