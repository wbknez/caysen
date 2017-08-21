"""
Contains the implementation of the display framework using TDL.
"""
import tdl

from caysen.kernel import SubSystem


class Canvas:
    """
    Represents a single, unique surface that corresponds to a console on which
    ASCII characters may be drawn.

    Attributes:
        name (str): The unique name for the canvas.
        console (tdl.Console): The backing TDL console.
        height (int): The height of the canvas in tiles.
        width (int): The width of the canvas in tiles.
    """

    def __init__(self, name, width, height):
        """
        Constructor.

        :param name: The unique name to use.
        :param width: The width of the backing console.
        :param height: The height of the backing console.
        """
        self.name = name
        self.console = tdl.Console(width, height)
        self.height = height
        self.width = width

    def blit(self, image, x=0, y=0):
        """
        Blits the specified image onto this canvas.

        :param image: The image to use.
        :param x: The x-axis coordinate
        :param y: The y-axis coordinate
        """
        image.blit(self.console, x, y)

    def blit2x(self, image, x=0, y=0):
        """
        Blits the specified image onto this canvas at half its resolution.

        :param image: The image to use.
        :param x: The x-axis coordinate
        :param y: The y-axis coordinate
        """
        image.blit_2x(self.console, x, y)

    def contains(self, point):
        """
        Determines whether or not the specified point, given as a pair of
        coordinates in x-y space, is contained within the bounds of this
        canvas' console.

        :param point: The point to check.
        :return: True if the point is within the console bounds, otherwise
        False.
        """
        return point in self.console

    def dispose(self):
        """
        Destroys the TDL console.

        This function should only be called once the instance of this canvas
        is no longer needed, as there is no way to re-initialize the backing
        console.
        """
        if self.console:
            del self.console

    def draw(self, x, y, char=None, fg=(255, 255, 255), bg=None):
        """
        Draws the specified character on this canvas at the specified
        x- and y-axis coordinates and with the specified color attributes.

        :param x: The x-axis coordinate of the tile to draw on.
        :param y: The y-axis coordinate of the tile to draw on.
        :param char: The ASCII symbol to use as the foreground character.
        :param fg: The foreground color.
        :param bg: The background color.
        """
        self.console.draw_char(x, y, char, fg, bg)

    def erase(self, x, y):
        """
        Clears the character located at the specified x- and y-axis
        coordinates on this canvas by, essentially, inserting a space in its
        place.

        :param x: The x-axis coordinate of the tile to clear.
        :param y: The y-axis coordinate of the tile to clear.
        """
        self.console.draw_char(x, y, ' ', bg=None)

    def fill(self, x, y, width=None, height=None, char=None,
             fg=(255, 255, 255), bg=None):
        """
        Draws a filled rectangle on this canvas at the specified x- and y-axis
        coordinates and with the specified width, height, and color
        attributes and with the specified character, if any.

        :param x: The x-axis coordinate of the tile to draw on.
        :param y: The y-axis coordinate of the tile to draw on.
        :param width: The width of the filled rectangle to draw.
        :param height: The height of the filled rectangle to draw.
        :param char: The ASCII symbol to use as a foreground character.
        :param fg: The background color.
        :param bg: The foreground color.
        """
        self.console.draw_rect(x, y, width, height, char, fg, bg)

    def outline(self, x, y, width=None, height=None, char=None,
                fg=(255, 255, 255), bg=None):
        """
        Draws a rectangular outline on this canvas at the specified x- and
        y-axis coordinates and with the specified width, height, and color
        attributes and with the specified character, if any.

        :param x: The x-axis coordinate of the tile to draw on.
        :param y: The y-axis coordinate of the tile to draw on.
        :param width: The width of the outline to draw.
        :param height: The height of the outline to draw.
        :param char: The ASCII symbol to use as a border.
        :param fg: The background color.
        :param bg: The foreground color.
        """
        self.console.draw_frame(x, y, width, height, char, fg, bg)

    def wipe(self):
        """
        Clears the entirety of this canvas.
        """
        self.console.clear()

    def write(self, x, y, msg, fg=(255, 255, 255), bg=None):
        """
        Draws the specified message on this canvas at the specified x- and
        y-axis coordinates and with the specified color attributes.

        :param x: The x-axis coordinate of the tile to start writing on.
        :param y: The y-axis coordinate of the tile to start writing on.
        :param msg: The message to write.
        :param fg: The foreground color.
        :param bg: The background color.
        """
        self.console.draw_str(x, y, msg, fg, bg)


class DisplaySubSystem(SubSystem):
    """
    An implementation of SubSystem that manages a console window that is used as
    an ASCII-capable rendering surface.

    To prevent tearing, this implementation uses an additional offscreen
    console that is, once per frame, blit to the main window via an update
    function.  All users should draw to the offscreen buffer only.

    Attributes:
        canvas (Canvas): The backbuffer.
        font (str): The path to a bitmap font file.
        fps (int): The maximum frames per second to render the display at.
        fullscreen (bool): Whether or not the display takes up the entire
        desktop.
        height (int): The height of the display in tiles.
        root (tdl.Console): The main display window.
        width (int): The width of the display in tiles.
    """

    def __init__(self):
        super().__init__("display")
        self.canvas = None
        self.font = None
        self.fps = 0
        self.fullscreen = False
        self.height = 0
        self.root = None
        self.width = 0

    def get_dependencies(self):
        return {"init": [], "update": [], "shutdown": []}

    def initialize(self, params, kernel):
        self.fullscreen = params.get("fullscreen", False)
        self.font = params.get("font", None)
        self.height = params.get("height", 50)
        self.title = params.get("title", "Caysen City")
        self.width = params.get("width", 80)

        if self.font is not None:
            greyscale = params.get("font.greyscale", True)
            alt_layout = params.get("font.altLayout", False)

            tdl.set_font(self.font, greyscale, alt_layout)

        self.canvas = Canvas("backbuffer", self.width, self.height)
        self.root = tdl.init(self.width, self.height, title=self.title,
                             fullscreen=self.fullscreen)
        return self.root is not None

    def set_fullscreen(self, fullscreen):
        """
        Sets whether or not the display is fullscreen.

        :param fullscreen: Whether or not to make the display fullscreen.
        """
        if self.fullscreen is not fullscreen:
            self.fullscreen = fullscreen
            tdl.set_fullscreen(self.fullscreen)

    def update(self, delta_time):
        self.root.blit(self.canvas.console, 0, 0, self.width, self.height, 0, 0)
        tdl.flush()
        return not tdl.event.is_window_closed()

    def shutdown(self):
        self.canvas.dispose()

        if not self.root is None:
            del self.root
        return True
