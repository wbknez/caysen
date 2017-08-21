"""

"""
from abc import ABCMeta, abstractmethod

from caysen.kernel import SubSystem


class GameState(metaclass=ABCMeta):
    """
    Represents a single piece of reusable game-specific functionality.

    Attributes:
        name (str): A unique name.
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def dispose(self):
        """
        Releases all resources this game state has acquired.
        """
        pass

    @abstractmethod
    def draw(self, canvas):
        """
        Draws this game state to the specified canvas.

        :param canvas: The canvas to draw to.
        """
        pass

    @abstractmethod
    def enter(self):
        """
        Signifies a transition to this game state from another.
        """
        pass

    @abstractmethod
    def exit(self):
        """
        Signifies a transition from this game state to another.
        """
        pass

    @abstractmethod
    def initialize(self):
        """
        Creates or otherwise initializes any resources this game state needs
        in order to operate effectively.
        """
        pass

    @abstractmethod
    def update(self, delta_time, stack):
        """
        Updates this game state in some way.

        The return value for this function indicates modality.  If this
        function returns True, then all other states below this one on the
        state stack will not be updated; True indicates the opposite.  This
        is useful, for example, for displaying modal message boxes, such as a
        tutorial, on top of a temporarily frozen game map.  An example of the
        alternative would be a player accessing an in-game menu, such as the
        inventory screen, in real-time while the rest of the game continues.

        :param delta_time: The amount of time in seconds that has passed
        since the previous update.
        :param stack: The game state stack that requested the update.
        :return: True if other states should also be updated, otherwise False.
        """
        return False


class GameStateStack:
    """
    Represents

    The game subsystem explicitly checks whether or not there are any states
    to update (and therefore draw) to decide when the game is over and the
    application should terminate.  As such,

    Attributes:
        stack (list):
    """

    def __init__(self):
        self.stack = list()

    def pop(self, state):
        """


        :param state:
        """
        if not self.stack:
            raise ValueError("The state stack is currently empty.")
        assert self.stack[-1] == state
        prev = self.stack.pop(-1)
        prev.exit()

    def push(self, state):
        """

        :param state:
        """
        pass

    def quit(self):
        """
        Removes any game states from this game state stack.

        As stated earlier, because the game subsystem checks to see if any
        game states are on the stack in order to determine exit status,
        calling this function will effectively terminate the application.
        """
        self.stack.clear()

    def slide(self, current, next):
        """

        :param current:
        :param next:
        :return:
        """
        pass

    def update(self, delta_time):
        """

        :param delta_time:
        """
        for state in reversed(self.stack):
            if not state.update(delta_time):
                break


class GameSubSystem(SubSystem):
    """

    """

    def __init__(self):
        super().__init__("game")

    def get_dependencies(self):
        return {"init": [], "update": [], "shutdown": []}

    def initialize(self, params, kernel):
        return True

    def shutdown(self):
        return True

    def update(self, delta_time):
        return True
