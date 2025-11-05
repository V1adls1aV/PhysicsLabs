from math import radians

import pytest

from .data import (
    LIGHT_FRICITON,
    MEDIUM_FRICITON,
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
        (START_LENGTH, START_WEIGHT, START_ANGLE, LIGHT_FRICITON),
        (START_LENGTH, START_WEIGHT, START_ANGLE, MEDIUM_FRICITON),
        (0.5, START_WEIGHT, START_ANGLE, LIGHT_FRICITON),
        (2.0, START_WEIGHT, START_ANGLE, LIGHT_FRICITON),
        (START_LENGTH, START_WEIGHT, radians(1.0), LIGHT_FRICITON),
        (START_LENGTH, START_WEIGHT, radians(5.0), LIGHT_FRICITON),
        (START_LENGTH, 2.0, START_ANGLE, LIGHT_FRICITON),
        (START_LENGTH, 0.5, START_ANGLE, LIGHT_FRICITON),
    ],
)
def test_energy_decrease(
    length: float, weight: float, angle: float, friction_coefficient: float
) -> None:
    pendulum = get_pendulum(length=length, weight=weight, angle=angle)
    states, _ = run_simulation(
        pendulum, friction_coefficient=friction_coefficient, simulation_time=SIMULATION_TIME
    )

    previous_energy = states[0].full_energy

    for state in states[1:]:
        assert state.full_energy <= previous_energy
        previous_energy = state.full_energy
