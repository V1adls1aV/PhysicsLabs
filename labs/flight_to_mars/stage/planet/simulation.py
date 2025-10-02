from collections.abc import Generator

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.criteria import (
    did_rocket_left_the_planet,
    get_does_the_velocity_gap_increase_checker,
)


def simulate_flight(calculator: RocketFlightCalculator, sampling_delta: float) -> Generator[Rocket]:
    velocity_gap_checker = get_does_the_velocity_gap_increase_checker()
    rocket = calculator(sampling_delta)

    while not (
        did_rocket_left_the_planet(rocket, calculator.planet_mass)
        or velocity_gap_checker(rocket, calculator.planet_mass)
    ):
        rocket = calculator(sampling_delta)
        yield rocket
