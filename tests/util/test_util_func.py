from auto_pilot.common.util import *
from auto_pilot.common.test_case import zAutoPilotTestCase
from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.data.coordinates import Coordinates
import numpy as np
from copy import deepcopy
import logging

logger = logging.getLogger(__file__)


class TestUtils(zAutoPilotTestCase):
    def test_region_similarity(self):
        observation = SensorRet(np.matrix(np.random.randint(0, 10, size=[5,5])))
        world_map = WorldMap(deepcopy(observation.data))
        assert region_similarity(observation, world_map, Coordinates(0, 0)) == 1.0
