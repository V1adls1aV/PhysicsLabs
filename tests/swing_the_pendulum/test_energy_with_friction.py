from math import radians
from statistics import mean

import pytest

from labs.swing_the_pendulum.model import PendulumState

from .data import (
    LIGHT_FRICTION,
    MEDIUM_FRICTION,
    SIMULATION_TIME,
    START_ANGLE,
    START_LENGTH,
    START_WEIGHT,
    get_pendulum,
)
from .util import run_simulation


@pytest.mark.parametrize(
    ("length", "weight", "angle", "friction_coefficient"),
    [
        (START_LENGTH, START_WEIGHT, START_ANGLE, LIGHT_FRICTION),
        (START_LENGTH, START_WEIGHT, START_ANGLE, MEDIUM_FRICTION),
        (0.5, START_WEIGHT, START_ANGLE, LIGHT_FRICTION),
        (2.0, START_WEIGHT, START_ANGLE, LIGHT_FRICTION),
        (START_LENGTH, START_WEIGHT, radians(1.0), LIGHT_FRICTION),
        (START_LENGTH, START_WEIGHT, radians(5.0), LIGHT_FRICTION),
        (START_LENGTH, 2.0, START_ANGLE, LIGHT_FRICTION),
        (START_LENGTH, 0.5, START_ANGLE, LIGHT_FRICTION),
    ],
)
def test_energy_decrease(
    length: float, weight: float, angle: float, friction_coefficient: float
) -> None:
    pendulum = get_pendulum(length=length, weight=weight, angle=angle)
    states, _ = run_simulation(
        pendulum, friction_coefficient=friction_coefficient, simulation_time=SIMULATION_TIME
    )

    for index in range(1, len(states) - 1):
        assert _sum_n_before(index, states) >= _sum_n_after(index, states)


def _sum_n_before(index: int, states: list[PendulumState], n: int = 10) -> float:
    return mean([states[i].full_energy for i in range(max(0, index - n), index)])


def _sum_n_after(index: int, states: list[PendulumState], n: int = 10) -> float:
    return mean([states[i].full_energy for i in range(index, min(index + n, len(states)))])
