"""
Usage: If the images are changed, please first run `init.py`.
    (backend)$ CUDA_VISIBLE_DEVICES=[gpu_id] python main.py
"""

from sklearn.cross_validation import KFold

import utils
from model import model_fn


X_path = "../dataset/data_X.npy"
y_path = "../dataset/data_y.npy"


if __name__ == '__main__':
    X, y = utils.load_data(X_path, y_path)
    config = utils.load_config()

    kf = KFold(len(X), config.cv)
    for cnt, (train_idx, test_idx) in enumerate(kf):
        print "******************** Fold: ", cnt, " *************************"
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        model = model_fn(config)    
        print model
        
        for i in range(20):
            model.fit(X_train, y_train, batch_size=config.bs, epochs = 1, verbose=1)
            score = model.evaluate(X_test, y_test, verbose=0)
            model.save_weights('../model/%s-%d' % (config.model_name, i))
            print "test:", score
        
