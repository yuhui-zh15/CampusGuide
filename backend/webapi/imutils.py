import json

import cv2
from PIL import Image
import numpy as np



def cv2pil(img):
    return Image.fromarray(img[:, :, ::-1])


def pil2cv(img):
    return np.array(img)[:, :, ::-1]


def crop(img, std_size, mode='CV'):
    if mode == 'PIL': img = pil2cv(img)
    std_width, std_height = std_size
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
    if mode == 'PIL': img = cv2pil(img)
    return img


