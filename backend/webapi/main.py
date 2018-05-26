#encoding=utf-8
import cv2
import numpy as np
from flask import Flask, Response
from flask import request

from model_wrapper import ModelWrapper


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    print 'uploading...'
    fin =  request.files['file']
    data = fin.read()

    tmp_path = '.debug/input.jpg'
    with open(tmp_path, 'wb') as fout:
        fout.write(data)
    img = cv2.imread(tmp_path)
    predicted = ModelWrapper.predict(img)
    print 'predicted:', predicted
    return app.make_response(predicted)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

