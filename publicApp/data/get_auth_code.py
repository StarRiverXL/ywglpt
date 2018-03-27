#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import logging, platform
from django.conf import settings
logger = logging.getLogger('django')

# 设置字体位置
font_path = '%s/static/publicApp/login/fonts/arial.ttf' % settings.BASE_DIR
# 生成几位数的验证码
number = 6
# 生成验证码图片的高度和宽度
size = (100, 30)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 5)


# 用来随机生成一个字符串
def gene_text():
    # source = list(string.letters)   # python2
    source = list(string.ascii_letters)     # python3
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


# 生成验证码
def gene_code(save_path, code_fine_name):
    """
    : param save_path: 图片保存路径
    : param code_fine_name: 图片保存名称
    : return: True
    """
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, 25)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    # text = gene_text()  # 生成字符串
    # print text
    font_width, font_height = font.getsize(code_fine_name)
    draw.text(((width - font_width) / number, (height - font_height) / number), code_fine_name, font=font,
              fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR) #创建扭曲
    image = image.transform((width + 30, height), Image.AFFINE, (1, 0, 0, 0, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    try:
        system_version = platform.system()
        if system_version == "Windows":
            image.save("%s\\%s.png" % (save_path, code_fine_name))  # 保存验证码图片
            logger.info("验证码图片保存成功,内容为：%s\\%s.png" % (save_path, code_fine_name))
        elif system_version == "Linux":
            image.save("%s/%s.png" % (save_path, code_fine_name))  # 保存验证码图片
            logger.info("验证码图片保存成功,内容为：%s/%s.png" % (save_path, code_fine_name))
        return True
    except Exception as e:
        logger.info("验证码保存图片失败，具体原因：%s" % e)
        return False

# if __name__ == '__main__':
#     gene_code()

