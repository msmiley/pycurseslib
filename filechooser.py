#!/usr/bin/env python

import curses
import curses.ascii
import os

import listbox
import editbox
import button

FILE_CHOOSER_ACTION_OPEN = "open"
FILE_CHOOSER_ACTION_SAVE = "save"
FILE_CHOOSER_ACTION_SELECT_FOLDER = "folder"
FILE_CHOOSER_ACTION_CREATE_FOLDER = "mkfolder"

class FileChooser():
    def __init__(self, window, root, title="File Chooser"):
        self.__window = window
        self.__size_y, self.__size_x = self.__window.getmaxyx()
        self.__root = os.path.expanduser(root)
        self.__cwd = self.__root
        self.__title = title
        self.__action = FILE_CHOOSER_ACTION_OPEN

        self.__show_hidden = False

        self.__cursor_idx = 0

        listgen = os.walk(self.__cwd)
        [root, dirs, files] = listgen.next()
        dirs.sort()
        filelist = []
        for entry in dirs:
            if not entry.startswith('.'):
                filelist.append(entry)

        print(filelist)

        self.refresh()

        # dialog items
        self.__diredit = editbox.EditBox(self.__window, self.__size_x-4, 3, 2, self.__cwd)
        self.__filelist = listbox.ListBox(self.__window, self.__size_y-10, self.__size_x-4, 5, 2, files)
        self.__ok_button = button.Button(self.__window, self.__size_y-3, 15, "OK")
        self.__cancel_button = button.Button(self.__window, self.__size_y-3, 3, "Cancel")

    def setaction(self, action):
        if action in [FILE_CHOOSER_ACTION_OPEN,
                      FILE_CHOOSER_ACTION_SAVE,
                      FILE_CHOOSER_ACTION_SELECT_FOLDER,
                      FILE_CHOOSER_ACTION_CREATE_FOLDER]:
            self.__action = action
        else:
            raise Exception, "Invalid FileChooser action"


    def refresh(self):
        self.__window.clear()
        self.__window.border()
        self.__window.addstr(0, 2, "[ " + self.__title + " ]")

        self.__window.addstr(2, 2, "Current Path:")


    def focus(self):

        while 1:
            self.__diredit.focus()
            self.__filelist.focus()
            if self.__cancel_button.focus():
                return False, ""
            if self.__ok_button.focus():
                return True, "filename"



if __name__ == "__main__":
    def main(stdscr):
        try:
            curses.use_default_colors()
            curses.init_pair(1, -1, curses.COLOR_CYAN)
        except:
            pass

        # add some numbers to background so we can see window
        for y in range(0, curses.LINES - 1):
            for x in range(0, curses.COLS):
                stdscr.addstr("%d" % ((y + x) % 10))
        stdscr.addstr(curses.LINES - 1, 0, "Press q to quit.")

        win = stdscr.subwin(30,50,5,5)
        win.bkgdset(ord(' '), curses.color_pair(1))

        fileb = FileChooser(win, '~')
        fileb.setaction(FILE_CHOOSER_ACTION_CREATE_FOLDER)
        ok, filename = fileb.focus()

        win.erase()
        stdscr.clear()

        stdscr.addstr(10,10, "Result: %d, %s" % (ok, filename))
        stdscr.getch()


    # initiate curses wrapper
    curses.wrapper(main)
