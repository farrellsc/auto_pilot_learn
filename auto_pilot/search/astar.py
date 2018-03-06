from auto_pilot.data.coordinates import Coordinates
from auto_pilot.data.world_map import WorldMap
from auto_pilot.common.util import ll_to_path
from auto_pilot.search.route_finder import RouteFinder
from auto_pilot.data.path import Path
from auto_pilot.common.param import Param
from overrides import overrides


@RouteFinder.register("astar")
class AStar(RouteFinder):
    def __init__(self, cost: float, heuristic_type: str):
        """
        delta and delta_name is a 4-element list, following the order of up, right, down, left
        """
        self.delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.delta_name = ["^", ">", "v", "<"]
        self.cost = cost
        self.heuristic_type = heuristic_type

    @overrides
    def find_route(self, world_map: WorldMap, init: Coordinates, goal: Coordinates) -> Path:
        """
        Find route using A*
        :return: WorldMap
        """
        world_map.make_heuristic(self.heuristic_type, goal)
        closed = [[0 for col in range(world_map.shape[0])] for row in range(world_map.shape[1])]
        closed[init.x][init.y] = 1
        expand = [[-1 for col in range(world_map.shape[0])] for row in range(world_map.shape[1])]

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

                if x == goal.x and y == goal.y:
                    found = True
                else:
                    for i in range(len(self.delta)):
                        x2 = x + self.delta[i][0]
                        y2 = y + self.delta[i][1]
                        if x2 >= 0 and x2 < world_map.shape[0] and y2 >= 0 and y2 < world_map.shape[1]:
                            if closed[x2][y2] == 0 and world_map[x2, y2] == 0:
                                g2 = g + self.cost
                                h2 = world_map.heuristic[x2][y2]
                                f2 = g2 + h2
                                stack.append([f2, g2, h2, x2, y2])
                                closed[x2][y2] = 1

        return ll_to_path(expand)

    @classmethod
    def from_params(cls, param: Param) -> 'AStar':
        cost: float = param.pop("cost")
        heuristic_type: str = param.pop("str")
        return cls(cost=cost, heuristic_type=heuristic_type)
