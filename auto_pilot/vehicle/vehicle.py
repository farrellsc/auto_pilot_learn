from auto_pilot.common.param import Param
from auto_pilot.data.motion import Motion
from auto_pilot.common.registrable import Registrable
from typing import TypeVar
from math import pi
from typing import Tuple
T = TypeVar('T')


class Vehicle(Registrable):
    def set_noise(self, new_t_noise, new_d_noise, new_m_noise):
        """
        This lets us change the noise parameters, which can be very
        helpful when using particle filters.
        """
        raise NotImplementedError

    def move(self, motion: Motion, tolerance=0.001, max_turning_angle=pi):
        """This function turns the robot and then moves it forward."""
        raise NotImplementedError

    def sense(self) -> Tuple[float, float]:
        """
        This function represents the robot sensing its location. When
        measurements are noisy, this will return a value that is close to,
        but not necessarily equal to, the robot's (x, y) position.
        """
        raise NotImplementedError

    @classmethod
    def from_params(cls, param: Param) -> 'Vehicle':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)

