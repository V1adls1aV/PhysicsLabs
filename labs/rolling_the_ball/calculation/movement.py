from math import cos, sin

from labs.model.constant import g

from ..model import Ball, Environment


def move_with_slippage(ball: Ball, env: Environment, time_delta: float) -> Ball:
    translational_acceleration = g * sin(env.incline_angle) - g * env.friction_coefficient * round(
        cos(env.incline_angle), 15
    )

    angular_acceleration = (
        env.friction_coefficient
        * ball.weight
        * g
        * ball.radius
        * ball.radius
        * round(cos(env.incline_angle), 15)
        / ball.moment_of_inertia
    )

    new_translational_velocity = (
        ball.translational_velocity + translational_acceleration * time_delta
    )
    new_angular_velocity = ball.angular_velocity + angular_acceleration * time_delta

    return Ball(
        weight=ball.weight,
        radius=ball.radius,
        translational_velocity=new_translational_velocity,
        angular_velocity=new_angular_velocity,
        position=ball.position + new_translational_velocity * time_delta,
        angle=ball.angle + new_angular_velocity * time_delta,
    )


def move_without_slippage(ball: Ball, env: Environment, time_delta: float) -> Ball:
    translational_acceleration = (
        ball.weight
        * g
        * round(sin(env.incline_angle), 15)
        / (ball.weight + ball.moment_of_inertia / ball.radius / ball.radius)
    )

    angular_acceleration = translational_acceleration / ball.radius

    new_translational_velocity = (
        ball.translational_velocity + translational_acceleration * time_delta
    )
    new_angular_velocity = ball.angular_velocity + angular_acceleration * time_delta

    return Ball(
        weight=ball.weight,
        radius=ball.radius,
        translational_velocity=new_translational_velocity,
        angular_velocity=new_angular_velocity,
        position=ball.position + new_translational_velocity * time_delta,
        angle=ball.angle + new_angular_velocity * time_delta,
    )
