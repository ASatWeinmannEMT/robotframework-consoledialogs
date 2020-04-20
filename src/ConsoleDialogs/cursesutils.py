import curses
import curses.ascii
from curses import A_UNDERLINE

class WindowFullException(Exception):
    pass


def calc_wordwrap_lines(s, width):
    # Split string into list of words
    word_list = s.split()

    # Line-based loop
    y = 0
    w = 0
    while True:
        width_sum = 0
        while w < len(word_list):
            word = word_list[w]
            if (width_sum + len(word)) >= width:
                break
            width_sum += len(word)

            if width_sum + 1 < width:
                width_sum += 1
            w += 1

        if w >= len(word_list):
            break
        y = y + 1

    # Return the actual number of lines needed
    return y


def addstr_charwrap(window, s, cursorpos=None, mode=0, halign=0, fail_on_window_full=False):

    (height, width) = window.getmaxyx()

    # Char-based loop
    y = 0
    c = 0
    while y < height:
        x = 0
        while x < width and c < len(s):
            flags = A_UNDERLINE if c == cursorpos else 0
            window.addch(y, x, s[c], flags)
            c += 1
            x += 1
        y += 1

        if c >= len(s):
            break


def addstr_wordwrap(window, s, mode=0, halign=0, fail_on_window_full=False):
    """ (cursesWindow, str, int, int, int, bool) -> None

    Add a string to a curses window. If mode is given
    (e.g. curses.A_BOLD), then format text accordingly. We do very
    rudimentary wrapping on word boundaries.

    """
    (height, width) = window.getmaxyx()

    # Split string into list of words
    word_list = s.split()

    # Line-based loop
    y = 0
    x = 0
    w = 0
    while w < len(word_list):
        if x + (len(word_list[w]) + 1) >= width:
            y += 1
            x = 0
            if y >= height:
                # No more lines to add
                break

        window.addstr(y, x, word_list[w], mode)
        x += len(word_list[w])
        window.addstr(y, x, ' ', mode)
        x += 1
        w += 1

    if fail_on_window_full and y >= height and w < len(word_list):
        # Haven't managed to fit all of the text into the window
        raise WindowFullException()

    # Return the actual number of lines we rendered
    return y + 1


def insert_str(string, ch, index):
    return string[:index] + chr(ch) + string[index:]


class CustomTextBox:
    """Editing widget using the interior of a window object.
    """
    def __init__(self, default_string="", hidden=False):
        self.string = default_string
        self.cursorpos = len(self.string)
        self.enable = False
        self.hidden = hidden

    def handle_key(self, k):
        if not self.enable:
            return

        ch = int(k)
        if curses.ascii.isprint(ch):
            if self.cursorpos <= len(self.string):
                self.string = insert_str(self.string, ch, self.cursorpos)
                self.cursorpos += 1
        elif ch in (curses.KEY_LEFT, curses.ascii.BS, curses.KEY_BACKSPACE):
            if self.cursorpos > 0:
                self.cursorpos = self.cursorpos - 1
                if ch in (curses.ascii.BS, curses.KEY_BACKSPACE):
                    self.string = self.string[:self.cursorpos] + self.string[(self.cursorpos + 1):]
        elif ch == curses.KEY_RIGHT:
            if self.cursorpos < len(self.string):
                self.cursorpos += 1
        elif ch == curses.KEY_DC:
            self.string = self.string[:self.cursorpos] + self.string[(self.cursorpos + 1):]
        elif ch == curses.KEY_HOME:
            self.cursorpos = 0
        elif ch == curses.KEY_END:
            self.cursorpos = len(self.string)

    def set_enable(self, enable):
        self.enable = enable
        self.cursorpos = len(self.string)

    def get_string(self):
        return self.string

    def draw(self, win):
        disp_str = self.string
        if self.hidden:
            disp_str = '*' * len(self.string)

        cp = self.cursorpos if self.enable else None
        addstr_charwrap(win, disp_str, cp)
