from auto_pilot.control.controller import Controller
from auto_pilot.common.param import Param
from overrides import overrides


@Controller.register("PID")
class PID(Controller):
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
    def from_params(cls, param: Param) -> 'PID':
        return cls()
