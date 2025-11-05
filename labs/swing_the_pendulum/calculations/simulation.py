from ..model import PendulumState
from .calculator import AngleCalculator


def simulate(
    calculator: AngleCalculator, time_delta: float, simulation_time: float
) -> tuple[list[PendulumState], list[PendulumState]]:
    time = 0.0

    states = []
    extremes = [calculator.initial_state]

    while time <= simulation_time:
        state = calculator(time_delta)
        time = state.time

        if (
            len(states) >= 2
            and (states[-1].angle - states[-2].angle) * (state.angle - states[-1].angle) < 0
        ):
            extremes.append(states[-1])
        states.append(state)

    return states, extremes
