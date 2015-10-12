#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import curses

CH_NUM_IN_LINE = 94
CH_BYTE_SIZE = 8

CH_HEIGHT = 8
CH_WIDTH  = 8

def char_to_index(font, ch_x, ch_y):
    return (ch_y * CH_NUM_IN_LINE + ch_x) * CH_BYTE_SIZE

def draw_char(stdscr, font, base_x, base_y, ch_x, ch_y):
    for x in range(CH_WIDTH):
        index = x + char_to_index(font, ch_x, ch_y)
        for y in range(CH_HEIGHT):
            if font[index] & (1<<y):
                str = 'X'
            else:
                str = ' '
            stdscr.addstr(base_y + y, base_x + x, str)

def curses_main(stdscr):
    font = np.fromfile('./font/misaki_gothic.fnt', dtype=np.uint8)

    # Test
    draw_char(stdscr, font, 0+8*0, 0, 1, 3)
    draw_char(stdscr, font, 0+8*1, 0, 2, 3)
    draw_char(stdscr, font, 0+8*2, 0, 3, 3)
    draw_char(stdscr, font, 0+8*3, 0, 4, 3)
    draw_char(stdscr, font, 0+8*4, 0, 5, 3)
    draw_char(stdscr, font, 0+8*5, 0, 6, 3)
    draw_char(stdscr, font, 0+8*6, 0, 7, 3)
    draw_char(stdscr, font, 0+8*7, 0, 8, 3)

    stdscr.getch()
    stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(curses_main)
