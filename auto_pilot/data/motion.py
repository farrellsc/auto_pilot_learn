class Motion:
    """
    TODO: add new class 'transition' for to_F
    """
    def __init__(self, turning: float, speed: float):
        self.turning = turning
        self.speed = speed

    def to_F(self):
        """
        transform (turning, distance) to next_state_func in Kalman Filter
        :return:
        """
        raise NotImplementedError