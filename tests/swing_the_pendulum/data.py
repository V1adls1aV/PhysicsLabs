from math import radians

from labs.swing_the_pendulum.model import PendulumState

ABSOLUTE_PRECISION = 1.75e-4  # 0.01 degrees  (about 0.05% of 2 degrees)
RELATIVE_PRECISION = 5e-4  # 0.05%

START_ANGLE = radians(2.0)
START_LENGTH = 1.0
START_WEIGHT = 1.0

NO_FRICITON = 0.0
LIGHT_FRICITON = 0.1
MEDIUM_FRICITON = 1.0
HEAVY_FRICITON = 5.0
ENORMOUS_FRICITON = 10.0

SIMULATION_TIME = 10.0
SAMPLING_DELTA = 0.001


def get_pendulum(
    length: float = START_LENGTH, weight: float = START_WEIGHT, angle: float = START_ANGLE
) -> PendulumState:
    return PendulumState(length=length, weight=weight, angle=angle)


DEFAULT_PENDULUM = get_pendulum()
