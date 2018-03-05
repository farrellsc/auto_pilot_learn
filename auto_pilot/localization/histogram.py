from auto_pilot.localization.filter import Filter
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from overrides import overrides
import numpy as np
from typing import List


@Filter.register("histogram")
class Histogram(Filter):
    def __init__(self, match_prob: float, non_match_prob: List[float],
                 hit_prob: float, miss_prob: List[float]):
        self.__match_prob = None
        self.__non_match_prob = None
        self.__hit_prob = None
        self.__miss_prob = None

        self.set_noise(match_prob, non_match_prob, hit_prob, miss_prob)

    def set_noise(self, match_prob: float, non_match_prob: List[float], hit_prob: float, miss_prob: List[float]):
        assert sum([match_prob] + non_match_prob) == 1, "Histogram Filter sensing params should add up to 1"
        assert sum([hit_prob] + miss_prob) == 1, "Histogram Filter motion params should add up to 1"

        # sensing params
        self.__match_prob = match_prob
        self.__non_match_prob = non_match_prob
        # motion params
        self.__hit_prob = hit_prob
        self.__miss_prob = miss_prob

    @overrides
    def sensing_update_prob(self, info: SensorRet, prob_mat: np.matrix, world: WorldMap) -> np.matrix:
        """
        Update probability matrix by the similarity of new observation and world map.
        :return: normalized probability matrix
        """
        q = []
        for i in range(len(prob_mat)):
            for j in range(len(prob_mat[0])):
                hit = (info == world[i])
                q.append(prob_mat[i] * (hit * self.match_prob + (1 - hit) * self.non_match_prob))
        s = sum(q)
        for i in range(len(q)):
            q[i] = q[i] / s
        return q

    @overrides
    def motion_update_prob(self,  motion: Motion, prob_mat: np.matrix) -> np.matrix:
        """
        Update probability matrix by landing place prediction after motion.
        :return: non-normalized probability matrix
        """
        q = []
        for i in range(len(prob_mat)):
            s = self.hit_prob * prob_mat[(i - motion) % len(p)]
            s = s + pOvershoot * p[(i - U - 1) % len(p)]
            s = s + pUndershoot * p[(i - U + 1) % len(p)]
            q.append(s)
        return q

    @classmethod
    def from_params(cls, param: Param) -> 'Histogram':
        return cls()
