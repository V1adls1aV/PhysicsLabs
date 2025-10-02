from collections.abc import Generator

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.space.calculator import RocketInterplanetaryFlightCalculator

from .criteria import does_reach_the_target, does_turn_back


def simulate_interplanetary_flight(
    calculator: RocketInterplanetaryFlightCalculator, sampling_delta: float, target_x: float
) -> Generator[Rocket]:
    rocket = calculator(sampling_delta)

    while not (does_reach_the_target(target_x, rocket) or does_turn_back(rocket)):
        rocket = calculator(sampling_delta)
        yield rocket
