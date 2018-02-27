from typing import Callable, TypeVar, List

T = TypeVar('T')


class Registrable(object):
    reg_list = dict()

    @classmethod
    def register(cls, class_name: str) -> Callable:
        def register_inner(class_type: T) -> None:
            cls.reg_list[class_name] = class_type
        return register_inner

    @classmethod
    def list_available(cls) -> List[str]:
        return list(cls.reg_list.keys())

    @classmethod
    def by_name(cls, class_name: str) -> T:
        return cls.reg_list.get(class_name, None)
