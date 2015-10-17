#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import curses

CH_NUM_IN_LINE = 16#94
CH_BYTE_SIZE = 4#8

CH_HEIGHT = 8
CH_WIDTH  = 4#8

def char_to_index(font, ch_x, ch_y):
    return (ch_y * CH_NUM_IN_LINE + ch_x) * CH_BYTE_SIZE

def draw_char(stdscr, font, base_x, base_y, ch_x, ch_y):
    for x in range(CH_WIDTH):
        index = x + char_to_index(font, ch_x, ch_y)
        for y in range(CH_HEIGHT):
            if font[index] & (1<<y):
                str = 'XX'
            else:
                str = '  '
            stdscr.addstr(base_y + y, base_x + x*2, str)
            """
            # curses.A_REVERSEで反転表示可能．
            # 'XX'とどっちが見やすいかについては今後検討．
            if font[index] & (1<<y):
                stdscr.addstr(base_y + y, base_x + x*2, '  ', curses.A_REVERSE)
            else:
                stdscr.addstr(base_y + y, base_x + x*2, '  ')
            """

def curses_main(stdscr):
    #font = np.fromfile('./font/misaki_gothic.fnt', dtype=np.uint8)
    font = np.fromfile('./font/misaki_4x8_jisx0201.fnt', dtype=np.uint8)

    #ch_array = np.fromstring(u'　滌漾熙'.encode('shift-jis'), dtype=np.uint8)
    ch_array = np.fromstring('Hello World!', dtype=np.uint8)
    #for i in range(0, len(ch_array), 2):
    for i in range(0, len(ch_array)):
    #    hi = ch_array[i]
    #    lo = ch_array[i+1]
    #    ch_x, ch_y = sjis_to_font(hi, lo)
        ch_x = ch_array[i] % 16
        ch_y = ch_array[i] / 16
        draw_char(stdscr, font, i*7, 0, ch_x, ch_y)

    stdscr.getch()
    stdscr.refresh()

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
