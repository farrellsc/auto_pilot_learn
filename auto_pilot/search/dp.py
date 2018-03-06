from auto_pilot.common.util import ll_to_path
from auto_pilot.data.path import Path
from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.world_map import WorldMap
from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("dp")
class DP(RouteFinder):
    def __init__(self, cost):
        self.delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.delta_name = ["^", ">", "v", "<"]
        self.cost = cost

    def find_route(self, world_map: WorldMap, init: Coordinates, goal: Coordinates) -> Path:
        """
        Find route using dynamic programming
        :return: WorldMap
        """
        value = [[99 for row in range(world_map.shape[0])] for col in range(world_map.shape[1])]
        change = True
        while change:
            change = False
            for x in range(world_map.shape[0]):
                for y in range(world_map.shape[1]):
                    if goal.x == x and goal.y == y:
                        if value[x][y] > 0:
                            value[x][y] = 0
                            change = True
                    elif world_map[x][y] == 0:
                        for a in range(len(self.delta)):
                            x2 = x + self.delta[a][0]
                            y2 = y + self.delta[a][1]
                            if x2 >= 0 and x2 < len(world_map) and y2 >= 0 and y2 < len(world_map[0]) \
                                and world_map[x2][y2] == 0:
                                v2 = value[x2][y2] + self.cost
                                if v2 < value[x][y]:
                                    change = True
                                    value[x][y] = v2
        return ll_to_path(value)

    @classmethod
    def from_params(cls, param: Param) -> 'DP':
        cost = param.pop("cost")
        return cls(cost=cost)
