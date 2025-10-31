from collections.abc import Generator

from ..model import PendulumState
from .calculator import AngleCalculator


def simulate(
    calculator: AngleCalculator, time_delta: float, simulation_time: float
) -> Generator[PendulumState, None, None]:
    yield calculator(0)
    time = 0.0

    while time <= simulation_time:
        state = calculator(time_delta)
        time = state.time
        yield state
