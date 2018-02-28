from auto_pilot.localization.filter import Filter
from auto_pilot.common.param import Param
from overrides import overrides


@Filter.register("histogram")
class Histogram(Filter):
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
    def from_params(cls, param: Param) -> 'Histogram':
        return cls()
