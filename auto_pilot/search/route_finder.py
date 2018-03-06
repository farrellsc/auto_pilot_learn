from auto_pilot.data.world_map import WorldMap
from auto_pilot.common.param import Param
from auto_pilot.data.path import Path
from auto_pilot.common.registrable import Registrable
from typing import TypeVar
T = TypeVar('T')


class RouteFinder(Registrable):
    def find_route(self, *params) -> Path:
        raise NotImplementedError

    @classmethod
    def from_params(cls, param: Param) -> 'RouteFinder':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)
