from labs.physical_pendulum.calculations import AngleCalculator, simulate
from labs.physical_pendulum.model import PendulumState

from .data import NO_FRICITON, PRECISION, SAMPLING_DELTA, SIMULATION_TIME


def almost_equal(value: float, reference: float) -> bool:
    return abs(value - reference) < PRECISION


def run_simulation(
    pendulum: PendulumState,
    *,
    friction_coefficient: float = NO_FRICITON,
    sampling_delta: float = SAMPLING_DELTA,
    simulation_time: float = SIMULATION_TIME,
) -> tuple[list[PendulumState], list[PendulumState]]:
    calculator = AngleCalculator(
        initial_state=pendulum,
        friction_coefficient=friction_coefficient,
    )
    values, extremes = tuple(simulate(calculator, sampling_delta, simulation_time))
    return values, extremes
