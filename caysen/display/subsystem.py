"""
Contains the bridge between TDL and this project's kernel system.
"""
import tdl

from caysen.display.canvas import Canvas
from caysen.kernel import SubSystem


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
        return {"init": [], "update": ["game", "input"], "shutdown": ["game"]}

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
        return tdl.event.is_window_closed()

    def shutdown(self):
        self.canvas.dispose()

        if not self.root is None:
            del self.root
        return True
