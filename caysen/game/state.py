"""

"""
from caysen.kernel import SubSystem


class GameSubSystem(SubSystem):
    """

    """

    def __init__(self):
        super().__init__("game")

    def get_dependencies(self):
        return {"init": [], "update": [], "shutdown": []}

    def initialize(self, params, kernel):
        return True

    def shutdown(self):
        return True

    def update(self, delta_time):
        return True
