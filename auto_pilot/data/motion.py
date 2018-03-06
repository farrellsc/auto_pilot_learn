class Motion:
    def __init__(self, turning: float, distance: float):
        self.turning = turning
        self.distance = distance

    def to_F(self):
        """
        transform (turning, distance) to next_state_func in Kalman Filter
        :return:
        """
        raise NotImplementedError

