from auto_pilot.robot.robot import Robot
from auto_pilot.data.path import Path
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.control.controller import Controller
from auto_pilot.common.param import Param
from overrides import overrides
from typing import List


@Controller.register("PID")
class PID(Controller):
    def __init__(self, bot: Robot, tau_p, tau_d, tau_i):
        self.robot = bot
        self.tau_p = tau_p
        self.tau_d = tau_d
        self.tau_i = tau_i

    @overrides
    def run(self, n=100, speed=1.0) -> Path:
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

        trajectory = [Coordinates(x_trajectory[i], y_trajectory[i]) for i in range(len(y_trajectory))]
        return Path(trajectory)

    @classmethod
    def from_params(cls, param: Param) -> 'PID':
        bot = Robot.from_params(param.pop("robot"))
        tau_p = param.pop("tau_p")
        tau_d = param.pop("tau_d")
        tau_i = param.pop("tau_i")
        return cls(bot=bot, tau_p=tau_p, tau_d=tau_d, tau_i=tau_i)
