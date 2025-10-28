from math import cos, sin

from labs.model.constant import g


def calculate_phase_transition_time(
    initial_velocity: float, friction_coefficient: float, incline_angle: float
) -> float:
    return initial_velocity / (
        g * (2 / 7 * friction_coefficient * cos(incline_angle) - sin(incline_angle))
    )


def calculate_angular_velocity(
    initial_velocity: float,
    friction_coefficient: float,
    incline_angle: float,
    radius: float,
    time: float,
) -> float:
    if time <= calculate_phase_transition_time(
        initial_velocity, friction_coefficient, incline_angle
    ):
        return friction_coefficient * g * cos(incline_angle) * time / (2 / 5 * radius)
    raise ValueError("For case without slippage calculation is not implemented yet.")


def calculate_translational_velocity(
    initial_velocity: float, friction_coefficient: float, incline_angle: float, time: float
) -> float:
    return (
        initial_velocity
        + g * (sin(incline_angle) - friction_coefficient * cos(incline_angle)) * time
    )
