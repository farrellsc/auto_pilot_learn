from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.world_map import WorldMap
from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("astar")
class AStar(RouteFinder):
    def __init__(self, delta, delta_name, cost, heuristic_type):
        self.delta = delta
        self.cost = cost
        self.delta_name = delta_name
        self.heuristic_type = heuristic_type

    @overrides
    def find_route(self, world_map: WorldMap, init: Coordinates, goal: Coordinates) -> WorldMap:
        """
        Find route using A*
        :return: WorldMap
        """
        world_map.make_heuristic(self.heuristic_type)
        closed = [[0 for col in range(len(world_map[0]))] for row in range(len(world_map))]
        closed[init[0]][init[1]] = 1

        expand = [[-1 for col in range(len(world_map[0]))] for row in range(len(world_map))]
        action = [[-1 for col in range(len(world_map[0]))] for row in range(len(world_map))]

        x = init.x
        y = init.y
        g = 0
        h = world_map.heuristic[x][y]
        f = g + h

        stack = [[f, g, h, x, y]]

        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand
        count = 0

        while not found and not resign:
            if len(stack) == 0:
                resign = True
                return "Fail"
            else:
                stack.sort()
                stack.reverse()
                next_comb = stack.pop()
                x = next_comb[3]
                y = next_comb[4]
                g = next_comb[1]
                expand[x][y] = count
                count += 1

                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    for i in range(len(self.delta)):
                        x2 = x + self.delta[i][0]
                        y2 = y + self.delta[i][1]
                        if x2 >= 0 and x2 < len(world_map) and y2 >= 0 and y2 < len(world_map[0]):
                            if closed[x2][y2] == 0 and world_map[x2][y2] == 0:
                                g2 = g + self.cost
                                h2 = world_map.heuristic[x2][y2]
                                f2 = g2 + h2
                                stack.append([f2, g2, h2, x2, y2])
                                closed[x2][y2] = 1

        return expand

    @classmethod
    def from_params(cls, param: Param) -> 'AStar':
        return cls()
