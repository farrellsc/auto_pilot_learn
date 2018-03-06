from auto_pilot.data.path import Path
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
    def find_route(self, world_map: WorldMap, path: Path) -> Path:
        """
        minimize diff(oldpath, newpath) + temporal diff of newpath
        :return: smoothed path
        """
        newpath = Path([Coordinates(path[col].x, path[col].y) for col in range(len(path))])
        change = self.tolerance
        while change >= self.tolerance:
            change = 0.0
            for i in range(1, len(path)-1):
                for j in range(len(path[0])):
                    aux = newpath[i][j]
                    newpath[i][j] += self.weight_data * (path[i][j] - newpath[i][j])
                    newpath[i][j] += self.weight_smooth * (newpath[i-1][j] + newpath[i+1][j] - 2 * newpath[i][j])
                    change += abs(aux - newpath[i][j])
        return newpath

    @classmethod
    def from_params(cls, param: Param) -> 'Smoother':
        weight_data: float = param.pop("weight_data")
        weight_smooth: float = param.pop("weight_smooth")
        tolerance: float = param.pop("tolerance")
        return cls(weight_data=weight_data, weight_smooth=weight_smooth, tolerance=tolerance)
