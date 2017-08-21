"""

"""
from caysen.game.state import GameSubSystem
from caysen.kernel import Kernel

from caysen.subsystem.audio import AudioSubSystem
from caysen.subsystem.display import DisplaySubSystem
from caysen.subsystem.input import InputSubSystem


def create_kernel():
    kernel = Kernel()

    kernel.add(AudioSubSystem())
    kernel.add(DisplaySubSystem())
    kernel.add(GameSubSystem())
    kernel.add(InputSubSystem())

    return kernel


def get_config_params(config_file):
    return {}


def get_user_params():
    return {}


def get_combined_params(config_file):
    config_params = get_config_params(config_file)
    user_params = get_user_params()

    return {**config_params, **user_params}
