#encoding=utf-8
import json
import datetime

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from webapi import ASSETS_DIR, ASSETS_FONTS_DIR, ASSETS_IMAGES_DIR, ASSETS_TEMPLATE_DIR
from webapi import utils


def draw_ellipse(image, bounds, width=1, outline='white', antialias=5):
    """
    Copied from StackOverFlow: to draw a ellipse with customized borderline.
    """
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)
    for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)
    mask = mask.resize(image.size, Image.LANCZOS)
    image.paste(outline, mask=mask)


def circlemask(img, canvas, pos, radius):
    diameter = 2 * radius
    width, height = img.size
    scale = max(diameter / float(width), diameter / float(height))
    img = img.resize((int(scale * width), int(scale * height)), Image.ANTIALIAS)
    width, height = img.size
    box = (width / 2 - radius, 0, width / 2 + radius, diameter)
    img = img.crop(box)
    mask = Image.new('L', img.size, 0)
    drawer = ImageDraw.Draw(mask)
    drawer.ellipse((0, 0, diameter, diameter), fill=255)
    img.putalpha(mask) 
    canvas.paste(img, pos, mask=mask)
    bounds = pos + (pos[0] + diameter, pos[1] + diameter)
    draw_ellipse(canvas, bounds, 10)


font2file = {
    'kai': 'simkai.ttf',
    'lishu': 'STLITI.TTF',
    'msyhl': 'msyhl.ttc',
    'msyh': 'msyh.ttc'
}


def typewrite(img, text, pos, font_size, font='kai', align='left'):
    font_rgba = (0, 0, 0, 255)
    font = ImageFont.truetype(font=ASSETS_FONTS_DIR + font2file[font], size=font_size)
    drawer = ImageDraw.Draw(img)
    if align == 'left':
        drawer.text(pos, text, font=font, fill=font_rgba)
    else:
        text_width, text_height = drawer.textsize(text, font=font)
        start = pos[0] - text_width, pos[1]
        drawer.text(start, text, font=font, fill=font_rgba)


abbr2full = {
    u'清芬': '清芬园食堂',
    u'三教': '第三教学楼',
    u'四教': '第四教学楼',
    u'文图': '人文社科图书馆',
    u'校史馆': '清华校史馆',
    u'新清华学堂': '新清华学堂',
    u'六教': '第六教学楼'
}


def preprocess(data):
    img = data['img']
    img = utils.cv2pil(img)
    predicted = utils.to_unicode(data['predicted'])
    title = utils.to_unicode(abbr2full[predicted])
    description = utils.to_unicode(data['description'])
    return img, predicted, title, description


def render_v1(data):
    img, predicted, title, description = preprocess(data)

    canvas = Image.open(ASSETS_TEMPLATE_DIR + '1.png')
    canvas.paste(utils.crop(img, std_size=(982, 982), mode='PIL'), (44, 49))

    typewrite(canvas, title, (44, 1209), font_size=90)
    typewrite(canvas, description, (50, 1365), font_size=45)

    profile = Image.open(ASSETS_IMAGES_DIR + predicted + '.jpg')
    circlemask(profile, canvas, (688, 838), 180)

    canvas.save('a.png')


def render_v2(data):
    img, predicted, title, description = preprocess(data)

    canvas = Image.open(ASSETS_TEMPLATE_DIR + '2.png')
    canvas.paste(utils.crop(img, std_size=(983, 691), mode='PIL'), (48, 806))

    border = Image.open(ASSETS_TEMPLATE_DIR + 'border.png')
    canvas.paste(border, (0, 0), mask=border)

    typewrite(canvas, title, (924, 290), font_size=107, align='right', font='msyhl')
    typewrite(canvas, description, (924, 460), font_size=50, align='right', font='msyhl')

    today = datetime.date.today().strftime('%b %d, %Y')
    typewrite(canvas, today, (916, 600), font_size=45, align='right', font='lishu')

    canvas.convert('RGB').save('b.jpg') 


if __name__ == '__main__':
    img = cv2.imread('test.png')
    predicted = u'文图'
    description = u'—— 孕育梦想的青春战场'
    render_v2({'img': img, 'predicted': predicted, 'description': description})
