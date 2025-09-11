from labs.model.vector import Vector2D


def compute_next_velocity(velocity: Vector2D, time_delta: float) -> Vector2D:
    return velocity + Vector2D(-1, -3) * time_delta
