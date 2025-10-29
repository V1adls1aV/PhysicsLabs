r"""
Tests to check correctness of the algorithm.

Проверить, что скорость возрастания $\omega$ становится строго меньше при переходе к фазе без
проскальзывания ($\dot\omega_1 > \dot\omega_2$).
"""

import pytest

from labs.roll_the_ball.config import SAMPLING_DELTA
from labs.roll_the_ball.simulation import Calculator, simulate

from .data import (
    EPS,
    GRIPPING_INPUT,
    NON_FULLY_SLIPPING_INPUT,
    PLAIN_INPUT,
    SLIPPING_INPUT,
    PlainInput,
)
from .util import calculate_phase_transition_time


@pytest.mark.parametrize(
    "data", PLAIN_INPUT + NON_FULLY_SLIPPING_INPUT + GRIPPING_INPUT + SLIPPING_INPUT
)
def test_angular_acceleration_decreases_at_transition(data: PlainInput) -> None:
    calculator = Calculator(ball=data.ball, env=data.environment)
    balls = list(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    transition_time = calculate_phase_transition_time(
        data.ball.translational_velocity,
        data.environment.friction_coefficient,
        data.environment.incline_angle,
    )

    # Find indices around transition point
    transition_index = int(transition_time / SAMPLING_DELTA)

    # Look at a wider range around transition to find the actual change
    if 2 < transition_index < len(balls) - 2:
        # Find the last ball state with slippage (before transition)
        ball_slipping = None
        ball_rolling = None

        # Look backwards from transition to find slipping phase
        for i in range(transition_index, max(0, transition_index - 5), -1):
            ball = balls[i]
            velocity_diff = abs(ball.translational_velocity - ball.angular_velocity * ball.radius)
            if velocity_diff > EPS:  # Still slipping
                ball_slipping = ball
                break

        # Look forwards from transition to find rolling phase
        for i in range(transition_index, min(len(balls), transition_index + 5)):
            ball = balls[i]
            velocity_diff = abs(ball.translational_velocity - ball.angular_velocity * ball.radius)
            if velocity_diff < EPS:  # Now rolling
                ball_rolling = ball
                break

        if ball_slipping and ball_rolling:
            angular_accel_slipping = ball_slipping.angular_acceleration
            angular_accel_rolling = ball_rolling.angular_acceleration

            # Angular acceleration should decrease: $\dot\omega_1 > \dot\omega_2$
            assert angular_accel_slipping > angular_accel_rolling, (
                f"Angular acceleration should decrease at transition: "
                f"slipping={angular_accel_slipping:.6f} > rolling={angular_accel_rolling:.6f}"
            )
