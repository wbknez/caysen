"""
Contains all major sub-systems (audio, input, and video) as well as a simple
kernel to manage them.
"""
from abc import ABCMeta, abstractmethod


class SubSystem(metaclass=ABCMeta):
    """
    Represents a simple mechanism for creating and managing re-usable system
    resources and executing common tasks.
    """

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_initialization_dependencies(self):
        """
        Returns a list of other sub-systems this sub-system dependes on for
        initialization.

        :return: A list of initialization dependencies.
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