from collections.abc import Callable

from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import G


def did_leave_the_planet(rocket: Rocket, planet_mass: float) -> bool:
    return rocket.velocity >= get_planet_escape_velocity(rocket.y, planet_mass)


def get_planet_escape_velocity(height: float, planet_mass: float) -> float:
    return (2 * G * planet_mass / height) ** 0.5


def get_does_the_velocity_gap_increase_checker() -> Callable[[Rocket, float], bool]:
    previous_gap = None

    def does_the_velocity_gap_increase(rocket: Rocket, planet_mass: float) -> bool:
        nonlocal previous_gap
        new_gap = get_planet_escape_velocity(rocket.y, planet_mass) - rocket.velocity

        if previous_gap is None:
            previous_gap = new_gap
            return False

        status = new_gap > previous_gap
        previous_gap = new_gap
        return status

    return does_the_velocity_gap_increase
