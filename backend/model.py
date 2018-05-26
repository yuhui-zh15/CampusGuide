import numpy as np

from keras.models import *
from keras.layers import *
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.optimizers import SGD, Adam
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten


def model_fn(config):
    model = Sequential()
    model.add(Convolution2D(                        # 0
        batch_input_shape=(None, 640, 360, 3),
        filters=32,
        kernel_size=5,
        strides=1,
        padding='same'     # Padding method
    ))
    model.add(Activation('relu'))                   # 1

    model.add(MaxPooling2D(                         # 2
        pool_size=4,
        strides=4,
        padding='same'    # Padding method
    ))

    # 160 x 90 x 32
    model.add(Convolution2D(                        # 3
        batch_input_shape=(None, 160, 90, 32),
        filters=64,
        kernel_size=5,
        strides=1,
        padding='same'     # Padding method
    ))
    model.add(Activation('relu'))                   # 4

    model.add(MaxPooling2D(                         # 5
        pool_size=5,
        strides=5,
        padding='same'    # Padding method
    ))

    # 32 x 18 x 64
    model.add(Flatten())                            # 6
    model.add(Dense(1024))                          # 7
    model.add(Activation('relu'))                   # 8
    model.add(Dense(config.num_of_class))           # 9
    model.add(Activation('softmax'))                # 10

    adam = Adam(lr=config.lr)
    model.compile(optimizer=adam,
        loss='categorical_crossentropy',
        metrics=['accuracy'])
    
    return model

