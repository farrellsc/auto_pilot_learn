from auto_pilot.data.world_map import WorldMap
from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.common.param import Param
from overrides import overrides
from typing import List
from auto_pilot.data.coordinates import Coordinates


@RouteFinder.register("smoother")
class Smoother(RouteFinder):
    def __init__(self, weight_data: float, weight_smooth: float, tolerance: float):
        self.weight_data = weight_data
        self.weight_smooth = weight_smooth
        self.tolerance = tolerance

    @overrides
    def find_route(self, world_map: WorldMap, path: List[Coordinates]) -> WorldMap:
        """
        minimize diff(oldpath, newpath) + temporal diff of newpath
        :return: smoothed path
        """
        raise NotImplementedError

    @classmethod
    def from_params(cls, param: Param) -> 'Smoother':
        return cls()
