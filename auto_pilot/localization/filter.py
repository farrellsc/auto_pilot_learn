from auto_pilot.common.param import Param
from auto_pilot.data.motion import Motion
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.common.registrable import Registrable
from typing import TypeVar
import numpy as np

T = TypeVar('T')


class Filter(Registrable):
    def sensing_update_prob(self, *params) -> np.matrix:
        """
        Update the prob matrix based on newly observed info.
        :param info:
        :param prob_mat:
        :param world:
        :param
        :return:
        """
        raise NotImplementedError

    def motion_update_prob(self, *params) -> np.matrix:
        """
        Make prediction and update the prob matrix after motion.
        :param motion:
        :param prob_mat:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def from_params(cls, param: Param) -> 'Filter':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)
