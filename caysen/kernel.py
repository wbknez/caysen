"""
Contains all major subsystems (audio, input, and video) as well as a simple
kernel to manage them.
"""
from abc import ABCMeta, abstractmethod

from caysen.util.timers import SystemTimer


class SubSystem(metaclass=ABCMeta):
    """
    Represents a simple mechanism for creating and managing re-usable system
    resources and executing common tasks.

    Attributes:
        name (str): The name of the subsystem for identification purposes.
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_dependencies(self):
        """
        Returns a list of other subsystems this subsystem dependes on for
        both initialization and updates.

        Put more clearly, every dependency for each execution - either
        one-time initialization, repeated updates, or shutdown - must be
        initialized or updated before this subsystem may do the same.

        :return: A dict of initialization and update dependencies.
        """
        pass

    @abstractmethod
    def initialize(self, params, kernel):
        """
        Initializes this subsystem and acquires all system resources that
        are necessary for successful operation.

        Like 'shutdown', the return value for this function is never
        actually used.  It is included, however, for completeness.

        :param params: A dictionary of user-modified parameters.
        :param kernel: The kernel that contains other subsystems this one
        might need for initialization.  This also lets this subsystem hold a
        reference to dependencies.
        :return: False if unsuccessful, otherwise True.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Shuts down this subsystem and frees all system resources it is
        currently using.

        Like 'initialize', the return value for this function is never
        actually used.  It is included, however, for completeness.

        :return: False if unsuccessful, otherwise True.
        """
        pass

    @abstractmethod
    def update(self, delta_time):
        """
        Updates this subsystem in some way.

        :param delta_time: The amount of time in seconds that has passed
        since the previous update.
        :return: False if unsuccessful, otherwise True.
        """
        pass


def _get_dependencies(for_state, subsystems):
    """
    Creates and returns a dictionary of dependencies by subsystem name for a
    specific state.

    :param for_state: The state to extract the dependencies for.
    :return: A dictionary of dependencies for a specific state,
    each associated with a subsystem by name.
    """
    deps = dict()

    for subsystem in subsystems.values():
        deps[subsystem.name] = subsystem.get_dependencies()[for_state]
    return deps


def _get_execution_order(for_state, subsystems):
    """
    Resolves the specified dictionary of subsystems with associated
    dependencies into a flat list based on which state is needed,
    organized from those with the least dependencies to those with the most
    in order to ensure all subsystems execute before their dependants.

    For this project, the possible states to choose dependencies from are:
        * init - Initialization dependencies dictate the order that
        subsystems are initialized in.
        * update - Run loop dependencies dictate the order in which
        subsystems are executed in the main (game) loop.
        * shutdown - Shutdown dependencies dictate the order that subsystems
        are shutdown.

    This algorithm is taken from a StackOverflow question at the following
    link:
    https://stackoverflow.com/questions/5287516/dependencies-tree-implementation
    and the link to the original script in Python is:
        https://code.activestate.com/recipes/576570-dependency-resolver/

    :param for_state: A single string that denotes which state the
    dependencies should be taken from.
    :param subsystems: A dictionary of subsystems, each associated with a
    unique name that appears in the dependency list.
    :return:
    """
    tree = []
    deps = _get_dependencies(for_state, subsystems)

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

    # Flatten and revert to subsystems instead of strings.
    flat_tree = [item for subtree in tree for item in subtree]
    return [subsystems[system] for system in flat_tree]


class Kernel:
    """
    Represents a mechanism for managing subsystems, each of which may
    themselves manage various system resources, in a simple and centralized
    manner.

    Attributes:
        is_running (bool): Whether or not the kernel is currently executing
        an infinite loop that only stops when signaled.
        subsystems (dict): A dictionary of subsystems, each associated with a
        unique name.
        timer (SystemTimer): A high performance timer that measured elapsed
        time in fractions of a second.
    """

    def __init__(self):
        self.is_running = False
        self.subsystems = dict()
        self.timer = SystemTimer()

    def add(self, subsystem, alternate_name=None):
        """
        Adds the specified subsystem to this kernel with the specified
        alternate name.

        If the alternate name is not valid then the subsystem's individual
        name will be used instead.

        :param subsystem: The subsystem to add.
        :param alternate_name: An alternate name for the subsystem; this
        allows two or more subsystems of a specific type to be added to the
        kernel (if for some reason that is desirable).  If no alternate name
        is given, the subsystem's name is used instead.
        """
        if alternate_name is None:
            alternate_name = subsystem.name
        self.subsystems[alternate_name] = subsystem

    def initialize(self, params):
        """
        Initializes all of the subsystems in this kernel using the specified
        dictionary of user-modified parameters.

        :param params: A dictionary of user-modified parameters.
        """
        exec_order = _get_execution_order('init', self.subsystems)
        for subsystem in exec_order:
            subsystem.initialize(params, self)

    def remove(self, name):
        """
        Removes the subsystem with the specified name from this kernel.

        :param name: The name of the subsystem to remove.
        """
        if self.subsystems[name]:
            del self.subsystems[name]

    def run(self):
        """
        Initiates an infinite loop within which each subsystem is updated
        atomically with the current elapsed time (in seconds).

        The loop is stopped if any subsystem's update method returns False or if
        the kernel flag is signaled.

        :raise ValueError: If the kernel is already running or there are no
        subsystems available for use.
        """
        if self.is_running:
            raise ValueError('Kernel is already running.')

        if not self.subsystems:
            raise ValueError('There are no subsystems available for use.')

        exec_order = _get_execution_order('update', self.subsystems)
        self.is_running = True
        self.timer.start()

        while self.is_running:
            self.timer.update()
            for subsystem in exec_order:
                if not subsystem.update(self.timer.delta_time):
                    self.is_running = False
                    break

    def shutdown(self):
        """
        Shutdowns all of the subsystems in this kernel individually.
        """
        exec_order = _get_execution_order('shutdown', self.subsystems)
        for subsystem in exec_order:
            subsystem.shutdown()
