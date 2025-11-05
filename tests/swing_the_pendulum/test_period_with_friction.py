from math import radians

import pytest

from labs.swing_the_pendulum.calculations.util import calculate_mean_period

from .calculations import run_theoretical_simulation
from .data import (
    LIGHT_FRICITON,
    MEDIUM_FRICITON,
    SIMULATION_TIME,
    START_ANGLE,
    START_LENGTH,
    START_WEIGHT,
    get_pendulum,
)
from .util import almost_equal, run_simulation


@pytest.mark.parametrize(
    ("length", "weight", "angle", "friction_coefficient"),
    [
        (START_LENGTH, START_WEIGHT, START_ANGLE, LIGHT_FRICITON),
        (START_LENGTH, START_WEIGHT, START_ANGLE, MEDIUM_FRICITON),
        (0.5, START_WEIGHT, radians(1.0), LIGHT_FRICITON),
        (2.0, START_WEIGHT, START_ANGLE, LIGHT_FRICITON),
        (2.0, START_WEIGHT, radians(3.0), LIGHT_FRICITON),
        (START_LENGTH, START_WEIGHT, radians(1.0), LIGHT_FRICITON),
        (START_LENGTH, 2.0, START_ANGLE, LIGHT_FRICITON),
        (START_LENGTH, 0.5, START_ANGLE, LIGHT_FRICITON),
    ],
)
def test_period_equality_with_friction(
    length: float, weight: float, angle: float, friction_coefficient: float
) -> None:
    pendulum = get_pendulum(length=length, weight=weight, angle=angle)
    simulated_states, simulated_extremes = run_simulation(
        pendulum, friction_coefficient=friction_coefficient, simulation_time=SIMULATION_TIME
    )
    theoretical_states, theoretical_extremes = run_theoretical_simulation(
        pendulum, friction_coefficient=friction_coefficient, simulation_time=SIMULATION_TIME
    )

    simulated_period = calculate_mean_period(simulated_extremes)
    theoretical_period = calculate_mean_period(theoretical_extremes)

    assert almost_equal(simulated_period, theoretical_period)

    for simulated_state, theoretical_state in zip(
        simulated_states, theoretical_states, strict=True
    ):
        assert almost_equal(simulated_state.angle, theoretical_state.angle)
