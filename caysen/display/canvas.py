"""
Contains
"""
import tdl


class Canvas:
    """"
    """

    def __init__(self, name, width, height):
        self.name = name
        self.console = tdl.Console(width, height)

    def clear(self, x, y):
        """
        Clears the character located at the specified x- and y-axis
        coordinates on this canvas by, essentially, inserting a space in its
        place.

        :param x: The x-axis coordinate of the tile to clear.
        :param y: The y-axis coordinate of the tile to clear.
        """
        self.console.draw_char(x, y, ' ', bg=None)

    def dispose(self):
        """
        Destroys the TDL console.
        """
        if self.console:
            del self.console

    def draw(self, x, y, char, fg=(255, 255, 255), bg=None):
        """
        Draws the specified character to the screen at the specified
        x- and y-axis coordinates and with the specified foreground and
        background colors.

        :param x: The x-axis coordinate of the tile to draw on.
        :param y: The y-axis coordinate of the tile to draw on.
        :param char: The ASCII symbol to use as the foreground character.
        :param fg: The foreground color.
        :param bg: The background color.
        """
        self.console.draw_char(x, y, char, fg, bg)

    def wipe(self):
        """
        Clears the entirety of this canvas.
        """
        self.console.clear(bg=None)

    def write(self, x, y, msg, fg=(255, 255, 255), bg=None):
        """

        :param x: The x-axis coordinate of the tile to start writing on.
        :param y: The y-axis coordinate of the tile to start writing on.
        :param msg: The message to write.
        :param fg: The foreground color.
        :param bg: The background color.
        """
        self.console.draw_str(x, y, msg, fg, bg)
