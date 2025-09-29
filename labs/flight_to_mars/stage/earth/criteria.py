from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import EARTH_MASS, G


def does_rocket_left_the_earth(rocket: Rocket) -> bool:
    return rocket.velocity >= get_earth_escape_velocity(rocket.y)


def get_earth_escape_velocity(height: float) -> float:
    return (2 * G * EARTH_MASS / height) ** 0.5
