import numpy as np

from keras.models import *
from keras.layers import *
from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input
from keras.optimizers import SGD, Adam
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization


def model_fn(config):
    model = Sequential()
    model.add(Convolution2D(                        # 0
        batch_input_shape=(None, config.height, config.width, 3),
        filters=128,
        kernel_size=16,
        strides=1,
        padding='same'     # Padding method
    ))
    model.add(Activation('relu'))                   # 1

    pool_size = 4
    model.add(MaxPooling2D(                         # 2
        pool_size=pool_size,
        strides=pool_size,
        padding='same'    # Padding method
    ))

    # 160 x 90 x 32
    model.add(Convolution2D(                        # 3
        batch_input_shape=(None, config.height/pool_size, config.width/pool_size, 64),
        filters=256,
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
    model.add(Dense(1024))  
    model.add(Activation('relu'))                   # 8
    model.add(Dense(config.num_of_class))           # 9
    model.add(Activation('softmax'))                # 10

    adam = Adam(lr=config.lr)
    model.compile(optimizer=adam,
        loss='categorical_crossentropy',
        metrics=['accuracy'])
    
    return model

def model_vgg19_fn(config):
    base_model = VGG19(weights = 'imagenet', include_top = False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(config.num_of_class, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    for layer in base_model.layers:
        layer.trainable = False

    sgd = SGD(lr=config.lr, decay=config.decay, momentum=config.mm, nesterov=True)
    model.compile(loss = 'categorical_crossentropy', 
            optimizer = sgd,
            metrics=['accuracy'])

    """
    for layer in base_model.layers[-2:]:
        layer.trainable = True
    
    sgd = SGD(lr=lr, decay=decay, momentum=mm, nesterov=True)
    model.compile(loss = 'categorical_crossentropy', 
            optimizer = 'sgd',
            metrics=['accuracy'])
    """

    return model
    
    """
    #model.fit_generator() # to be filled
    model.fit(X_train, y_train, batch_size = bs, nb_epoch=1, verbose=1)


    score = model.evaluate(X_test, y_test, verbose=0)
    print "test:", score
    """

