from auto_pilot.mapping.Mapper import Mapper
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("SLAM")
class SLAM(Mapper):
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
    def from_params(cls, param: Param) -> 'SLAM':
        return cls()
