


class Widget():
    """
    Base class for Widgets in the PyCursesLib library
    """
    def __init__(self, window, rows, cols, y, x, data=None, color=0):
        self.window = window
        self.data = data
        self.color_pair = color
        self.y, self.x = (y, x)
        self.rows = rows
        self.cols = cols

    def setdata(self, data):
        """
        Assign user data to base class.
        """
        self.data = data

    def refresh(self):
        """
        Call a refresh on the base class window object.
        """
        self.window.refresh()

    def focus(self):
        """
        The main entry point for derived widgets. Process input and give up
        focus.
        """
        pass

    def setcolor(self, color_pair):
        """
        Set the curses color pair that should be used for drawing to the window.
        """
        self.color_pair = color_pair
