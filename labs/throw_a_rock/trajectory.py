from labs.model.vector import Vector2D


def make_step(
    current_position: Vector2D, velocity: Vector2D, time_delta: float
) -> Vector2D:
    return current_position + Vector2D(velocity.x * time_delta, velocity.y * time_delta)


def compute_grounding_point(current_position: Vector2D, velocity: Vector2D) -> Vector2D:
    grounding_time = current_position.y / -velocity.y
    x = current_position.x + velocity.x * grounding_time
    return Vector2D(x, y=0.0)
