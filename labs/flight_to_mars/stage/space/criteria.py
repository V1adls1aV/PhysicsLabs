from labs.flight_to_mars.model.planet import Planet
from labs.flight_to_mars.model.rocket import Rocket


def did_reach_the_target(target_x: float, rocket: Rocket) -> bool:
    return target_x <= rocket.x


def did_turn_back(rocket: Rocket) -> bool:
    return rocket.velocity_x < 0


def did_reach_planet(planet: Planet, rocket: Rocket) -> bool:
    return (rocket.x - planet.x) ** 2 + (rocket.y - planet.y) ** 2 <= (1.5 * planet.radius) ** 2
