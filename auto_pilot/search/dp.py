from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("dp")
class DP(RouteFinder):
    def __init__(self):
        pass

    def set(self):
        pass

    def set_noise(self):
        pass

    def sense(self):
        pass

    def move(self):
        pass

    @classmethod
    def from_params(cls, param: Param) -> 'DP':
        return cls()
