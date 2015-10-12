#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PIL import Image

CH_HEIGHT = 8
CH_WIDTH  = 8

def print_char_image(image, ch_x, ch_y):
    for y in range(CH_HEIGHT):
        for x in range(CH_WIDTH):
            xy = (x + ch_x * CH_WIDTH, y + ch_y * CH_HEIGHT)
            if image.getpixel(xy) == (255, 255, 255, 255):
                sys.stdout.write('  ')
            else:
                sys.stdout.write('XX')
        sys.stdout.write('\n')

if __name__ == '__main__':
    image = Image.open('./image/misaki_gothic.png')
    for y in range(94):
        for x in range(94):
            print_char_image(image, x, y)
