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

"""
--------< sample >--------
   (ch_x, ch_y) = (1, 3)
    +----------------+
    |    XX          |
    |  XXXXXXXXXX    |
    |    XX          |
    |    XXXXXXXX    |
    |  XXXX  XX  XX  |
    |XX  XXXX    XX  |
    |  XXXX    XX    |
    |                |
    +----------------+

--------< format >--------
     byte -->
 bit [0] [1] ... [7]
  |  <0> ... ... ...
  v  <1> ... ... ...
     ... ... ... ...
     <7> ... ... <7>

--------< output >--------
    [0x20, # 00100000
     0x52, # 01010010
     0x7f, # 01111111
     0x2a, # 00101010
     0x1a, # 00011010
     0x4a, # 01001010
     0x30, # 00110000
     0x00] # 0x000000
"""
def char_to_array(image, ch_x, ch_y):
    array = []
    for x in range(CH_WIDTH):
        ptn = 0x00
        for y in range(CH_HEIGHT):
            xy = (x + ch_x * CH_WIDTH, y + ch_y * CH_HEIGHT)
            if image.getpixel(xy) == (0, 0, 0, 255):
                ptn |= 1<<y
        array.append(ptn)
    return array

if __name__ == '__main__':
    image = Image.open('./image/misaki_gothic.png')
    with open('./font/misaki_gothic.fnt', 'wb') as font:
        for y in range(94):
            for x in range(94):
                array = bytearray(char_to_array(image, x, y))
                font.write(array)
