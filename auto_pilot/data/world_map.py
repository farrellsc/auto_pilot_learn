import numpy as np


class WorldMap:
    def __init__(self):
        self.map = np.zeros()
        self.heuristic = None

    def from_file(self, path_to_map: str):
        pass

    def make_heuristic(self):
        """
        make a heuristic map for A*, stored in self.heuristic
        :return:
        """
        raise NotImplementedError