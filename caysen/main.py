#!/usr/bin/env python3

"""
The main driver for Caysen, a small, example roguelike village that is used
to explore artificial intelligence algorithms that emphasize emotional
awareness and social cognition.
"""
import logging
import sys

from caysen.config import create_kernel, get_combined_params
from caysen.kernel import SubSystemError, AppExitSignal


def main():
    """
    The application entry point.

    :return: An exit code.
    """
    params = get_combined_params('data/config.yml')
    kernel = create_kernel()

    try:
        kernel.initialize(params)
    except SubSystemError:
        logging.exception("A subsystem encountered a critical error during "
                          "initialization; the application will now exit "
                          "prematurely.")
        sys.exit(0)

    try:
        kernel.run()
    except AppExitSignal:
        logging.info('Received user application exit signal from kernel; '
                     'proceeding to shutdown.')
    except SubSystemError:
        # It bears worth noting here that handling errors in execution is a
        # subject that is certainly open to debate.
        # In this case, we are going to go ahead and try and shutdown as many
        # systems as possible in order to cleanly release as many resources
        # as we can.
        # This would potentially be cleaner if we knew which subsystem caused
        # the problem, specifically, but it does not matter.  Well designed
        # subsystems should be capable of correctly shutting down even if
        # something terrible happened to their internal state.
        logging.critical('A subsytem encountered a critical error during the '
                         'main game loop; attempting to shutdown those that '
                         'remain.')

    if not kernel.shutdown():
        logging.critical("The shutdown process did not complete without "
                         "error.  Please inspect above in the log file to "
                         "find out why.")


if __name__ == "__main__":
    sys.exit(main())
