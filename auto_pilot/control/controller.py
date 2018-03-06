from auto_pilot.common.param import Param
from auto_pilot.common.registrable import Registrable
from auto_pilot.data.coordinates import Coordinates
from typing import TypeVar, List
T = TypeVar('T')


class Controller(Registrable):
    def run(self, n, speed) -> List[Coordinates]:
        """
        Wrap up robot, control it to follow the planned route.
        :param n: number of steps
        :param speed:
        :return:
        """
        raise NotImplementedError

    @classmethod
    def from_params(cls, param: Param) -> 'Controller':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)
