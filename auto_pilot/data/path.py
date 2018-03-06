from auto_pilot.data.coordinates import Coordinates
from typing import List


class Path:
    def __init__(self, path: List[Coordinates]):
        self.path = path

    def __getitem__(self, key):
        return self.path[key]

    def __len__(self):
        return len(self.path)
