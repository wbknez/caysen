"""
Contains all major sub-systems (audio, input, and video) as well as a simple
kernel to manage them.
"""
from abc import ABCMeta, abstractmethod

import tdl


class SubSystem(metaclass=ABCMeta):
    """
    Represents a simple mechanism for creating and managing re-usable system
    resources and executing common tasks.

    Attributes:
        name (str): The name of the sub-system for identification purposes.
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_dependencies(self):
        """
        Returns a list of other sub-systems this sub-system dependes on for
        both initialization and updates.

        Put more clearly, every dependency for each execution - either
        one-time initialization or repeated updates - must be initialized or
        updated before this sub-system may do the same.

        :return: A dict of initialization and update dependencies.
        """
        pass

    @abstractmethod
    def initialize(self, params):
        """
        Initializes this sub-system and acquires all system resources that
        are necessary for successful operation.

        :param params: A dictionary of user-modified parameters.
        :return: False if unsuccessful, otherwise True.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Shuts down this sub-system and frees all system resources it is
        currently using.

        :return: False if unsuccessful, otherwise True.
        """
        pass

    @abstractmethod
    def update(self, delta_time):
        """
        Updates this sub-system in some way.

        :param delta_time: The amount of time in milliseconds that has passed
        since the previous update.
        :return: False if unsuccessful, otherwise True.
        """
        pass


class DisplaySubSystem(SubSystem):
    """
    An implementation of SubSystem that manages a console window that is used as
    an ASCII-capable rendering surface.

    To prevent tearing, this implementation uses an additional offscreen
    console that is, once per frame, blit to the main window via an update
    function.

    Attributes:
        back (tdl.Console): The back buffer used as an offscreen display; all
        rendering calls are written here before being blitted to the main
        display.
        console (tdl.Console): Main display.
        font (str): Path to the bitmap font used for text presentation on a
        console.
        fps (int): The frames per second to limit the display to.
        fullscreen (bool): Whether or not the display is consumes the entire
        screen.
        height (int): The number of rows in the display console.
        title (str): The title to use for the display console.
        width (int): The number of columns in the display console.
    """

    def __init__(self):
        super().__init__("display")
        self.back = None
        self.console = None
        self.font = None
        self.fps = 20
        self.fullscreen = False
        self.height = 0
        self.title = ""
        self.width = 0

    def clear(self, x, y):
        """
        Clears the character located at the specified x- and y-axis
        coordinates by, essentially, inserting a space in its place.

        Note that this is applied to the back buffer, so a call to update()
        must occur before these changes are visualized to the user.

        :param x: The x-axis coordinate of the tile to clear.
        :param y: The y-axis coordinate of the tile to clear.
        """
        self.back.draw_char(x, y, ' ', bg=None)

    def clear_all(self):
        """
        Clears the entire visual display.

        Note that this is applied to the back buffer, so a call to update()
        must occur before these changes are visualized to the user.
        """
        self.back.clear()

    def draw(self, x, y, char, fg=(255, 255, 255), bg=None):
        """
        Draws the specified character to the screen at the specified
        x- and y-axis coordinates and with the specified foreground and
        background colors.

        Note that this is applied to the back buffer, so a call to update()
        must occur before these changes are visualized to the user.

        :param x: The x-axis coordinate of the tile to draw on.
        :param y: The y-axis coordinate of the tile to draw on.
        :param char: The ASCII symbol to use as the foreground character.
        :param fg: The foreground color.
        :param bg: The background color.
        """
        self.back.draw_char(x, y, char, fg, bg)

    def get_dependencies(self):
        return {"init": [], "update": ["input"]}

    def initialize(self, params):
        self.fullscreen = params.get("fullscreen", False)
        self.font = params.get("font", None)
        self.height = params.get("height", 50)
        self.title = params.get("title", "Caysen City")
        self.width = params.get("width", 80)

        if self.font is not None:
            greyscale = params.get("font.greyscale", True)
            alt_layout = params.get("font.altLayout", False)

            tdl.set_font(self.font, greyscale, alt_layout)

        self.back = tdl.Console(self.width, self.height)
        self.console = tdl.init(self.width, self.height, title=self.title,
                                fullscreen=self.fullscreen)
        tdl.set_fps(self.fps)
        return self.console is not None

    def set_fullscreen(self, fullscreen):
        """
        Sets whether or not to make the display fullscreen.

        :param fullscreen: Whether or not to make the display fullscreen.
        """
        if self.fullscreen is not fullscreen:
            self.fullscreen = fullscreen
            tdl.set_fullscreen(self.fullscreen)

    def shutdown(self):
        if self.console is not None:
            del self.console
        return True

    def update(self, delta_time):
        self.console.blit(self.back, 0, 0, self.width, self.height, 0, 0)
        tdl.flush()
        return not tdl.event.is_window_closed()


class InputSubSystem(SubSystem):
    """
    An implementation of SubSystem that manages the event queue of keyboard
    and mouse input events and responds to each by either calling a
    user-created callback function, if bound, otherwise discarding it.

    Attributes::

    """

    def __init__(self):
        super().__init__("input")

    def get_dependencies(self):
        return {"init": ["display"], "update": []}

    def initialize(self, params):
        pass

    def shutdown(self):
        pass

    def update(self, delta_time):
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                pass
            elif event.type == 'KEYUP':
                pass
            elif event.type == 'MOUSEDOWN':
                pass
            elif event.type == 'MOUSEMOTION':
                pass
            elif event.type == 'MOUSEUP':
                pass
            elif event.type == 'QUIT':
                return False
        return True
