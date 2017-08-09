"""
Contains all of the enumerations of keyboard generated events that the input
system can both keep track of and bind user-created callbacks to.
"""
import enum


class ModState:
    """
    Represents a collection of the four most common modifier keys: alt,
    control, meta, and shift.

    This class is intended to encapsulate the general state of these
    modifiers at any point in time and so does not distinguish between,
    for example, left and right shift.

    Attributes:
        alt (bool): Whether or not an alt key is currently being pressed.
        control (bool): Whether or not a control key is currently being pressed.
        meta (bool): Whether or not a meta key is currently being pressed.
        shift (bool): Whether or not a shift key is currently being pressed.
    """

    def __init__(self, alt=False, control=False, meta=False, shift=False):
        self.alt = alt
        self.control = control
        self.meta = meta
        self.shift = shift

    def __eq__(self, other):
        if isinstance(other, ModState):
            return self.alt == other.alt and self.control == other.control \
                   and self.meta == other.meta and self.shift == other.shift
        return NotImplemented

    def __hash__(self):
        return hash((self.alt, self.control, self.meta, self.shift))

    def __ne__(self, other):
        return not self == other


class ModCounter:
    """
    Represents a mechanism for tracking the progression of the four most
    common modifier keys: alt, control, meta, and shift.

    Attributes:
        alt_count (int): The number of times the alt key has been pressed on
        either side.
        control_count (int): The number of times the control key has been
        pressed on either side.
        meta_count (int): The number of times the meta key has been pressed
        on either side.
        shift_count (int): The number of times the shift key has been pressed on
        either side.
    """

    def __init__(self, alt_count=0, control_count=0, meta_count=0,
                 shift_count=0):
        self.alt_count = alt_count
        self.control_count = control_count
        self.meta_count = meta_count
        self.shift_count = shift_count

    def update_state(self, mod_state):
        """
        Updates the specified modifier state with the current status of all
        tracked modifier keys.

        :param mod_state: The (current) modifier state to update.
        """
        mod_state.alt = True if self.alt_count > 0 else False
        mod_state.control = True if self.control_count > 0 else False
        mod_state.meta = True if self.meta_count > 0 else False
        mod_state.shift = True if self.shift_count > 0 else False


