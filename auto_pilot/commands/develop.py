from auto_pilot.commands.subcommand import SubCommand
from auto_pilot.common.registrable import Registrable
from auto_pilot.vehicle.robot import Robot
from typing import Callable, TypeVar
import logging
T = TypeVar('T')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DevelopRegister(Registrable):
    develop_test_list = {}

    @classmethod
    def register(cls, class_name: str) -> Callable:
        def register_inner(class_type: T) -> None:
            cls.develop_test_list[class_name] = class_type
        return register_inner


class Develop(SubCommand):
    @classmethod
    def test_all(cls):
        logger.info("%d tests in total", len(DevelopRegister.develop_test_list))
        for func_name, func in DevelopRegister.develop_test_list.items():
            logger.info("running %s", func_name)
            func()
        logger.info("all(%d) tests passed", len(DevelopRegister.develop_test_list))

    @staticmethod
    @DevelopRegister.register("test_registrable")
    def test_registrable():
        available_classes = Registrable.list_available()
        assert "robot" in available_classes, "err, robot not in available_classes"
        assert len(available_classes) == 1, "err, len(available_classes) != 1"
