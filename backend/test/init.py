import cv2
import numpy as np
import pickle 
import os
import glob
import sys
from collections import defaultdict

import imutils
import utils

config = utils.load_config()
image_names = glob.glob("../images/test/*/*.png")

X = []
y = []
image_ids = []

print ""
counters = defaultdict(int)

for i in range(len(image_names)):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print "processing image... %.2f" % ((1. + i) / len(image_names) * 100.) + "%"

    image_name = image_names[i]
    # image = (cv2.imread(image_name) - 128.0) / 255.0
    image = cv2.imread(image_name)
    image = imutils.crop(image, (config.width, config.height))
    cv2.imwrite('.debug/' + image_name.split('/')[-1], image)
    image = (image - 128.0) / 255.0

    X.append(image)
    li = image_name.split("/")
    
    idx = int(li[3][0])
    onehot = [0] * 7
    onehot[idx] = 1
    y.append(onehot)
    counters[idx] += 1
    
    image_ids.append(image_name)

print counters
X = np.array(X)
y = np.array(y)

print X.shape

with open("../dataset/test/data_X_x6.npy", "w") as f:
    np.save(f, X)
with open("../dataset/test/data_y_x6.npy", "w") as f:
    np.save(f, y)
with open("../dataset/test/data_ids_x6.npy", "w") as f:
    np.save(f, image_ids)

