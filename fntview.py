#!/usr/bin/python
# -*- coding: utf-8 -*-
import curses
import FontManager

WIN_WIDHT = 256
WIN_HEIGHT = 32

def draw_bitmap(win, bitmap, base_x, base_y, limit_x, limit_y):
    for x in range(len(bitmap)):
        draw_x = base_x + x*2
        if not (0 <= draw_x and draw_x < limit_x - 1):
            continue
        for y in range(8):
            draw_y = base_y + y
            if not (0 <= draw_y and draw_y < limit_y - 1):
                continue
            if bitmap[x] & (1<<y):
                win.addstr(draw_y, draw_x, '  ', curses.A_REVERSE)
            else:
                win.addstr(draw_y, draw_x, '  ')

def curses_main(stdscr):
    win = curses.newwin(WIN_HEIGHT, WIN_WIDHT)
    win.noutrefresh()

    sjis_str = u'遥か３８万キロのボヤージュ.mp3'.encode('shift-jis')

    fm = FontManager.FontManager(font4x8_file='./font/misaki_4x8_jisx0201.fnt',
                                 font8x8_file='./font/misaki_gothic.fnt')
    bitmap = fm.str_to_bitmap(sjis_str)

    while True:
        begin_offset = WIN_WIDHT
        end_offset = - len(sjis_str) * 8

        for x in range(begin_offset, end_offset, -2):
            draw_bitmap(win, bitmap, x, 0, WIN_WIDHT, WIN_HEIGHT)

            win.refresh()
            curses.doupdate()

            import time
            time.sleep(0.050)

if __name__ == '__main__':
    curses.wrapper(curses_main)
