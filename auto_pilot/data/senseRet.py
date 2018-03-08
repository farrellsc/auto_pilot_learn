import numpy as np


class SensorRet:
    """
    This class describes the landscape at a set of coordinates.
    """
    def __init__(self, mat: np.matrix):
        self.data = mat
