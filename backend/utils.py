#encoding=utf-8
import numpy as np
import pickle as pkl 
import random
import os
import sys
import argparse


# id2building = {
#     0: 'unknown',
#     1: '清芬',
#     2: '三教',
#     3: '四教',
#     4: '文图',
#     5: '校史馆',
#     6: '新清华学堂',
#     7: '六教'      
# }

# id2building = {
#     0: '清芬',
#     1: '三教',
#     2: '四教',
#     3: '文图',
#     4: '校史馆',
#     5: '新清华学堂',
#     6: '六教',
#     7: 'unknown'
# }

id2building = {
    0: '清芬',
    1: '三教',
    2: '四教',
    3: '文图',
    4: '新清华学堂',
    5: '六教',
    6: 'unknown'
}

def load_data(X_path, y_path):
    print "loading data..."
    X = np.load(X_path)
    y = np.load(y_path)
    idx = range(len(X))
    random.shuffle(idx)
    X = X[idx]
    y = y[idx]
    print X.shape
    print y.shape
    return X, y


def load_config():
    """ZP: Please call this func before accessing the
       global variables. I believe it's good to encapsulate 
       them into 1 function/1 file... 
    """
    class Config:
        cv = 5
        # for x6 (no 校史馆)
        model_name = 'cnn_x6'
        lr = 1e-3
        num_of_class = 7
        # for vgg19
        # model_name = "vgg19"
        # lr = 3e-3
        # num_of_class = 8
        decay = 0.
        mm = 0.9
        bs = 15
        height = 48
        width = 32
    print({k:v for k,v in Config.__dict__.items() if not k.startswith("__")})
    config = Config()
    return config

if __name__ == "__main__":
    X, y = load_data(X_path, y_path)
    print X.shape
    print y.shape
