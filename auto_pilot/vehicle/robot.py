from auto_pilot.common.registrable import Registrable
from auto_pilot.vehicle.vehicle import Vehicle
from auto_pilot.common.util import angle_trunc
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.motion import Motion
from math import pi, cos, sin
import random
from auto_pilot.common.param import Param
from overrides import overrides
from typing import Tuple


@Vehicle.register("robot")
class Robot(Vehicle):
    def __init__(self, x=0.0, y=0.0, heading=0.0, turning=2*pi/10, distance=1.0):
        """
        This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created.
        """
        self.x = x
        self.y = y
        self.heading = heading
        self.turning = turning
        self.distance = distance
        self.turning_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0

    @overrides
    def set_noise(self, new_t_noise: float, new_d_noise: float, new_m_noise: float):
        self.turning_noise = new_t_noise
        self.distance_noise = new_d_noise
        self.measurement_noise = new_m_noise

    @overrides
    def move(self, motion: Motion, tolerance=0.001, max_turning_angle=pi):
        """
        apply noise, this doesn't change anything if turning_noise and distance_noise are zero.
        """
        turning = random.gauss(motion.turning, self.turning_noise)
        distance = random.gauss(motion.distance, self.distance_noise)

        # truncate to fit physical limitations
        turning = max(-max_turning_angle, turning)
        turning = min(max_turning_angle, turning)
        distance = max(0.0, distance)

        # Execute motion
        self.heading += turning
        self.heading = angle_trunc(self.heading)
        self.x += distance * cos(self.heading)
        self.y += distance * sin(self.heading)

    @overrides
    def sense(self) -> Coordinates:
        return Coordinates(random.gauss(self.x, self.measurement_noise),
                           random.gauss(self.y, self.measurement_noise))

    def __repr__(self):
        """
        This allows us to print a robot's position
        """
        return '[%.5f, %.5f]'  % (self.x, self.y)

    @classmethod
    def from_params(cls, param: Param) -> 'Robot':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)