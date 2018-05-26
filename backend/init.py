import cv2
import numpy as np
import pickle 
import os
import glob
import sys

image_names = glob.glob("../images/*/*.png")

X = []
y = []

print ""

for i in range(len(image_names)):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print "processing image... %.2f" % ((1. + i) / len(image_names) * 100.) + "%"

    image_name = image_names[i]
    image = (cv2.imread(image_name) - 128.0) / 255.0
    X.append(image)
    li = image_name.split("/")
    
    idx = int(li[2][0])
    onehot = [0] * 8
    onehot[idx] = 1
    y.append(onehot)

X = np.array(X)
y = np.array(y)

print X.shape

with open("../dataset/data_X.npy", "w") as f:
    np.save(f, X)
with open("../dataset/data_y.npy", "w") as f:
    np.save(f, y)
