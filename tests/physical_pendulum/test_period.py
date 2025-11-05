from math import radians

import pytest

from labs.physical_pendulum.calculations.util import (
    calculate_mean_period,
    calculate_theoretical_period,
)

from .data import (
    NO_FRICITON,
    SIMULATION_TIME,
    START_ANGLE,
    START_LENGTH,
    START_WEIGHT,
    get_pendulum,
)
from .util import almost_equal, run_simulation


@pytest.mark.parametrize(
    ("length", "weight", "angle"),
    [
        (START_LENGTH, START_WEIGHT, START_ANGLE),
        (0.5, START_WEIGHT, START_ANGLE),
        (2.0, START_WEIGHT, START_ANGLE),
        (START_LENGTH, START_WEIGHT, radians(1.0)),
        (START_LENGTH, START_WEIGHT, radians(5.0)),
        (START_LENGTH, 2.0, START_ANGLE),
        (START_LENGTH, 0.5, START_ANGLE),
    ],
)
def test_period_equality(length: float, weight: float, angle: float) -> None:
    pendulum = get_pendulum(length=length, weight=weight, angle=angle)
    _, extremes = run_simulation(
        pendulum, friction_coefficient=NO_FRICITON, simulation_time=SIMULATION_TIME
    )

    theoretical_period = calculate_theoretical_period(length)
    simulated_period = calculate_mean_period(extremes)

    assert almost_equal(simulated_period, theoretical_period)
