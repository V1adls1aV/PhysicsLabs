from labs.model.vector import Vector2D
from labs.throw_a_rock.motion.compute import compute_grounding_point, compute_next_point
from labs.throw_a_rock.velocity.calculator import VelocityCalculator


def simulate_flight(velocity_calculator: VelocityCalculator):
    previous_point = Vector2D(0.0, 0.0)
    yield previous_point
    velocity = velocity_calculator.initial_velocity
    point = compute_next_point(
        previous_point, velocity, velocity_calculator.sampling_delta
    )

    while point.y >= 0.0:
        yield point
        previous_point = point

        velocity = velocity_calculator()
        point = compute_next_point(
            previous_point, velocity, velocity_calculator.sampling_delta
        )

    yield compute_grounding_point(previous_point, velocity)
