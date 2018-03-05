from auto_pilot.vehicle.vehicle import Vehicle
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.control.controller import Controller
from auto_pilot.common.param import Param
from auto_pilot.data.motion import Motion
from overrides import overrides
from typing import List


@Controller.register("PID")
class PID(Controller):
    def __init__(self, bot: Vehicle, tau_p, tau_d, tau_i):
        self.robot = bot
        self.tau_p = tau_p
        self.tau_d = tau_d
        self.tau_i = tau_i

    @overrides
    def run(self, n=100, speed=1.0) -> List[Coordinates]:
        x_trajectory = []
        y_trajectory = []
        sum_CTE = 1

        for i in range(n):
            if len(y_trajectory) == 0:
                steering = -self.tau_p * self.robot.y - self.tau_i * sum_CTE
            elif len(y_trajectory) == 1:
                steering = -self.tau_p * self.robot.y - self.tau_d * (y_trajectory[-1] - 1) - self.tau_i * sum_CTE
            else:
                steering = -self.tau_p * y_trajectory[-1] - self.tau_d * (y_trajectory[-1] - y_trajectory[-2]) - \
                           self.tau_i * sum_CTE
            self.robot.move(steering, speed)
            x_trajectory.append(self.robot.x)
            y_trajectory.append(self.robot.y)
            sum_CTE += self.robot.y

        return x_trajectory, y_trajectory

    @classmethod
    def from_params(cls, param: Param) -> 'PID':
        return cls()
