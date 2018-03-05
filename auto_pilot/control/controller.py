from auto_pilot.common.param import Param
from auto_pilot.common.registrable import Registrable
from typing import TypeVar
T = TypeVar('T')


class Controller(Registrable):
    @classmethod
    def from_params(cls, param: Param) -> 'Controller':
        class_choice = param.pop("type")
        return Registrable.by_name(class_choice).from_params(param)
