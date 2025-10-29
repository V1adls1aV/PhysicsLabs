from collections.abc import Generator

from ..model import Ball, Environment
from .calculator import Calculator


def is_simulation_finished(ball: Ball, env: Environment) -> bool:
    return ball.position >= env.plane_length


def simulate(calculator: Calculator, sampling_delta: float) -> Generator[Ball]:
    current_ball = calculator.current_ball
    yield current_ball

    while not is_simulation_finished(current_ball, calculator.env):
        current_ball = calculator(sampling_delta)
        yield current_ball
