from labs.model.vector import Vector2D


def compute_next_point(current_point: Vector2D, velocity: Vector2D, time_delta: float) -> Vector2D:
    return current_point + Vector2D(velocity.x, velocity.y) * time_delta


def compute_grounding_point(current_point: Vector2D, velocity: Vector2D) -> Vector2D:
    grounding_time = current_point.y / -velocity.y
    x = current_point.x + velocity.x * grounding_time
    return Vector2D(x, y=0.0)


def compute_flight_time(
    trajectory_data: list[tuple[Vector2D, Vector2D]], sampling_delta: float
) -> float:
    """
    Compute approximate total flight time until ground contact.

    Uses linear interpolation for the final partial step.
    """
    if len(trajectory_data) < 2:
        return 0.0

    last_above_ground_point = trajectory_data[-2][0]
    velocity_at_last_step = trajectory_data[-1][1]

    residual_time = (
        last_above_ground_point.y / -velocity_at_last_step.y
        if velocity_at_last_step.y != 0
        else 0.0
    )

    return (len(trajectory_data) - 2) * sampling_delta + residual_time
