# from scipy.integrate import ode

from labs.model.vector import Vector2D


def make_step(
    current_position: Vector2D, velocity: Vector2D, time_delta: float
) -> Vector2D:
    return current_position + Vector2D(velocity.x * time_delta, velocity.y * time_delta)


def calculate_next_velocity(velocity: Vector2D, time_delta: float) -> Vector2D:
    # time.sleep(0.2)
    return velocity + Vector2D(-1, -3) * time_delta
