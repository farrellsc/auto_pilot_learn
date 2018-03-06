from auto_pilot.data.coordinates import Coordinates
import numpy as np


class WorldMap:
    """
    This class describes a grid cell world map.
    """
    def __init__(self, mat: np.matrix):
        self.map = mat
        self.heuristic = None
        self.shape = self.map.shape

    def from_file(self, path_to_map: str):
        pass

    def __getitem__(self, tup):
        x, y = tup
        return self.map[x, y]

    def make_heuristic(self, heuristic_type: str, goal: Coordinates):
        """
        make a heuristic map for A*, stored in self.heuristic
        :return:
        """
        raise NotImplementedError
