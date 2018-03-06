from math import pi, exp, sqrt


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
