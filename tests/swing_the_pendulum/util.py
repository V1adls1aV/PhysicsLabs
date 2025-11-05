from labs.swing_the_pendulum.model import PendulumState
from labs.swing_the_pendulum.simulation import PendulumCalculator, simulate

from .data import (
    ABSOLUTE_PRECISION,
    NO_FRICTION,
    RELATIVE_PRECISION,
    SAMPLING_DELTA,
    SIMULATION_TIME,
)


def almost_equal(value: float, reference: float) -> bool:
    diff = abs(value - reference)
    max_value = max(abs(value), abs(reference))
    return diff < max(ABSOLUTE_PRECISION, RELATIVE_PRECISION * max_value)


def run_simulation(
    pendulum: PendulumState,
    *,
    friction_coefficient: float = NO_FRICTION,
    sampling_delta: float = SAMPLING_DELTA,
    simulation_time: float = SIMULATION_TIME,
) -> tuple[list[PendulumState], list[PendulumState]]:
    calculator = PendulumCalculator(
        initial_state=pendulum,
        friction_coefficient=friction_coefficient,
    )
    values, extremes = tuple(simulate(calculator, sampling_delta, simulation_time))
    return values, extremes
