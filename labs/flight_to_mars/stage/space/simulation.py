from collections.abc import Generator

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.criteria import get_is_astronaut_dead_from_hunger_checker
from labs.flight_to_mars.stage.space.calculator import RocketInterplanetaryFlightCalculator

from .criteria import did_reach_the_target, did_turn_back


def simulate_interplanetary_flight(
    calculator: RocketInterplanetaryFlightCalculator, sampling_delta: float, target_x: float
) -> Generator[Rocket]:
    yield calculator(0)
    rocket = calculator(sampling_delta)
    is_astronaut_dead_from_hunger_checker = get_is_astronaut_dead_from_hunger_checker()

    while not (
        did_reach_the_target(target_x, rocket)
        or did_turn_back(rocket)
        or is_astronaut_dead_from_hunger_checker()
    ):
        rocket = calculator(sampling_delta)
        yield rocket
