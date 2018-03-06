from auto_pilot.localization.filter import Filter
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.data.motion import Motion
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.common.param import Param
from auto_pilot.common.util import region_similarity
from overrides import overrides
import numpy as np
from typing import List


@Filter.register("histogram")
class Histogram(Filter):
    """
    discrete, 2D
    """
    def __init__(self, match_prob: float, non_match_prob: List[float],
                 hit_prob: float, miss_prob: List[float]):
        self.__match_prob = None
        self.__non_match_prob = None
        self.__hit_prob = None
        self.__miss_prob = None

        self.set_noise(match_prob, non_match_prob, hit_prob, miss_prob)

    @overrides
    def set_noise(self, match_prob: float, hit_prob: float, miss_prob: List[float]):
        """
        miss_prob is a 4-element list, following the order of up, right, down, left
        """
        assert sum([hit_prob] + miss_prob) == 1, "Histogram Filter motion params should add up to 1"

        # sensing params
        self.__match_prob = match_prob
        # motion params
        self.__hit_prob = hit_prob
        self.__miss_prob = miss_prob

    @overrides
    def sensing_update_prob(self, info: SensorRet, prob_mat: np.matrix, world: WorldMap) -> np.matrix:
        """
        Update probability matrix by the similarity of new observation and world map.
        :return: normalized probability matrix
        """
        q = np.matrix(np.zeros(prob_mat.shape))
        for i in range(len(prob_mat)):
            for j in range(len(prob_mat[0])):
                sim = region_similarity(info, world, Coordinates(i, j))
                q[i, j] = prob_mat[i, j] * sim * self.match_prob
        return q/q.sum()

    @overrides
    def motion_update_prob(self,  motion: Motion, prob_mat: np.matrix) -> np.matrix:
        """
        Update probability matrix by landing place prediction after motion.
        :return: non-normalized probability matrix
        """
        q = np.matrix(np.zeros(prob_mat.shape))
        for i in range(len(prob_mat)):
            for j in range(len(prob_mat[0])):
                s = self.hit_prob * prob_mat[(Coordinates(i, j) - motion) % prob_mat.shape]
                for index, bias in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                    s += self.__miss_prob[index] * \
                         prob_mat[(Coordinates(i, j) - motion - Coordinates(bias[0], bias[1])) % prob_mat.shape]
                q[i, j] = s
        return q

    @classmethod
    def from_params(cls, param: Param) -> 'Histogram':
        match_prob: float = param.pop("match_prob")
        non_match_prob: List[float] = param.pop("non_match_prob")
        hit_prob: float = param.pop("hit_prob")
        miss_prob: List[float] = param.pop("miss_prob")
        return cls(
            match_prob=match_prob, non_match_prob=non_match_prob, hit_prob=hit_prob, miss_prob=miss_prob
        )
