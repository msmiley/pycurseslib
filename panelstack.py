#!/usr/bin/env python

import curses
from curses import panel


class PanelStack():
    """
    A class to make it easy to work with curses panels. The class keeps track
    of the stack of panels and provides methods to show, hide, and move the
    panels on the stack.
    """
    def __init__(self):
        self.__panels = {}
        self.__currentPanel = None

    def new(self, name, rows, cols, y, x, color_pair=0):
        """
        Create new panel with given name, of size rows-by-cols, at
        starting position y,x with color described by the given color_pair.
        A new curses window is created with a border, associated with
        the panel, and returned for further drawing.
        """
        win = curses.newwin(rows, cols, y, x)
        self.__panels[name] = panel.new_panel(win)
        if curses.has_colors():
            win.bkgdset(ord(' '), curses.color_pair(color_pair))
        else:
            win.bkgdset(ord(' '), curses.A_BOLD)
        win.clear()
        win.border()
        self.update()
        return win

    def setdata(self, name, data):
        """
        Set the user data pointer of the panel to data. Can be any Python object.
        """
        panel = self.__panels[name]
        panel.set_userptr(data)

    def getdata(self, name):
        """
        Returns the user data pointer of the panel with name.
        """
        panel = self.__panels[name]
        return panel.userptr()

    def clearwindow(self, name):
        """
        Clears the window of the panel with name and redraws the border.
        """
        win = self.__panels[name].window()
        win.clear()
        win.border()
        return win

    def update(self):
        """
        Redraw and update panels.
        """
        panel.update_panels()
        curses.doupdate()

    def show(self, name):
        """
        Show the panel with name. Brings panel to top.
        """
        panel = self.__panels[name]
        panel.show()
        self.update()

    def hide(self, name):
        """
        Hide the panel with name.
        """
        panel = self.__panels[name]
        if not panel.hidden():
            panel.hide()
            self.update()

    def toggle(self, name):
        """
        Toggle the visibility of the panel with name.
        """
        panel = self.__panels[name]
        if panel.hidden():
            panel.show()
        else:
            panel.hide()
        self.update()

    def top(self, name):
        """
        Bring the panel with name to top of stack.
        """
        panel = self.__panels[name]
        if panel.hidden():
            panel.show()
        panel.top()
        self.update()
        self.__currentPanel = name

    def bottom(self):
        """
        Send the panel with name to bottom of stack.
        """
        panel = self.__panels[self.__currentPanel]
        panel.bottom()


if __name__ == "__main__":
    def main(stdscr):
        try:
            curses.use_default_colors()
            curses.init_pair(1, -1, curses.COLOR_CYAN)
            curses.init_pair(2, -1, curses.COLOR_GREEN)
        except:
            pass

        # panel stack initialization
        stack = PanelStack()

        # add some numbers to background so we can see panels
        for y in range(0, curses.LINES - 1):
            for x in range(0, curses.COLS):
                stdscr.addstr("%d" % ((y + x) % 10))
        stdscr.addstr(curses.LINES - 1, 0, "Press q to quit.")

        # add a few panels
        win1 = stack.new('win1', 10, 20, 10, 10, 1)
        # draw something on win1, make sure this is done when win1 is on top
        win1.addstr(0,2,"Test Win1")
        win1.refresh()

        win2 = stack.new('win2', 15, 30, 15, 20, 2)
        # draw something on win2, make sure this is done when win2 is on top
        win2.addstr(0,2,"Test Win2")
        win2.refresh()

        win3 = stack.new('win3', 20, 35, 5, 25)
        # draw something on win3, make sure this is done when win3 is on top
        win3.addstr(0,2,"Test Win3")
        win3.refresh()

        while 1:
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')): break
            elif key == ord('1'):
                stack.toggle('win1')
            elif key == ord('2'):
                stack.toggle('win2')
            elif key == ord('3'):
                stack.toggle('win3')
            elif key == ord('a'):
                stack.top('win1')
            elif key == ord('b'):
                stack.top('win2')
            elif key == ord('c'):
                stack.top('win3')

            curses.napms(500)

    # initiate curses wrapper
    curses.wrapper(main)
