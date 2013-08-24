#!/usr/bin/env python

import curses
from curses.textpad import rectangle
from widget import Widget

class Button(Widget):
    def __init__(self, window, y, x, data, color=0):
        Widget.__init__(self, window, None, None, y, x, data, color)
        self.__active = False

        self.setdata(data)
        self.refresh()

    def setdata(self, data):
        # save the horizontal size needed in the cols variable
        self.cols = len(data) + 3
        Widget.setdata(self, data)
        self.refresh()

    def refresh(self):
        """
        Redraw button based on active or inactive state.
        """
        if self.__active:
            self.window.addstr(self.y, self.x, "[")
            self.window.addstr(self.y, self.x+self.cols, "]")
            self.window.addstr(self.y, self.x+2, self.data, curses.A_REVERSE)
        else:
            self.window.addstr(self.y, self.x, "<")
            self.window.addstr(self.y, self.x+self.cols, ">")
            self.window.addstr(self.y, self.x+2, self.data)
        Widget.refresh(self)

    def focus(self):
        self.__active = True
        self.refresh()

        # hide cursor if shown
        try:
            curses.curs_set(0) # hide cursor
        except:
            pass

        while 1:
            # enable interpreted escape character sequences
            self.window.keypad(1)

            # get key press (non-blocking)
            key = self.window.getch()
            # return false on tab, true on enter
            if key == 9:
                pressed = False
                break
            elif key == 10:
                pressed = True
                break

            curses.napms(50)

        self.__active = False
        self.refresh()
        return pressed

if __name__ == "__main__":
    def main(stdscr):
        try:
            curses.use_default_colors()
            curses.init_pair(1, -1, curses.COLOR_CYAN)
            curses.init_pair(2, -1, curses.COLOR_BLUE)
        except:
            pass

        # add some numbers to background so we can see window
        for y in range(0, curses.LINES - 1):
            for x in range(0, curses.COLS):
                stdscr.addstr("%d" % ((y + x) % 10))
        stdscr.addstr(curses.LINES - 1, 0, "Press tab to select.")
        stdscr.refresh()

        win = stdscr.subwin(22,50,5,5)
        win.bkgdset(ord(' '), curses.color_pair(1))
        win.clear()
        win.border()
        win.addstr(0, 2, "[ Window with an embedded Button ]")

        button1 = Button(win, 4, 4, "Quit")
        button2 = Button(win, 6, 4, "Stay")

        while 1:
            if button1.focus():
                break
            button2.focus()


    # initiate curses wrapper
    curses.wrapper(main)
