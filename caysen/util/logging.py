"""
Contains classes and functions to add additional logging capabilities to this
project, including colored console output and a new logging level solely for AI
related messages.
"""
import logging

_BASE_FORMAT = "%(symb) %(log) %(msg)"

_COLORS = {"DEBUG": "",
           "INFO": "",
           "WARNING": "",
           "CRITICAL": "",
           "ERROR": ""}

_SYMBOLS = {"DEBUG": ">",
            "INFO": "*",
            "WARNING": "*",
            "CRITICAL": "!!",
            "ERROR": "!!"}


def _log_proxy(self, message, level, *args, **kws):
    """
    A proxy method used to send logging messages to functions that have been
    dynamically added to Logger.

    :param message: The message to log.
    :param level: The logging level to use.
    :param args: A combination of arguments that will be combined with
    message to form a complete log message.
    :param kws: Additional logging information such as exec_info().
    """
    if self.isEnabledFor(level):
        self._log(level, message, args, **kws)


class LogLevel:
    """
    A collection of utility methods for adding custom log levels to Python's
    logging framework.

    Attributes:
        _CUSTOM_LEVELS (dict): A dictionary of custom logging level values
        associated by name.
    """

    _CUSTOM_LEVELS = dict()

    @classmethod
    def add(cls, name, value):
        """
        Adds a new logging level with the specified name and value to
        Python's logging framework as well as adding a custom instance
        function with the same name to Logger for easy use.

        :param name: The name of the logging level.
        :param value: The numeric value of the logging level.
        :raise KeyError: If the logging level has already been added.
        """
        if LogLevel._CUSTOM_LEVELS[name]:
            raise KeyError("Log level %s has already been registered with "
                           "Python's logging framework.  Please choose "
                           "another name and try again." % name)
        LogLevel._CUSTOM_LEVELS[name] = value
        logging.addLevelName(value, name)
        setattr(logging.Logger, name, lambda self, message, *args, **kws:
                _log_proxy(self, message, level=value, *args, **kws))

    @classmethod
    def remove(cls, name):
        """
        Removes the logging level with the specified name from both this
        class' and Python's logging framework's collection of levels, as well as
        removing any custom Logger functions.

        :param name: The name of hte logging level to remove.
        :raise KeyError: If the logging level has already been deleted.
        """
        if not LogLevel._CUSTOM_LEVELS[name]:
            raise KeyError("The log level %s has not been registered with "
                           "Python's logging framework and so cannot be "
                           "removed." % name)
        del LogLevel._CUSTOM_LEVELS[name]
        logging.addLevelName(logging.NOTSET, name)
        delattr(logging.Logger, name)

    @classmethod
    def value(cls, name):
        """
        Returns the value of the specified logging level that can be used to
        send and control output from loggers.

        :param name: The name of the logging level to search for.
        :return: The logging level value.
        :raise KeyError: If a logging level with the given name cannot be found.
        """
        if not LogLevel._CUSTOM_LEVELS[name]:
            raise KeyError("The log level %s has not been registered with "
                           "Python's logging framework yet." % name)
        return LogLevel._CUSTOM_LEVELS[name]


class ColoredFormatter(logging.Formatter):
    """
    Formats individual logging records by inserting ANSI escape sequences to
    color text.

    In addition to color, this formatter also minimizes the resulting message
    string by not including date information and reducing the level name to a
    series of colored symbols.  Please note that the messages themselves are
    not colored.

    The symbol and color combinations applied by this formatter are as follows:
        - > (brown)  Debug message.
        - * (white)  Information message.
        - * (yellow) Warning message.
        - !! (red)   Critical message.
        - !! (red)   Error message.

    The message format is as follows:
        [symbol] ([logger name]) [message]
    where symbol is the color and symbol combination described above (per
    level type), the logger name corresponds to the module of the logger that
    produced the record, and the message is the one that is unchanged from the
    logging record itself.  Finally, all emssages but INFO are indented by a
    single space for added visibility.
    """

    def format(self, record):
        symbol = _COLORS[record.levelname] % _SYMBOLS[record.levelname]
        return _BASE_FORMAT % {"sym": symbol, "log": record.name,
                               "msg": record.msg}
