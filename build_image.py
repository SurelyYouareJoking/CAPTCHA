#coding=utf-8

import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import string
import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# from ckanext.unicom.model.check_image import Images
# from ckan.lib.base import BaseController, model, abort, h, redirect

#字体的位置，不同版本的系统会有不同
FONT_PATH = '/home/ziru/ckan/lib/default/src/ckanext-unicom/ckanext/unicom/public/captcha/font/GB18030.ttf'
IMAGE_PATH = '/home/ziru/ckan/lib/default/src/ckanext-unicom/ckanext/unicom/public/captcha/'
#生成几位数的验证码
NUMBER = 4
#生成验证码图片的高度和宽度
SIZE = (100, 30)
#背景颜色
BGCOLOR = (255, 255, 255)
#字体颜色
FONTCOLOR = (0, 0, 255)
#干扰线颜色
LINECOLOR = (0, 0, 255)
#是否要加入干扰线
DRAW_LINE = True
#加入干扰线条数的上下限
LINE_NUMBER = (1, 5)

#用来随机生成一个字符串
def gene_text():
    source = list(string.letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, NUMBER))#number是生成验证码的位数

#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=LINECOLOR)

#生成验证码
def gene_code():
    width, height = SIZE
    image = Image.new('RGBA', (width, height), BGCOLOR)
    file = open(FONT_PATH)
    file.close()
    font = ImageFont.truetype(FONT_PATH, 25)
    draw = ImageDraw.Draw(image)
    text = gene_text()
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / NUMBER,
               (height - font_height) / NUMBER),
              text, font=font, fill=FONTCOLOR)
    if DRAW_LINE:
        gene_line(draw, width, height)
    #调整纸张样式
    # image = image.transform((width+20, height+10),
    #                         Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0),
    #                         Image.BILINEAR)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    ticks = datetime.now()
    dir_name = ticks.strftime("image%Y%m%d%H%M%S")
    save_image_path = ''.join([IMAGE_PATH, dir_name, '.png'])
    show_path = ''.join(['/captcha/', dir_name, '.png'])
    image.save(save_image_path)
    # c_image = Images({'path': show_path,
    #                   'code': text,})
    # model.Session.add(c_image)
    # model.Session.commit()

def get_image():
    gene_code()
    return Images.get_top()

if __name__ == "__main__":
  print gene_code()
