from auto_pilot.localization.filter import Filter
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from auto_pilot.vehicle.vehicle import Vehicle
from auto_pilot.common.util import measurement_prob
from overrides import overrides
import numpy as np
import random
from typing import List


@Filter.register("particle")
class Particle(Filter):
    def __init__(self, sense_noise: float, particle_num: int, particle_type: Vehicle, particle_params):
        self.__particle_num = particle_num
        self.__sense_noise = sense_noise
        self.__particles: List[particle_type] = \
            [particle_type.from_params(particle_params) for _ in range(self.__particle_num)]

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
                weight_index = (weight_index+ 1) % self.__particle_num
            next_particles.append(self.__particles[weight_index])
        self.__particles = next_particles

    @overrides
    def motion_update_prob(self, motion: Motion):
        """
        Perform motion for each particle
        """
        for i in range(len(self.__particles)):
            self.__particles[i].move(motion)

    @classmethod
    def from_params(cls, param: Param) -> 'Particle':
        return cls()
