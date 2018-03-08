from auto_pilot.data.world_map import WorldMap
from auto_pilot.robot.robot import Robot
from auto_pilot.robot.vehicle import Vehicle
from auto_pilot.data.motion import Motion
from auto_pilot.common.param import Param
from auto_pilot.localization.filter import Filter
from auto_pilot.localization.histogram import Histogram
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.common.test_case import zAutoPilotTestCase
import logging
from math import pi
import numpy as np

logger = logging.getLogger(__file__)


class TestHistogram(zAutoPilotTestCase):
    def setUp(self):
        world_size = [20, 20]
        self.info = SensorRet(np.matrix(np.random.randint(0, 10, [5, 5])))
        self.world_map = WorldMap(np.matrix(np.random.randint(0, 10, world_size)))
        self.prob_mat = np.matrix(np.ones(world_size))
        self.histogram_filter = Filter.from_params(Param({
            'type': 'histogram',
            'match_prob': 0.8,
            'hit_prob': 0.8,
            'miss_prob': [0.05 for _ in range(4)]
        }))

    def tearDown(self):
        pass

    def test_sensing_update(self):
        p = self.prob_mat
        p2 = self.histogram_filter.sensing_update_prob(self.info, self.prob_mat, self.world_map)
        print(p)
        print(p2)

    def test_moving_update(self):
        pass
