#!/usr/bin/env python3

"""
The main driver for Caysen, a small, example roguelike village that is used
to explore artificial intelligence algorithms that emphasize emotional
awareness and social cognition.
"""
import sys

from caysen.initializer import create_kernel, get_combined_params


def main():
    """
    The application entry point.

    :return: An exit code.
    """
    params = get_combined_params('data/config.ini')
    kernel = create_kernel()

    kernel.initialize(params)
    kernel.run()
    kernel.shutdown()


if __name__ == "__main__":
    sys.exit(main())
