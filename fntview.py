#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import curses
import FontImage

def draw_char(win, base_x, base_y, limit_x, limit_y,
              ch_data, ch_width, ch_height):
    for x in range(ch_width):
        draw_x = base_x + x*2
        if not (0 <= draw_x and draw_x < limit_x - 1):
            continue
        for y in range(ch_height):
            draw_y = base_y + y
            if not (0 <= draw_y and draw_y < limit_y - 1):
                continue
            if ch_data[x] & (1<<y):
                win.addstr(draw_y, draw_x, '  ', curses.A_REVERSE)
            else:
                win.addstr(draw_y, draw_x, '  ')

def draw_string(win, font, base_x, base_y, sjis_str):
    ch_array = np.fromstring(sjis_str, dtype=np.uint8)
    # 8x8
    for i in range(0, len(ch_array), 2):
        hi = ch_array[i]
        lo = ch_array[i+1]
        ch_x, ch_y = sjis_to_font(hi, lo)
        ch_data = font.get(ch_x, ch_y)
        draw_char(win, base_x + i*8, base_y + 0, WIN_WIDHT, WIN_HEIGHT,
                  ch_data, font.ch_width, font.ch_height)
    """
    # 4x8
    for i in range(0, len(ch_array), 1):
        ch_x, ch_y = ch_array[i] % 16, ch_array[i] / 16
        ch_data = font.get(ch_x, ch_y)
        draw_char(win, base_x + i*8, base_y + 0, WIN_WIDHT, WIN_HEIGHT,
                  ch_data, font.ch_width, font.ch_height)
    """

WIN_WIDHT = 256
WIN_HEIGHT = 32

def curses_main(stdscr):
    font4x8 = FontImage.FontImage('./font/misaki_4x8_jisx0201.fnt',
                                  4, 8, 16, 4)
    font8x8 = FontImage.FontImage('./font/misaki_gothic.fnt',
                                  8, 8, 94, 8)

    win = curses.newwin(WIN_HEIGHT, WIN_WIDHT)
    win.noutrefresh()

    sjis_str = u'遥か３８万キロのボヤージュ'.encode('shift-jis')
    #sjis_str = u'abcdefghijklmnopqrstuvwxyz0123456789'.encode('shift-jis')

    while True:
        begin_offset = WIN_WIDHT
        end_offset = - len(sjis_str) * 8

        for x in range(begin_offset, end_offset, -2):
            draw_string(win, font8x8, x, 0, sjis_str)
            #draw_string(win, font4x8, x, 0, sjis_str)

            win.refresh()
            curses.doupdate()

            import time
            time.sleep(0.050)

def sjis_to_font(hi, lo):
    """
    第一バイト
    ・[0x81～0x9f]と[0xe0～0xef]の範囲に大別される．
    ・前半であれば，0x81を引くだけでよい．
    ・後半であれば，0x81と2範囲の空間分を引く．
    ・" * 2" は第一バイトに2つの区(01～63)が含まれて
    　いることに対応させる計算である．
    """
    if 0x81 <= hi and hi <= 0x9f:
        ch_y = (hi - 0x81) * 2
    elif 0xe0 <= hi and hi <= 0xef:
        ch_y = (hi - 0x81 - (0xe0 - 0x9f - 1)) * 2

    """
    第二バイト
    ・[0x40～0x7e]と[0x80～0xfc]の範囲からなる．
    　見方を変えれば，0x7fのみが抜けた連番である．
    ・前半であれば，0x40を引くだけでよい．
    ・後半であれば，0x40と1(0x7fの分)を引く．
    """
    if 0x40 <= lo and lo <= 0x7e:
        ch_x = lo - 0x40
    elif 0x80 <= lo and lo <= 0xfc:
        ch_x = lo - 0x40 - 1

    return ch_x, ch_y

if __name__ == '__main__':
    curses.wrapper(curses_main)
