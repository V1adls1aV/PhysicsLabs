import pytest

from labs.rolling_the_ball.config import SAMPLING_DELTA
from labs.rolling_the_ball.model import Ball, Environment
from labs.rolling_the_ball.simulation import Calculator, simulate

from .data import EPS


@pytest.mark.parametrize("friction_coefficient", [0.1, 0.5, 1.0])
@pytest.mark.parametrize("initial_velocity", [1.0, 2.0, 3.0])
def test_zero_incline_uniform_motion_after_transition(
    friction_coefficient: float, initial_velocity: float
) -> None:
    environment = Environment(
        incline_angle=0.0,
        friction_coefficient=friction_coefficient,
        plane_length=20.0,
    )
    ball = Ball(
        mass=1.0,
        radius=0.1,
        translational_velocity=initial_velocity,
        angular_velocity=0.0,
    )

    calculator = Calculator(ball=ball, env=environment)
    balls = list(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    # Find the transition point where slippage ends
    # Use more relaxed tolerance for zero incline case
    transition_tolerance = 0.1
    transition_index = None
    for i, ball_state in enumerate(balls):
        velocity_diff = abs(
            ball_state.translational_velocity - ball_state.angular_velocity * ball_state.radius
        )
        if velocity_diff < transition_tolerance:  # Slippage has ended
            transition_index = i
            break

    assert transition_index is not None, (
        f"Slippage should end at some point. Last velocity diff: {velocity_diff:.6f}"
    )

    # Check that the translational velocity after transition is correct (theoretical value)
    # and that motion becomes uniform (constant velocity and zero acceleration) after transition.
    transition_velocity = balls[transition_index].translational_velocity
    for i in range(transition_index, len(balls)):
        ball_state = balls[i]

        # Translational velocity should remain constant and equal to value at transition
        assert abs(ball_state.translational_velocity - transition_velocity) < EPS, (
            f"Translational velocity after transition should remain constant."
            f"expected={transition_velocity:.6f}, actual={ball_state.translational_velocity:.6f}"
        )

        # Translational acceleration should be zero for uniform motion
        assert abs(ball_state.translational_acceleration) < EPS, (
            f"Translational acceleration should be zero for uniform motion: "
            f"accel={ball_state.translational_acceleration:.6f}"
        )

        # Angular acceleration should also be zero for uniform motion
        assert abs(ball_state.angular_acceleration) < EPS, (
            f"Angular acceleration should be zero for uniform motion: "
            f"accel={ball_state.angular_acceleration:.6f}"
        )
