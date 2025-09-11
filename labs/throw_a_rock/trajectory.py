from labs.model.vector import Vector2D


def compute_next_point(
    current_point: Vector2D, velocity: Vector2D, time_delta: float
) -> Vector2D:
    return current_point + Vector2D(velocity.x, velocity.y) * time_delta


def compute_grounding_point(current_point: Vector2D, velocity: Vector2D) -> Vector2D:
    grounding_time = current_point.y / -velocity.y
    x = current_point.x + velocity.x * grounding_time
    return Vector2D(x, y=0.0)
