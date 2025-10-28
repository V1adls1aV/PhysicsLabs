from functools import lru_cache
from math import tan

from ..model import Ball, Environment

EPS = 1e-1


@lru_cache
def is_movement_without_slippage_possible(env: Environment) -> bool:
    return env.friction_coefficient >= 2 / 7 * round(tan(env.incline_angle), 15)


def is_slippage_finished(ball: Ball) -> bool:
    return abs(ball.translational_velocity - ball.angular_velocity * ball.radius) < EPS
