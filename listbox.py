#!/usr/bin/env python

import curses
import curses.ascii
from curses.textpad import rectangle
from widget import Widget

class ListBox(Widget):
    """
    Implements a listbox control using curses.
    Instantiation requires a parent curses window to draw on, desired
    coordinates for the listbox, and a Python list of data to display.
    """
    def __init__(self, window, rows, cols, y, x, data, color=0):
        Widget.__init__(self, window, rows, cols, y, x, data, color)

        self.__cursor_idx = 0
        self.__data_idx = 0
        self.__page_offset = 0
        # the max index that can be shown in listbox (back out borders and zero)
        self.__max_box_idx = self.rows-3

        self.setdata(data) # calls refresh()

    def setcolor(self, color_pair):
        """
        Set the curses color pair that should be used for drawing to the window.
        """
        Widget.setcolor(self, color_pair)
        # refresh the data when we change the color
        self.setdata(self.data)

    def refresh(self):
        """
        Redraw the ListBox on the screen.
        """
        # draw list bounding box
        curses.textpad.rectangle(self.window, self.y, self.x, self.y+self.rows-1, self.x+self.cols-1)

        # draw visible portion of list box data
        self.__listwin.overwrite(self.window, self.__page_offset, 0, self.y+1, self.x+1, self.y+self.rows-2, self.x+self.cols-2)
        Widget.refresh(self)

    def scroll(self, amount):
        """
        Scroll listbox by amount, e.g. where -1 is up by one, and +1 is down by one.
        """
        self.scrollto(self.__cursor_idx + amount)

    def scrollto(self, idx):
        """
        Scroll to a specified index in the dataset.
        """
        # clamp to max value
        if idx >= len(self.data):
            idx = len(self.data)-1
        # clamp to min value
        if idx < 0:
            idx = 0

        # figure out direction of travel to get to specified index
        if idx < self.__cursor_idx:
            # going up in list, if idx not visible, adjust offset so selection
            # is first visible
            if idx < self.__page_offset:
                self.__page_offset = idx
        else:
            # if desired index is in current view, keep current page offset,
            # otherwise, increase offset so selection is last visible
            if not (self.__page_offset + self.__max_box_idx >= idx):
                self.__page_offset = idx - self.__max_box_idx

        self.__cursor_idx = self.sethilite(idx)

        self.refresh()

    def sethilite(self, index):
        """
        Set the current hilight to the given index. Clears the highlight on
        the previous index. Returns the new index.
        """
        # note: coordinates on addnstr below are into the __listwin pad
        # clear old hilite
        self.removehilite()
        # set new hilite and return index of new hilite
        self.__listwin.addnstr(index, 0, self.data[index], self.cols-2, curses.A_REVERSE)
        return index

    def removehilite(self):
        self.__listwin.addnstr(self.__cursor_idx, 0, self.data[self.__cursor_idx], self.cols-2, curses.color_pair(self.color_pair))

    def setdata(self, data):
        """
        Update the ListBox data with the given data set.
        """
        Widget.setdata(self, data)

        # the pad is sized -1 instead of -2 (for borders) because to fill in
        # the appropriate color we need an extra column
        self.__listwin = curses.newpad(len(data), self.cols-1)
        for idx, data in enumerate(self.data):
            self.__listwin.addnstr(idx, 0, data.ljust(self.cols-2), self.cols-2, curses.color_pair(self.color_pair))

        self.refresh()

    def findidx(letter):
        """
        Returns the index of the first item in the data list starting
        with the given letter.
        """
        for idx, item in enumerate(self.data):
            if item.startswith(letter):
                return idx


    def focus(self):
        """
        Give the ListBox focus, and control over the curses input.
        """
        try:
            curses.curs_set(0) # hide cursor
        except:
            pass

        # draw hilite on current selection when given focus
        self.sethilite(self.__cursor_idx)
        self.refresh()

        while 1:
            # enable interpreted escape character sequences
            self.window.keypad(1)

            # get key press (non-blocking)
            key = self.window.getch()
            # lose focus on tab or enter
            if key in [9, 10]: break
            # handle arrows and page up/down
            elif key == curses.KEY_UP: self.scroll(-1)
            elif key == curses.KEY_DOWN: self.scroll(1)
            elif key == curses.KEY_PPAGE: self.scroll(-10)
            elif key == curses.KEY_NPAGE: self.scroll(10)
            # scroll to first item with pressed alpha key
            elif curses.ascii.isalpha(key):
                dest = findidx(chr(key))
                self.scrollto(dest)

            curses.napms(50)

        # remove hilite when we lose focus
        self.removehilite()
        self.refresh()
        # return selected item
        return self.data[self.__cursor_idx]

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
        win.addstr(0, 2, "[ Window with an embedded ListBox ]")
        win.addstr(2, 3, "Select an item then press tab to")
        win.addstr(3, 3, "send selection to parent.")

        # generate list of test data
        data = map(lambda x: chr(x)+'_test'+str(x), range(ord('a'),ord('z')))

        lb = ListBox(win, 15, 30, 5, 5, data, 2)
        selection = lb.focus()

        win.erase()

        stdscr.clear()

        stdscr.addstr(10,10, "Selected item: %s" % selection)
        stdscr.getch()

    # initiate curses wrapper
    curses.wrapper(main)
