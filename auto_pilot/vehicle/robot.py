from auto_pilot.vehicle.vehicle import Vehicle
from auto_pilot.common.param import Param
from overrides import overrides


@Vehicle.register("robot")
class Robot(Vehicle):
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
    def from_params(cls, param: Param) -> 'Robot':
        return cls()
