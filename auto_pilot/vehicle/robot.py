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
    def __init__(self, x=0.0, y=0.0, heading=0.0, turning=2*pi/10, distance=1.0, drift=0):
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
        self.steering_drift = drift

    @overrides
    def set_noise(self, new_t_noise: float, new_d_noise: float, new_m_noise: float, drift: float):
        self.turning_noise = new_t_noise
        self.distance_noise = new_d_noise
        self.measurement_noise = new_m_noise
        self.steering_drift = drift

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

    """
    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        \"""
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        \"""
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)
    """

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