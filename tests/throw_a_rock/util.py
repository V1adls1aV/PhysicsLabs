import math

from labs.model.enum import CorrelationType
from labs.model.vector import Vector2D
from labs.throw_a_rock.acceleration import acceleration_law_by_resistance_type
from labs.throw_a_rock.motion.simulation import simulate_flight
from labs.throw_a_rock.velocity import VelocityCalculator

from ..util import absolute_error_check, relative_error_check

SAMPLING_DELTA = 2 ** (-10)  # maximum in the ui

RELATIVE_ERROR = 10 ** (-3)  # 0.1%
ABSOLUTE_ERROR_TIME = 10 ** (-5)
ABSOLUTE_ERROR_DISTANCE = 10 ** (-5)


def compute_trajectory(
    initial_velocity: float,
    angle: float,
    resistance_type: CorrelationType,
) -> list[tuple[Vector2D, Vector2D]]:
    velocity_calculator = VelocityCalculator(
        initial_velocity=Vector2D.from_polar(initial_velocity, math.radians(angle)),
        acceleration_law=acceleration_law_by_resistance_type[resistance_type],
        sampling_delta=SAMPLING_DELTA,
    )
    return list(simulate_flight(velocity_calculator))


def assert_accuracy(
    flight_time: float,
    flight_distance: float,
    expected_flight_time: float,
    expected_flight_distance: float,
) -> None:
    assert any(
        (
            relative_error_check(flight_time, expected_flight_time, RELATIVE_ERROR),
            absolute_error_check(flight_time, expected_flight_time, ABSOLUTE_ERROR_TIME),
        )
    )
    assert any(
        (
            relative_error_check(flight_distance, expected_flight_distance, RELATIVE_ERROR),
            absolute_error_check(
                flight_distance, expected_flight_distance, ABSOLUTE_ERROR_DISTANCE
            ),
        )
    )
