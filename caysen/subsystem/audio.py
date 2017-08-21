"""
Contains the implementation of the audio framework using PyDub.
"""
from caysen.kernel import SubSystem


class AudioSubSystem(SubSystem):
    """

    """

    def __init__(self):
        super().__init__("audio")

    def get_dependencies(self):
        return {"init": [], "update": ["game"], "shutdown": []}

    def initialize(self, params, kernel):
        return True

    def shutdown(self):
        return True

    def update(self, delta_time):
        return True
