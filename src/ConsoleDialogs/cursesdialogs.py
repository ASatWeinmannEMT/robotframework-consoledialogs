# -*- coding: utf-8 -*-
"""
============================
ConsoleDialogs.cursesdialogs
============================

curses based dialogs
"""
from curses import (wrapper, curs_set, KEY_RESIZE, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
                    A_REVERSE, init_pair, color_pair, COLOR_RED, COLOR_GREEN, COLOR_BLACK,
                    COLOR_WHITE, COLOR_BLUE)
from ConsoleDialogs.cursesutils import addstr_wordwrap, CustomTextBox
from math import ceil, floor
import os

# Set NCURSES_NO_UTF8_ACS environment variable to ensure
# ncurses displays the correct special characters (borders etc)
os.environ["NCURSES_NO_UTF8_ACS"] = "1"

BORDER_WIDTH = 1
STDSCR_MIN_HEIGHT = 2 * BORDER_WIDTH
STDSCR_MIN_WIDTH = (2 * BORDER_WIDTH)


COLOR_PAIR_GREEN_ON_BLACK = 1
COLOR_PAIR_RED_ON_BLACK = 2
COLOR_PAIR_WHITE_ON_BLUE = 3


class CursesDialog(object):

    def show(self):
        wrapper(self.draw)

    def draw(self, stdscr):

        # Setup colors
        init_pair(COLOR_PAIR_GREEN_ON_BLACK, COLOR_GREEN, COLOR_BLACK)
        init_pair(COLOR_PAIR_RED_ON_BLACK, COLOR_RED, COLOR_BLACK)
        init_pair(COLOR_PAIR_WHITE_ON_BLUE, COLOR_WHITE, COLOR_BLUE)

        self.exit = False
        while not self.exit:
            stdscr.clear()
            stdscr.border()
            curs_set(0)
            height, width = stdscr.getmaxyx()

            # Populate content
            if height > STDSCR_MIN_HEIGHT and width > STDSCR_MIN_WIDTH:
                sw_h = height - STDSCR_MIN_HEIGHT
                sw_w = width - STDSCR_MIN_WIDTH
                subwin = stdscr.derwin(sw_h, sw_w, BORDER_WIDTH, BORDER_WIDTH)
                self._draw_content(subwin, sw_w, sw_h)
            stdscr.refresh()

            # Wait for key
            k = stdscr.getch()
            if k != KEY_RESIZE:
                self._handle_key(k)

    def _handle_key(self, k):
        if k == 10:
            self._exit()

    def _draw_content(self, scr, width, height):
        pass

    def _exit(self):
        self.exit = True


class CursesMessageDialog(Dialog):
    def __init__(self, message):
        self.message = message

    def _draw_content(self, scr, width, height):
        # Pre-condition: width >= 1, height >= 1

        # Draw message
        if height > 1:
            text_win = scr.derwin(height - 1, width, 0, 0)
            addstr_wordwrap(text_win, self.message)

        # Draw OK button
        scr.addstr(height - 1, int(width * 0.5), "OK", A_REVERSE)


class CursesPassFailDialog(Dialog):
    def __init__(self, message):
        self.message = message
        self.result = False
        self.selected_button = 0

    def _draw_content(self, scr, width, height):
        # Pre-condition: width >= 1, height >= 1

        # Draw message
        if height > 1:
            text_win = scr.derwin(height - 1, width, 0, 0)
            addstr_wordwrap(text_win, self.message)

        # Draw PASS button
        flags = A_REVERSE if self.selected_button == 0 else 0
        scr.addstr(height - 1, int(width * 0.25), "PASS", flags | color_pair(COLOR_PAIR_GREEN_ON_BLACK))

        # Draw FAIL button
        flags = A_REVERSE if self.selected_button == 1 else 0
        scr.addstr(height - 1, int(width * 0.75), "FAIL", flags | color_pair(COLOR_PAIR_RED_ON_BLACK))

    def get_result(self):
        return self.result

    def _handle_key(self, k):
        if k == 10:
            # Set result and exit
            self.result = (self.selected_button == 0)
            self._exit()
        elif k == int(KEY_LEFT):
            if self.selected_button == 1:
                self.selected_button = 0
        elif k == int(KEY_RIGHT):
            if self.selected_button == 0:
                self.selected_button = 1


class CursesInputDialog(Dialog):
    def __init__(self, message, default, hidden=False):
        self.message = message
        self.hidden = hidden
        self.selected_button = 0
        self.textbox = CustomTextBox(default_string=default)
        self.textbox.set_enable(True)

    def _draw_content(self, scr, width, height):
        # Pre-condition: width >= 1, height >= 1

        # Draw message
        if height > 2:
            text_win = scr.derwin(int(floor(height / 2)), width, 0, 0)
            addstr_wordwrap(text_win, self.message)

        # Draw text edit box
        if height > 1:
            textbox_win = scr.subpad(int(ceil(height / 2)) - 1, width, int(ceil(height / 2)), 0)
            textbox_win.attrset(color_pair(COLOR_PAIR_WHITE_ON_BLUE))
            self.textbox.draw(textbox_win)

        # Draw OK button
        flags = A_REVERSE if self.selected_button == 1 else 0
        scr.addstr(height - 1, int(width * 0.5), "OK", flags)

    def get_result(self):
        return self.textbox.get_string()

    def _handle_key(self, k):
        if k == 10:
            if self.selected_button == 1:
                self._exit()
            else:
                self.selected_button = 1
        elif k == int(KEY_DOWN):
            if self.selected_button == 0:
                self.selected_button = 1
                self.textbox.set_enable(False)
        elif k == int(KEY_UP):
            if self.selected_button == 1:
                self.selected_button = 0
                self.textbox.set_enable(True)
        else:
            if self.selected_button == 0:
                self.textbox.handle_key(k)
