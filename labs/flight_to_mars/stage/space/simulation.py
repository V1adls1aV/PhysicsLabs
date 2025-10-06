from collections.abc import Generator

from labs.flight_to_mars.model.planet import Planet
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.criteria import get_is_astronaut_dead_from_hunger_checker
from labs.flight_to_mars.stage.space.calculator import RocketInterplanetaryFlightCalculator
from labs.flight_to_mars.stage.space.criteria import did_reach_planet


def simulate_interplanetary_flight(
    calculator: RocketInterplanetaryFlightCalculator, sampling_delta: float, target_planet: Planet
) -> Generator[Rocket]:
    yield calculator(0)
    rocket = calculator(sampling_delta)
    is_astronaut_dead_from_hunger_checker = get_is_astronaut_dead_from_hunger_checker(
        sampling_delta
    )

    while not (did_reach_planet(target_planet, rocket) or is_astronaut_dead_from_hunger_checker()):
        rocket = calculator(sampling_delta)
        yield rocket
