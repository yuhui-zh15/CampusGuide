#encoding=utf-8
import sys
from collections import defaultdict

import numpy as np

from utils import load_config, id2building
from model import model_fn, model_vgg19_fn


X_path = '../dataset/test/data_X_x6.npy'
y_path = '../dataset/test/data_y_x6.npy'
ids_path = '../dataset/test/data_ids_x6.npy'


def gen_markdown(correct, wrong):
    with open('test/report.md', 'w') as fout:
        fout.write('# Error Analysis\n\n')
        fout.write('## Wrong\n\n')
        
        expected2predicted = defaultdict(list)
        for id, expected, predicted in wrong:
            id = id.replace('../', '')
            expected2predicted[expected].append((id, predicted))

        for expected, items in expected2predicted.iteritems():
            fout.write('#### %s\n\n' % (id2building[expected]))
            for id, predicted in items:
                fout.write('expected = %s, predicted = %s\n\n' % (id2building[expected], id2building[predicted]))
                fout.write('![img](%s)\n\n' % (id))

        fout.write('## Correct\n\n')
        expected2predicted = defaultdict(list)
        for id, expected, predicted in correct:
            id = id.replace('../', '')
            expected2predicted[expected].append((id, predicted))

        for expected, items in expected2predicted.iteritems():
            fout.write('#### %s\n\n' % (id2building[expected]))
            for id, predicted in items:
                fout.write('expected = %s, predicted = %s\n\n' % (id2building[expected], id2building[predicted]))
                fout.write('![img](%s)\n\n' % (id))


def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-epoch', type=int, required=True)
    parser.add_argument('-mode', type=str, choices=['one', 'all'], required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()

    X = np.load(X_path)
    y = np.load(y_path)
    ids = np.load(ids_path)
    config = load_config()

    model = model_fn(config)

    if args.mode == 'all':
        for epoch in xrange(20):
            model.load_weights('../model/%s-%d' % (config.model_name, epoch))

            score = model.evaluate(X, y)
            print 'epoch:', epoch
            print 'score:', score
    else:
        model.load_weights('../model/best/%s-%d' % (config.model_name, args.epoch))

        score = model.evaluate(X, y)
        print 'score:', score

        correct = []
        wrong = []
        prediction = model.predict(X)
        for predicted, label, id in zip(prediction.tolist(), y.tolist(), ids.tolist()):
            expected = np.argmax(label)
            predicted = np.argmax(predicted)
            item = (id, expected, predicted)
            if expected == predicted:
                correct.append(item)
            else:
                wrong.append(item)

        print 'correct:'
        for id, expected, predicted in correct:
            print id, 'expected =', id2building[expected], 'predicted =', id2building[predicted]
        print 'wrong:'
        for id, expected, predicted in wrong:
            print id, 'expected =', id2building[expected], 'predicted =', id2building[predicted]

        gen_markdown(correct, wrong)
