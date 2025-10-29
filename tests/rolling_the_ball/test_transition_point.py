import pytest

from labs.rolling_the_ball.config import SAMPLING_DELTA
from labs.rolling_the_ball.simulation import Calculator, simulate

from .data import (
    EPS,
    NON_FULLY_SLIPPING_INPUT,
    PLAIN_INPUT,
    PlainInput,
)
from .util import calculate_phase_transition_time


@pytest.mark.parametrize("data", PLAIN_INPUT + NON_FULLY_SLIPPING_INPUT)
def test_transition_point_accuracy(data: PlainInput) -> None:
    calculator = Calculator(ball=data.ball, env=data.environment)
    tuple(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    expected_time = calculate_phase_transition_time(
        data.ball.translational_velocity,
        data.environment.friction_coefficient,
        data.environment.incline_angle,
    )
    assert expected_time > 0

    actual_time = calculator.slippage_end_time
    assert actual_time is not None
    assert actual_time > 0
    assert abs(expected_time - actual_time) < EPS


@pytest.mark.parametrize("data", PLAIN_INPUT)
def test_slippage_ends_at_transition_point(data: PlainInput) -> None:
    calculator = Calculator(ball=data.ball, env=data.environment)
    balls = list(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    transition_time = calculate_phase_transition_time(
        data.ball.translational_velocity,
        data.environment.friction_coefficient,
        data.environment.incline_angle,
    )

    # Find the ball state closest to transition time
    transition_index = int(transition_time / SAMPLING_DELTA)
    if transition_index < len(balls):
        ball_at_transition = balls[transition_index]

        # At transition point, translational and angular velocities should be synchronized
        velocity_diff = abs(
            ball_at_transition.translational_velocity
            - ball_at_transition.angular_velocity * ball_at_transition.radius
        )

        # Use more relaxed tolerance due to discretization effects
        assert velocity_diff < 1e-1
