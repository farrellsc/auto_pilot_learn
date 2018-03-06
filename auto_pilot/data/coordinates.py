import numpy as np


class Coordinates:
    """
    This class describes a set of coordinates (x,y)
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_mat(self) -> np.matrix:
        """
        transform coordinates to numpy matrix for kalman filter
        """
        raise NotImplementedError
