from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.world_map import WorldMap
from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("dp")
class DP(RouteFinder):
    def __init__(self, delta, delta_name, cost):
        self.delta = delta
        self.cost = cost
        self.delta_name = delta_name

    def find_route(self, world_map: WorldMap, init: Coordinates, goal: Coordinates) -> WorldMap:
        """
        Find route using dynamic programming
        :return: WorldMap
        """
        value = [[99 for row in range(len(world_map[0]))] for col in range(len(world_map))]
        change = True
        while change:
            change = False
            for x in range(len(world_map)):
                for y in range(len(world_map[0])):
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
        return value

    @classmethod
    def from_params(cls, param: Param) -> 'DP':
        return cls()
