#!/usr/bin/env python

import curses
from curses.textpad import rectangle
from widget import Widget

class EditBox(Widget):
    """
    A single line edit box for use in dialogs.
    Can be customized with color and borders.
    """
    def __init__(self, window, cols, y, x, data, color=0):
        Widget.__init__(self, window, None, cols, y, x, data, color)

        self.__border = False

        self.__derwin = self.window.derwin(1, self.cols, self.y, self.x)
        self.__derwin.bkgdset(ord(' '), curses.color_pair(self.color_pair))

        self.setdata(data)

        self.refresh()

    def setdata(self, data):
        """
        Set the data for the EditBox.
        """
        self.__tb = curses.textpad.Textbox(self.__derwin)

        for ch in data.ljust(self.cols):
            self.__tb.do_command(ch)

        self.__tb.do_command(ord(curses.ascii.ctrl('a')))
        Widget.setdata(self, data)

    def setcolor(self, color_pair):
        """
        Set the curses color pair that should be used for drawing to the window.
        """
        Widget.setcolor(self, color_pair)
        # refresh the data when we change the color
        Widget.setdata(self, data)

    def addborder(self):
        """
        Adds a border around the EditBox. Uses space outside the coordinates
        given in constructor.
        """
        self.__border = True
        self.refresh()

    def refresh(self):
        """
        Redraw border for EditBox and command an underlying window refresh.
        """
        if self.__border:
            rectangle(self.window, self.y-1, self.x-1, self.y+1, self.x+self.cols)
        Widget.refresh(self)

    def focus(self):
        """
        Give EditBox focus to process input events. Loop exits with Enter or
        Tab.
        """
        self.refresh()

        # restore cursor if hidden
        try:
            curses.curs_set(1) # show cursor
        except:
            pass

        def handlekey(key):
            """
            Provides special case handling of key events for the Textbox loop.
            Any unhandled cases should be passed through so Textbox can process
            them.
            """
            if key == 127: # convert backspace into CTRL-H
                return ord(curses.ascii.ctrl('h'))
            elif key == 9: # lose focus on tab, send terminate to Textbox
                return ord(curses.ascii.ctrl('g'))
            else:
                return key

        # give Textbox control of the loop, Tb will call handlekey for each keypress
        self.__tb.edit(handlekey)

        # get data from Textbox and return
        return self.__tb.gather()


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
        stdscr.addstr(curses.LINES - 1, 0, "Press tab to quit.")
        stdscr.refresh()

        win = stdscr.subwin(22,50,5,5)
        win.bkgdset(ord(' '), curses.color_pair(1))
        win.clear()
        win.border()
        win.addstr(0, 2, "[ Window with an embedded EditBox ]")

        edit1 = EditBox(win, 10, 3, 3, "test1")
        #edit1.addborder()

        edit2 = EditBox(win, 12, 6, 3, "test2", 1)
        edit2.addborder()

        edit3 = EditBox(win, 14, 9, 3, "test3", 2)
        edit3.addborder()

        data1 = edit1.focus()
        data2 = edit2.focus()
        data3 = edit3.focus()

        win.erase()
        stdscr.clear()

        stdscr.addstr(10,10, "Entered text 1: %s" % data1)
        stdscr.addstr(12,10, "Entered text 2: %s" % data2)
        stdscr.addstr(14,10, "Entered text 3: %s" % data3)
        stdscr.getch()

    # initiate curses wrapper
    curses.wrapper(main)
