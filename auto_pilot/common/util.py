from auto_pilot.data.world_map import WorldMap
from auto_pilot.data.senseRet import SensorRet
from auto_pilot.data.path import Path
from auto_pilot.data.coordinates import Coordinates
from math import pi, exp, sqrt
from typing import List


def angle_trunc(a):
    """
    helper function to map all angles onto [-pi, pi]
    """
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


def gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


def measurement_prob(measurement, sense_noise, landmarks):
    # calculates how likely a measurement should be
    x, y = measurement
    prob = 1.0
    for i in range(len(landmarks)):
        dist = sqrt((x - landmarks[i][0]) ** 2 + (y - landmarks[i][1]) ** 2)
        prob *= gaussian(dist, sense_noise, measurement[i])
    return prob


def region_similarity(observation: SensorRet, world_map: WorldMap, pos: Coordinates) -> float:
    """
    calculate the similarity ratio between observation and worldmap[i,j]
    return a float in range of [0,1]
    """
    raise NotImplementedError


def ll_to_path(map: List[List[int]]) -> Path:
    raise NotImplementedError
