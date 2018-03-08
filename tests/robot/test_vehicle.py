from auto_pilot.robot.robot import Robot
from auto_pilot.robot.vehicle import Vehicle
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from auto_pilot.common.test_case import zAutoPilotTestCase
import logging
from math import pi

logger = logging.getLogger(__file__)


class TestVehicle(zAutoPilotTestCase):
    def test_from_param(self):
        params = Param({
            'type': 'vehicle',
            'x': 0,
            'y': 0,
            'orientation': 0
        })

        v1 = Robot.from_params(params)
        assert v1.x == 0
        assert v1.y == 0
        assert v1.orientation == 0

    def test_move_sense(self):
        params = Param({
            'type': 'vehicle',
            'x': 0,
            'y': 0,
            'orientation': 0,
            'drift': 0,
            'turning_noise': 0,
            'distance_noise': 0,
            'measurement_noise': 0
        })

        v1 = Robot.from_params(params)
        v1.move(Motion(pi/2, 10))
        c = v1.sense()
        assert round(c.x) == 0
        assert round(c.y) == 10
