#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import exceptions
from PIL import Image
import PIL.ImageColor as IC

""" RGBA-PNGとL-PNGでデータ形式が異なることへの対処 """
def getcolor(image, color):
    if image.getbands() == ('R', 'G', 'B', 'A'):
        return IC.getcolor(color, 'RGBA')
    elif image.getbands() == ('1',):
        return IC.getcolor(color, 'L')
    else:
        raise exceptions.NotImplementedError('Only RGBA or L format!')

def print_char_image(image, ch_width, ch_height, ch_x, ch_y):
    white_color = getcolor(image, 'white')
    for y in range(ch_height):
        for x in range(ch_width):
            xy = (x + ch_x * ch_width, y + ch_y * ch_height)
            if image.getpixel(xy) == white_color:
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
def char_to_array(image, ch_width, ch_height, ch_x, ch_y):
    black_color = getcolor(image, 'black')
    array = []
    for x in range(ch_width):
        ptn = 0x00
        for y in range(ch_height):
            xy = (x + ch_x * ch_width, y + ch_y * ch_height)
            if image.getpixel(xy) == black_color:
                ptn |= 1<<y
        array.append(ptn)
    return array

if __name__ == '__main__':
    image = Image.open('./image/misaki_gothic.png')
    # DEBUG: 'Ａ'を表示
    print_char_image(image, 8, 8, 0, 6)
    """ 8x8の変換処理 """
    with open('./font/misaki_gothic.fnt', 'wb') as font:
        for y in range(94):
            for x in range(94):
                array = bytearray(char_to_array(image, 8, 8, x, y))
                font.write(array)

    image = Image.open('./image/misaki_4x8_jisx0201.png')
    # DEBUG: 'A'を表示
    print_char_image(image, 4, 8, 1, 4)
    """ 4x8の変換処理 """
    with open('./font/misaki_4x8_jisx0201.fnt', 'wb') as font:
        for y in range(16):
            for x in range(16):
                array = bytearray(char_to_array(image, 4, 8, x, y))
                font.write(array)
