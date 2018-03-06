import numpy as np


class Coordinates:
    """
    This class describes a set of coordinates (x,y)
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = [x, y]

    def __add__(self, other):
        added = [self.coords[i] + other[i] for i in range(len(self.coords))]
        return Coordinates(*added)

    def __sub__(self, other):
        subtracted = [self.coords[i] - other[i] for i in range(len(self.coords))]
        return Coordinates(*subtracted)

    def __str__(self):
        return str(self.coords)

    def __mod__(self, num):
        moded = [self.coords[i] % num[i] for i in range(len(self.coords))]
        return Coordinates(*moded)

    def __getitem__(self, key):
        return self.coords[key]

    def __len__(self):
        return len(self.coords)

    def to_mat(self) -> np.matrix:
        """
        transform coordinates to numpy matrix for kalman filter
        """
        raise NotImplementedError
