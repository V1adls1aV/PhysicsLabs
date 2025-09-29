from collections.abc import Generator

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.earth.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.earth.criteria import (
    does_rocket_left_the_earth,
    does_the_velocity_gap_increase,
)


def simulate_flight(calculator: RocketFlightCalculator, sampling_delta: float) -> Generator[Rocket]:
    rocket = calculator(sampling_delta)

    while not (does_rocket_left_the_earth(rocket) or does_the_velocity_gap_increase(rocket)):
        rocket = calculator(sampling_delta)
        yield rocket
