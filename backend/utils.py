#encoding=utf-8
import numpy as np
import pickle as pkl 
import random
import os
import sys
import argparse


id2building = {
    0: 'unknown',
    1: '清芬',
    2: '三教',
    3: '四教',
    4: '文图',
    5: '校史馆',
    6: '新清华学堂',
    7: '六教'      
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
        num_of_class = 8
        cv = 5
        model_name = 'cnn'
        lr = 1e-4
    print({k:v for k,v in Config.__dict__.items() if not k.startswith("__")})
    config = Config()
    return config

if __name__ == "__main__":
    X, y = load_data(X_path, y_path)
    print X.shape
    print y.shape