@enum.unique
class Key(enum.Enum):
    """
    Represents the different types of keys on a keyboard that can generate an
    input event.

    This set of keys is modeled after a keyboard with a QWERTY layout;
    international symbols may be missing.  In addition, due to how TDL models
    modifiers, this project does not recognize left or right variations of
    any of the modifier keys.  Technically, TDL recognizes left and right alt
    and control keys but not shift, which makes the scheme incomplete.  That
    said, it is easy enough to add if desired.  Just be aware that the alt
    and control keys are described in the key event class itself, while the
    left and right meta keys have their own event key descriptors.
    """

    """ Represents the letter 'a'. """
    A = 'a'

    """ Represents the letter 'b'. """
    B = 'b'

    """ Represents the letter 'c'. """
    C = 'c'

    """ Represents the letter 'd'. """
    D = 'd'

    """ Represents the letter 'e'. """
    E = 'e'

    """ Represents the letter 'f'. """
    F = 'f'

    """ Represents the letter 'g'. """
    G = 'g'

    """ Represents the letter 'h'. """
    H = 'h'

    """ Represents the letter 'i'. """
    I = 'i'

    """ Represents the letter 'j'. """
    J = 'j'

    """ Represents the letter 'k'. """
    K = 'k'

    """ Represents the letter 'l'. """
    L = 'l'

    """ Represents the letter 'm'. """
    M = 'm'

    """ Represents the letter 'n'. """
    N = 'n'

    """ Represents the letter 'o'. """
    O = 'o'

    """ Represents the letter 'p'. """
    P = 'p'

    """ Represents the letter 'q'. """
    Q = 'q'

    """ Represents the letter 'r'. """
    R = 'r'

    """ Represents the letter 's'. """
    S = 's'

    """ Represents the letter 't'. """
    T = 't'

    """ Represents the letter 'u'. """
    U = 'u'

    """ Represents the letter 'v'. """
    V = 'v'

    """ Represents the letter 'w'. """
    W = 'w'

    """ Represents the letter 'x'. """
    X = 'x'

    """ Represents the letter 'y'. """
    Y = 'y'

    """ Represents the letter 'z'. """
    Z = 'z'

    """ Represents the 'F1' key. """
    F1 = 'F1'

    """ Represents the 'F2' key. """
    F2 = 'F2'

    """ Represents the 'F3' key. """
    F3 = 'F3'

    """ Represents the 'F4' key. """
    F4 = 'F4'

    """ Represents the 'F5' key. """
    F5 = 'F5'

    """ Represents the 'F6' key. """
    F6 = 'F6'

    """ Represents the 'F7' key. """
    F7 = 'F7'

    """ Represents the 'F8' key. """
    F8 = 'F8'

    """ Represents the 'F9' key. """
    F9 = 'F9'

    """ Represents the 'F10' key. """
    F10 = 'F10'

    """ Represents the 'F11' key. """
    F11 = 'F11'

    """ Represents the 'F12' key. """
    F12 = 'F12'

    """ Represents the 'insert' key. """
    Insert = 'insert'

    """ Represents the 'delete' key. """
    Delete = 'delete'

    """ Represents the 'home' key. """
    Home = 'home'

    """ Represents the 'end' key. """
    End = 'end'

    """ Represents the 'page up' key. """
    Page_Up = 'pageup'

    """ Represents the 'page down' key. """
    Page_Down = 'pagedown'

    """ Represents the 'space bar' as a key. """
    Space = 'space'

    """ Represents the 'enter', or 'return', key. """
    Enter = 'enter'

    """ Represents the 'caps lock' key. """
    Caps_Lock = 'capslock'

    """ Represents the 'grave', or 'tilde' key. """
    Grave = 'grave'

    """ Represents the 'escape' key. """
    Escape = 'escape'

    """ Represents the 'backspace' key. """
    Backspace = 'backspace'

    """ Represents the 'tab' key. """
    Tab = 'tab'

    """ Represents either 'alt' key. """
    Alt = 'alt'

    """ Represents either 'control' key. """
    Control = 'control'

    """ Represents either 'meta' key. """
    Meta = 'meta'

    """ Represents either 'shift' key. """
    Shift = 'shift'

    """ Represents the 'print screen' key. """
    Print_Screen = 'print_screen'

    """ Represents the 'scroll lock' key. """
    Scroll_Lock = 'scrolllock'

    """ Represents the 'pause' key. """
    Pause = 'pause'

    """ Represents the 'down arrow' key. """
    Down = 'down'

    """ Represents the 'left arrow' key. """
    Left = 'left'

    """ Represents the 'right arrow' key. """
    Right = 'right'

    """ Represents the 'up arrow' key. """
    Up = 'up'

    """ Represents the 'comma' key. """
    Comma = ','

    """ Represents the 'caps lock' key. """
    Period = '.'

    """ Represents the 'backslash' key. """
    Back_Slash = '/'

    """ Represents the 'semicolon' key. """
    Semicolon = ';'

    """ Represents the 'apostrophe' key. """
    Apostrophe = '\''

    """ Represents the 'left bracket' key. """
    Left_Bracket = '['

    """ Represents the 'right bracket' key. """
    Right_Bracket = ']'

    """ Represents the 'forward slash' key. """
    Forward_Slash = '\\'

    """ Represents the 'hyphen', or 'dash', key. """
    Hyphen = '-'

    """ Represents the 'equals' key. """
    Equals = '='

    """ Represents the 'number 1' key. """
    num_1 = '1'

    """ Represents the 'number 2' key. """
    num_2 = '2'

    """ Represents the 'number 3' key. """
    num_3 = '3'

    """ Represents the 'number 4' key. """
    num_4 = '4'

    """ Represents the 'number 5' key. """
    num_5 = '5'

    """ Represents the 'number 6' key. """
    num_6 = '6'

    """ Represents the 'number 7' key. """
    num_7 = '7'

    """ Represents the 'number 8' key. """
    num_8 = '8'

    """ Represents the 'number 9' key. """
    num_9 = '9'

    """ Represents the 'number 0' key. """
    num_0 = '0'


@enum.unique
class Numpad(enum.Enum):
    """
    Represents the different types of keys on a numpad that can generate an
    input event.
    """

    """ Represents the 'number 1' key. """
    num_1 = 'kp1'

    """ Represents the 'number 2' key. """
    num_2 = 'kp2'

    """ Represents the 'number 3' key. """
    num_3 = 'kp3'

    """ Represents the 'number 4' key. """
    num_4 = 'kp4'

    """ Represents the 'number 5' key. """
    num_5 = 'kp5'

    """ Represents the 'number 6' key. """
    num_6 = 'kp6'

    """ Represents the 'number 7' key. """
    num_7 = 'kp7'

    """ Represents the 'number 8' key. """
    num_8 = 'kp8'

    """ Represents the 'number 9' key. """
    num_9 = 'kp9'

    """ Represents the 'number 0' key. """
    num_0 = 'kp0'

    """ Represents the 'addition' key. """
    Add = 'kpadd'

    """ Represents the 'decimal', or 'period', key. """
    Decimal = 'kpdec'

    """ Represents the 'division' key. """
    Divide = 'kpdiv'

    """ Represents the 'enter', or 'return', key. """
    Enter = 'kpenter'

    """ Represents the 'multiply' key. """
    Multiply = 'kpmul'

    """ Represents the 'subtract' key. """
    Subtract = 'kpsub'
