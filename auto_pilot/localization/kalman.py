from auto_pilot.localization.filter import Filter
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from overrides import overrides
import numpy as np
from typing import Tuple


@Filter.register("kalman")
class Kalman(Filter):
    def __init__(self, identity_mat, measurement_func, external_motion, measurement_uncertainty):
        self.__identity_mat = identity_mat
        self.__measurement_func = measurement_func

        self.__external_motion = None
        self.__measurement_uncertainty = None
        self.set_noise(external_motion, measurement_uncertainty)

    def set_noise(self, external_motion, measurement_uncertainty):
        self.__external_motion = external_motion
        self.__measurement_uncertainty = measurement_uncertainty

    @overrides
    def sensing_update_prob(self, info: Coordinates, current_state: np.matrx,
                            current_uncertainty: np.matrx) -> Tuple[np.matrix, np.matrix]:
        """
        Update input state and uncertainty with newly observed location
        :return:
        """
        error_mat = info.to_mat() - self.__measurement_func * current_state
        S = self.__measurement_func * current_uncertainty * self.__measurement_func.transpose()\
            + self.__measurement_uncertainty
        kalman_gain = current_uncertainty * self.__measurement_func.transpose() * S.inverse()

        next_state = current_state + kalman_gain * error_mat
        next_uncertainty = (self.__identity_mat - kalman_gain * self.__measurement_func) * current_uncertainty
        return next_state, next_uncertainty

    @overrides
    def motion_update_prob(self, motion: Motion, current_state: np.matrx,
                           current_uncertainty: np.matrx) -> Tuple[np.matrix, np.matrix]:
        """
        Update input state by motion then return state and uncertainty
        :return:
        """
        next_state_func = motion.to_F()
        next_state = next_state_func * current_state + self.__external_motion
        next_uncertainty = next_state_func * current_uncertainty * next_state_func.transpose()
        return next_state, next_uncertainty

    @classmethod
    def from_params(cls, param: Param) -> 'Kalman':
        return cls()

