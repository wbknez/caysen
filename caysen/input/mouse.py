"""
Contains all of the enumerations of mouse generated events that the input
system can both keep track of and bind user-created callbacks to.
"""
import enum


@enum.unique
class MouseButton(enum.Enum):
    """
    Represents the different types of mouse buttons that can generate an
    input event.
    """

    """
    Represents a mouse button event generated by the left mouse button 
    being either pressed or released.
    """
    Left = 0

    """
    Represents a mouse button event generated by the middle mouse button 
    (the mouse wheel) being either pressed or released.
    """
    Middle = 1

    """
    Represents a mouse button event generated by the right mouse button 
    being either pressed or released.
    """
    Right = 2


@enum.unique
class MouseMotion(enum.Enum):
    """
    Represents the different types of mouse motion an input system can track.
    """

    """
    Represents a mouse motion event that has been clamped to the nearest cell 
    on a display.
    
    Note that the cell size is based on the font the display is using.
    """
    Cell = 5

    """
    Represents a mouse motion event that is given in terms of display 
    coordinates.
    """
    Position = 6


@enum.unique
class MouseWheel(enum.Enum):
    """
    Represents the different mouse wheel events that can occur.
    """

    """
    Represents a mouse button event generated by the mouse wheel being 
    scrolled down.
    """
    Down = 3

    """
    Represents a mouse button event generated by the mouse wheel being 
    scrolled up.
    """
    Up = 4
