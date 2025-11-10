import math

from labs.model.constant import g

from ..model import PendulumState


def calculate_mean_period(extremes: list[PendulumState]) -> float:
    return 2 * (extremes[-1].time - extremes[0].time) / (len(extremes) - 1)


def calculate_theoretical_period(pendulum_length: float) -> float:
    return 2 * math.pi * math.sqrt(2 * pendulum_length / (3 * g))
