from labs.model.constant import g
from labs.util.trigonometry import cos_rounded, sin_rounded

from ..model import Ball, Environment


def move_with_slippage(ball: Ball, env: Environment, time_delta: float) -> Ball:
    ball.translational_acceleration = (
        g * sin_rounded(env.incline_angle)
        - g * env.friction_coefficient * cos_rounded(env.incline_angle)
    )  # fmt: skip

    ball.angular_acceleration = (
        env.friction_coefficient
        * ball.mass
        * g
        * ball.radius
        * ball.radius
        * cos_rounded(env.incline_angle)
        / ball.rotational_inertia
    )

    return move_with_accelerations(ball=ball, time_delta=time_delta)


def move_without_slippage(ball: Ball, env: Environment, time_delta: float) -> Ball:
    ball.translational_acceleration = (
        ball.mass
        * g
        * sin_rounded(env.incline_angle)
        / (ball.mass + ball.rotational_inertia / ball.radius / ball.radius)
    )

    ball.angular_acceleration = ball.translational_acceleration / ball.radius

    return move_with_accelerations(ball=ball, time_delta=time_delta)


def move_with_accelerations(
    ball: Ball,
    time_delta: float,
) -> Ball:
    new_translational_velocity = (
        ball.translational_velocity + ball.translational_acceleration * time_delta
    )
    new_angular_velocity = ball.angular_velocity + ball.angular_acceleration * time_delta

    return Ball(
        mass=ball.mass,
        radius=ball.radius,
        translational_velocity=new_translational_velocity,
        angular_velocity=new_angular_velocity,
        position=ball.position + new_translational_velocity * time_delta,
        angle=ball.angle + new_angular_velocity * time_delta,
    )
