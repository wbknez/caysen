"""
Contains all of the supporting infrastructure for the creation and binding of
arbitrary input actions to event handlers, or callbacks.
"""
import enum


@enum.unique
class ActionState(enum.Enum):
    """
    Represents the different types of activation states an input action may
    have.
    """

    """
    Represents an action that has been pressed "down" or otherwise activated.
    """
    Down = 'down'

    """
    Represents an action that is being kept in the "down" state repeatedly 
    over a period of time.
    """
    Held = 'held'

    """
    Represents an action whose movement component has changed in some way.
    """
    Motion = 'motion'

    """
    Represents an action that has been released and is now "up" or otherwise 
    free.
    """
    Up = 'up'


class Action:
    """
    Represents a single input action of arbitrary origin.

    Attributes:
        code (str): The type of action.
        state (ActionState): The state of the action.
        mods (Modifiers): The modifiers that must be active in order for the
        action to trigger.
    """

    def __init__(self, code, state=None, mods=None):
        self.code = code
        self.state = state
        self.mods = mods

    def __eq__(self, other):
        if isinstance(other, Action):
            return self.code == other.code and self.state == other.state \
                   and self.mods == other.mods
        return NotImplemented

    def __hash__(self):
        hash((self.code, self.state, self.mods))

    def __ne__(self, other):
        return not self == other


class ActionNotBoundError(Exception):
    """
    Represents an exception that is thrown when an attempt is made to "fire", or
    otherwise execute, a callback for an action that an action map does not
    have and cannot find anywhere in the hierarchy to which it belongs.
    """


class ActionMap:
    """
    Represents a mapping of actions to lists of callbacks that are invoked
    when those actions are detected, or triggered, by some other stimulus.

    Programmatically, action maps bind callbacks to different combinations of
    keys, button states, and modifiers.  The map itself makes no distinction
    between the type of actions that are and are not allowed in the map,
    providing no mechanism to filter or otherwise block actions from being
    acted on.

    In addition, action maps each contain a "parent" map and so may form a
    hierarchy.  This allows maps lower on the chain to handle actions that
    are not bound to them (and also those that are not bound to their
    parents) and so may function as an overlay of sorts.  This is
    particularly useful for state stacks to allow states to inherit another's
    input handling while simultaneously overwriting selection portions.

    Attributes:
        actions (dict): A mapping of all bindable actions to a list of
        callbacks for that particular binding.
        parent (ActionMap): The parent action map in a hierarchy that allows
        one map to field requests for actions that they do not themselves
        posses but can be found elsewhere.
    """

    def __init__(self, parent=None):
        self.actions = {}
        self.parent = parent

    def bind(self, action, callback):
        """
        Binds the specified action to the specified callback so that, during
        gameplay, the callback executes when that action occurs.

        :param action: The action to bind.
        :param callback: The callback to call when the action occurs.
        """
        if action not in self.actions:
            self.actions[action] = list()
        self.actions[action].append(callback)

    def fire(self, action, args=None):
        """
        Attempts to call, or otherwise execute, all of the callbacks bound to
        the specified action and pass them any additional, necessary
        arguments as well.

        :param action: The action whose callbacks should be executed.
        :param args: Any additional arguments to send to the callbacks.
        :raises ActionNotBoundError: If the specified action is neither found in
        this action map nor its parent.
        """
        if action not in self.actions:
            if self.parent is not None:
                self.parent.fire(action, args)
            else:
                raise ActionNotBoundError(action + ' not bound to any '
                                                   'callbacks.')

        for callback in self.actions[action]:
            callback(args)

    def is_bound(self, action):
        """
        Returns whether or not the specified action is bound to at least one
        valid callback.

        :param action: The action to search for.
        :return: Whether or not the action has at least one valid callback
        associated with it.
        """
        return action in self.actions and len(self.actions[action]) > 0

    def is_bound_to(self, action, callback):
        """
        Returns whether or not the specified callback is in the list of
        callbacks bound to the specified action.

        :param action: The action to search for.
        :param callback: The callback to check.
        :return: Whether or not the callback is bound to the action.
        """
        return action in self.actions and callback in self.actions[action]

    def unbind(self, action, callback):
        """
        Unbinds the specified callback from being associated with the
        specified action.

        If this action results in the specified action having no valid
        callbacks bound to it, it is removed completely from this action map.

        :param action: The action to unbind the callback from.
        :param callback: The callback to unbind.
        """
        if action in self.actions and callback in self.actions[action]:
            self.actions[action].remove(callback)
            if len(self.actions[action]) == 0:
                del self.actions[action]

    def unbind_all(self, action):
        """
        Unbinds all of the callbacks associated with the specified action.

        :param action: The action to unbind.
        """
        if action in self.actions:
            del self.actions[action]
