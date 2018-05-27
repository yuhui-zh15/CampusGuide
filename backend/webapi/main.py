"""
Usage:
    (backend)$ CUDA_VISIBLE_DEVICES=[gpu_id] python -m webapi.main
"""

#encoding=utf-8
import os
import time
import json

import cv2
import numpy as np
import flask
from flask import Flask, Response
from flask import request

from model_wrapper import ModelWrapper
from webapi import *
from share import render_fn


app = Flask(__name__)


def get_user_dir(user_id):
    return CACHE_DIR + user_id + '/'


@app.route('/upload', methods=['POST'])
def upload():
    print 'uploading...'
    fin =  request.files['file']
    data = fin.read()
    user_id = request.form['openid']
    user_dir = get_user_dir(user_id)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)      # TODO: delete zombie cache

    img = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    predicted = ModelWrapper.predict(img)
    assets = json.load(open(ASSETS_DIR + ASSETS_JSON_FILE))
    resp_dict = assets[predicted.decode('utf-8')]
    resp_dict.update({'predicted': predicted})
    resp = flask.jsonify(resp_dict)
    print predicted
    print resp
    
    with open(user_dir + CACHE_IMAGE_FILE, 'wb') as fout:
        fout.write(data)
    json_data = {'predicted': predicted, 'description': resp_dict['description']}
    json.dump(json_data, open(user_dir + CACHE_JSON_FILE, 'w'))
    return resp


@app.route('/share', methods=['GET'])
def share():
    print 'sharing...'
    args = request.args
    user_id = args['openid']
    option = int(args['option'])
    print user_id, option
    user_dir = get_user_dir(user_id)
    img = cv2.imread(user_dir + CACHE_IMAGE_FILE)
    data = json.load(open(user_dir + CACHE_JSON_FILE))
    data['img'] = img

    assert option >= 0 and option < len(render_fn), 'Invalid option: %d' % option
    share_img = render_fn[option](data)
    share_img_encode = cv2.imencode('.jpg', share_img)[1].tostring()
    cv2.imwrite('share_img.jpg', share_img)
    with open('share_img_encode.jpg', 'wb') as fout:
        fout.write(share_img_encode)
    return app.make_response(share_img_encode)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

