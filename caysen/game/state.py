"""

"""
from abc import ABCMeta, abstractmethod

from caysen.kernel import SubSystem, SubSystemError


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
    def initialize(self, stack):
        """
        Creates or otherwise initializes any resources this game state needs
        in order to operate effectively.

        :param stack: The game state stack that requested the initialization.
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
    Represents a mechanism to manage game states and switch between them as
    necessary.

    The game state stack represents a flattened tree view of a game's state
    any given point in time.  In particular, the game state stack handles two
    pivotal operations: horizontal and vertical state transitions.  Vertical
    transitions occur when a parent state pushes a child onto the state
    stack, thereby including both in the draw and potentially the update
    cycles.  This is useful for layering states on top of one another,
    such as an options menu overlaid on a running game map.  There is a
    second type of vertical transition whereby the child pops itself off the
    stack, returning control flow to its parent.  This is useful for
    demarcating different types of states (i.e. "menu" vs. "in-game") that
    the user should be interacting with.  Vertical transitions of either type
    are accomplished by simply using the "push" and "pop" functions of the game
    state stack.

    In contrast, horizontal transitions occur when one state pops itself off
    the stack before applying another, effectively replacing it.  This is
    useful for explicitly switching between states, such as different menus
    on a character screen.  Because "switch" has programmatic connotations,
    horizontal transitions are accomplished using the "slide" function,
    which will take care of calling the appropriate "enter" and "exit"
    functions for each state.  A horizontal transition is essentially a
    re-parenting operation.

    The game subsystem explicitly checks whether or not there are any states
    to update (and therefore draw) to decide when the game is over and the
    application should terminate.  As such, while the "quit" function serves
    as a way to exit the application, there is otherwise no explicit "kill
    all" type function.

    Finally, please note that this game state stack implementation is
    singular in both nature and purpose.  That is, an enterprising programmer
    might create a state stack that is a collection of stacks, essentially
    allowing multiple state stacks to run simultaneously.  Whether or not
    this might be beneficial is for the reader to decide, but is not used
    here.  However, more importantly, this game state stack does not allow
    in-place swapping All operations occur at the head of the stack,
    never anywhere else.  Thus, it is impossible to, for example,
    swap parents and still preserve the order of any children.  Again,
    this might be useful in some circumstances but this project has nome such.

    Attributes:
        stack (list): The current state stack represented as a list, the last
        element of which is the top-most game state.
        states (dict): A dictionary of game states associated by name.
    """

    def __init__(self):
        self.stack = list()
        self.states = dict()

    def add(self, state, name=None, call_init=True):
        """
        Adds the specified game state to this game state stack with the
        specified alternate name before initializing it if necessary.

        :param state: The game state to add.
        :param name: An alternative name for the state; this allows two or
        more game states of the same type to coexist in this game state stack.
        """
        if name is None:
            name = state.name
        self.states[name] = state
        if call_init:
            self.states[name].init(self)

    def dispose(self):
        """
        Releases all of the resources held
        """
        self.stack.clear()
        for state in self.states.values():
            state.dispose()

    def draw(self, canvas):
        """
        Draws every game state in this game state stack, starting with the
        "bottom" or furtherest down.

        Because this function draws from the bottom up, there is no way to
        prevent parent game states from rendering themselves.  Technically,
        it would be more in-line to mirror the "update" function and allow
        top game states to determine whether or not those below them should
        be drawn.  However, that places an obnoxious burden on all game
        states to correctly know all contexts in which they will be used.  As
        such, this project does not support that and instead all active game
        states are given a chance to present themselves.

        Finally, game states are drawn from the bottom up (as opposed to the
        other way around in traditional 3D rendering systems due to alpha
        and depth testing) because TDL does not support console layering.

        :param canvas: The canvas to draw on.
        """
        for state in self.states:
            state.draw(canvas)

    def pop(self, state):
        """


        :param state:
        """
        if not self.stack:
            raise ValueError("The state stack is currently empty.")
        assert self.stack[-1] == state
        prev = self.stack.pop(-1)
        prev.exit()

    def push(self, state, call_parent=True):
        """


        :param state:
        :param call_parent:
        """
        if call_parent:
            self.stack[-1].exit()
        self.stack.append(state)
        state.enter()

    def quit(self):
        """
        Removes all game states from this game state stack.

        As stated earlier, because the game subsystem checks to see if any
        game states are on the stack in order to determine exit status,
        calling this function will effectively terminate the application.
        """
        self.stack.clear()

    def remove(self, name):
        """
        Removes the game state with the specified name from this game state
        stack.

        :param name: The name of the game state to remove.
        """
        if self.states[name]:
            del self.states[name]

    def slide(self, current_state, next_state):
        """


        :param current_state: The current state to exit.
        :param next_state: The new state to enter.
        """
        self.pop(current_state)
        self.push(next_state, False)

    def update(self, delta_time):
        """
        Updates every game state in this game state stack, starting with the
        "top", or head, of the stack.

        In order to allow for modality, updates occur as a reversed iteration
        over the current state stack.  This allows top-level game states to
        deny those beneath them the ability to update if such behavior is
        desired.

        :param delta_time: The amount of time in seconds that has passed
        since the previous update.
        """
        for state in reversed(self.stack):
            if not state.update(delta_time):
                break


class GameSubSystem(SubSystem):
    """


    Attributes:
        canvas (Canvas):
        stack (GameStateStack):
    """

    def __init__(self):
        super().__init__("game")
        self.canvas = None
        self.stack = GameStateStack()

    def get_dependencies(self):
        return {"init": ["display"], "update": [], "shutdown": []}

    def initialize(self, params, kernel):
        if not kernel.subsystems["display"]:
            raise SubSystemError("Could not obtain a canvas; the display "
                                 "subsystem has not been initialized or is "
                                 "not present.")
        self.canvas = kernel.subsystems["display"].canvas

    def shutdown(self):
        self.canvas = None
        self.stack.dispose()

    def update(self, delta_time):
        self.stack.update(delta_time)
        self.stack.draw(self.canvas)
        if not self.stack:
            pass
