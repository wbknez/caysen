"""
Contains timers that are each specialized for different use-cases, such as
monitoring the elapsed system time for update purposes or waiting for a
specific amount of wallclock time to pass before performing an action.
"""
import time


class SystemTimer:
    """
    Represents a simple mechanism for measuring the amount of wallclock time
    in milliseconds that has elapsed during game updates.

    Attributes:
        current_time (float): The most recently requested time in miliseconds.
        delta_time (float): The amount of time that elapsed between the
        most current requested time and the last one.
        last_time (float): The last requested time in milliseconds.
    """

    def __init__(self):
        self.current_time = 0.0
        self.delta_time = 0.0
        self.last_time = 0.0

    def reset(self):
        """
        Resets all of the time-based variables by setting them to zero.
        """
        self.current_time = self.delta_time = self.last_time = 0.0

    def start(self):
        """
        Begins tracking the current time.
        """
        self.current_time = time.time()

    def update(self):
        """
        Captures the current time since epoch and updates this delta timer's
        internal state, replacing the previously captured time with the
        current one and recomputing the amount of time that has elapsed since
        the last time this function was called.
        """
        self.last_time = self.current_time
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time


class Stopwatch:
    """
    Represents a simple mechanism for waiting for a specific amount of time.

    Attributes:
        callback (func): The function to call when the target time is reached.
        is_running (bool): Whether or not the stopwatch is currently tracking
        the elapsed time until some target time is reached.
        repeating (bool): Whether or not the stopwatch should reset itself
        and continue to call the callback after the target time has been
        reached.
        start_time (float): The time (in milliseconds) since epoch at which
        the stopwatch starting tracking time.
        target_time (float): The amount of time (in milliseconds) that the
        stopwatch should run for.
    """

    def __init__(self, target_time=0.0, repeating=False, callback=None):
        self.callback = callback
        self.is_running = False
        self.repeating = repeating
        self.start_time = 0.0
        self.target_time = target_time

    def start(self, target_time=None):
        """
        Starts the stopwatch tracking the elapsed time towards some target.

        :param target_time: The time in milliseconds that this stopwatch
        should run for; this is unnecessary if the target time was set in the
        constructor.
        """
        if target_time is not None:
            self.target_time = target_time

        self.is_running = True
        self.start_time = time.time()

    def update(self):
        """
        Forces the stopwatch to check how much time has elapsed since it
        started tracking time and call the callback if the target time has
        been reached.

        If this stopwatch has been set to repeat, then it will reset itself
        and continue.  Otherwise, it will set the running false to False and
        stop.

        :return: Whether or not the stopwatch is still running.
        :raises ValueError: If the stopwatch is not running (prior to this
        function being called).
        """
        if not self.is_running:
            raise ValueError('The stopwatch is not running.')

        delta_time = time.time() - self.start_time

        if delta_time >= self.target_time:
            if self.callback is not None:
                self.callback()
            self.is_running = False

        if self.repeating:
            self.is_running = True
            self.start_time = delta_time - self.target_time

        return self.is_running
