"""
Contains all major sub-systems (audio, input, and video) as well as a simple
kernel to manage them.
"""
from abc import ABCMeta, abstractmethod

from caysen.util.timers import SystemTimer


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
        one-time initialization, repeated updates, or shutdown - must be
        initialized or updated before this sub-system may do the same.

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


def _get_execution_order(deps):
    """
    Resolves the specified dictionary of dependencies into a flat list,
    organized from those with the least dependencies to those with the most
    in order to ensure all sub-systems execute before their dependants.

    This algorithm was taken from a StackOverflow question at the following
    link:
    https://stackoverflow.com/questions/5287516/dependencies-tree-implementation
    and the link to the original script in Python is:
        https://code.activestate.com/recipes/576570-dependency-resolver/

    :param deps: A dictionary of sub-system names with associated dependencies.
    """
    tree = []

    while deps:
        # Dependencies that are not named in the original dict.
        # This does not actually happen in this project but it is still
        # an important case to cover.
        no_deps = set(subsystem for dep in deps.values() \
                      for subsystem in deps) - set(deps.keys())

        # Named dependants with no associated dependencies.
        no_deps.update(subsystem for subsystem, dep in deps.items()
                       if not dep)

        # Because they have no further dependencies, they can be added
        # to the resulting dependency tree.
        tree.append(no_deps)

        # Remove dependencies that have been met (are in the tree).
        deps = dict(((subsystem, dep - no_deps)
                     for subsystem, dep in deps.items() if dep))

    # Flatten.
    return [item for subtree in tree for item in subtree]


def _get_dependencies(for_state, subsystems):
    """

    :param for_state:
    :return:
    """
    deps = dict()

    for subsystem in subsystems.values():
        deps[subsystem.name] = subsystem.get_dependencies()[for_state]
    return deps


class Kernel:
    """


    Attributes:
        exec_order (list):
        is_running (bool):
    """

    def __init__(self):
        self.exec_order = list()
        self.is_running = False
        self.subsystems = dict()
        self.timer = SystemTimer()

    def add(self, system, alternate_name=None):
        """

        :param system:
        :param alternate_name:
        :return:
        """
        if alternate_name is None:
            other_name = system.name
        self.subsystems[alternate_name] = system

    def initialize(self, params):
        self._set_execution_order("init")
        for subsystem in self.exec_order:
            subsystem.initialize(params)

    def remove(self, name):
        if self.subsystems[name]:
            del self.subsystems[name]

    def run(self):
        """

        :return:
        :raise ValueError: If the kernel is already running or there are no
        sub-systems available for use.
        """
        if self.is_running:
            raise ValueError('Kernel is already running.')

        if not self.subsystems:
            raise ValueError('There are no sub-systems available for use.')

        self._set_execution_order("update")
        self.is_running = True
        self.timer.start()

        while self.is_running:
            self.timer.update()
            for subsystem in self.exec_order:
                if not subsystem.update(self.timer.delta_time):
                    self.is_running = False
                    break

    def _set_execution_order(self, for_state):
        """

        :param for_state:
        """
        deps = _get_dependencies(for_state, self.subsystems)
        exec_names = _get_execution_order(deps)

        self.exec_order.clear()
        for name in exec_names:
            self.exec_order.append(self.subsystems[name])

    def shutdown(self):
        self._set_execution_order("shutdown")
        for subsystem in self.exec_order:
            subsystem.shutdown()
