from auto_pilot.localization.filter import Filter
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from auto_pilot.robot.robot import Robot
from auto_pilot.common.util import measurement_prob
from overrides import overrides
import random
from typing import List


@Filter.register("particle")
class Particle(Filter):
    """
    continuous, 2D
    """
    def __init__(self, sense_noise: float, particle_num: int, particle_params: Param):
        self.__particle_num = particle_num
        self.__sense_noise = 0.0
        self.__particles: List[Robot] = \
            [Robot.from_params(particle_params) for _ in range(self.__particle_num)]

        self.set_noise(sense_noise)

    @overrides
    def set_noise(self, sense_noise: float):
        self.__sense_noise = sense_noise

    @overrides
    def sensing_update_prob(self, true_pos: Coordinates, landmarks: List[Coordinates]):
        """
        Calculate weight array and resample.
        """
        weights = []
        for i in range(self.__particle_num):
            weights.append(measurement_prob(true_pos, self.__sense_noise, landmarks))

        weight_max = max(weights)
        weight_index = 0
        beta = 0
        next_particles = []
        for i in range(self.__particle_num):
            beta += random.uniform(0, weight_max)
            while weights[weight_index] < beta:
                beta -= weights[weight_index]
                weight_index = (weight_index + 1) % self.__particle_num
            next_particles.append(self.__particles[weight_index])
        self.__particles = next_particles

    @overrides
    def motion_update_prob(self, motion: Motion):
        """
        Perform motion for each particle
        """
        [self.__particles[i].move(motion) for i in range(self.__particle_num)]

    @classmethod
    def from_params(cls, param: Param) -> 'Particle':
        particle_num: int = param.pop("particle_num")
        particle_params: Param = param.pop("particle_params")
        sense_noise: float = param.get("sense_noise", 0.0)
        return cls(
            particle_num=particle_num,
            particle_params=particle_params,
            sense_noise=sense_noise
        )
