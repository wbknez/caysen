"""
Contains methods and classes pertaining to two dimensional bounds;
specifically circles and squares.
"""

from abc import ABCMeta, abstractmethod

import numpy as np


class Bounds(metaclass=ABCMeta):
    """
    Represents a two-dimensional bounding area that can be tested for
    intersections with a variety of geometric shapes.

    Attributes:
        center (numpy.array): The center of the bounding area in
        two-dimensional space.
    """

    def __init__(self, center=np.zeros(2, dtype=np.int32)):
        self.center = center

    @abstractmethod
    def intersects(self, bounds):
        """
        Tests whether or not an intersection occurred between this bounds the
        specified bounds.

        :param bounds: The bounding area to test.
        :return: Whether or not an intersection occurred.
        """
        pass

    @abstractmethod
    def intersects_circle(self, circle):
        """
        Tests whether or not an intersection occurred between this bounds and
        the specified bounding circle.

        :param circle: The circle to test.
        :return: Whether or not an intersection occurred.
        """
        pass

    @abstractmethod
    def intersects_square(self, square):
        """
        Tests whether or not an intersection occurred between this bounds and
        the specified bounding square.

        :param square: The square to test.
        :return: Whether or not an intersection occurred.
        """
        pass
