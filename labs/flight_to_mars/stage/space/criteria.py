from collections.abc import Callable

from labs.flight_to_mars.model.planet import Planet
from labs.flight_to_mars.model.rocket import Rocket


def did_reach_the_target(target_x: float, rocket: Rocket) -> bool:
    return target_x <= rocket.x


def did_turn_back(rocket: Rocket) -> bool:
    return rocket.velocity_x < 0


def get_planet_reach_checker(planet: Planet) -> Callable[[Rocket], bool]:
    previous_rocket = None

    def did_reach_planet(rocket: Rocket) -> bool:
        nonlocal previous_rocket
        # Line-circle intersection check if we have previous rocket
        if previous_rocket is not None and check_planet_reach(previous_rocket, rocket, planet):
            previous_rocket = rocket
            return True

        previous_rocket = rocket
        return False

    return did_reach_planet


def check_planet_reach(previous_rocket: Rocket, rocket: Rocket, planet: Planet) -> bool:
    return _line_intersects_circle(
        previous_rocket.x,
        previous_rocket.y,
        rocket.x,
        rocket.y,
        planet.x,
        planet.y,
        planet.radius * 50,
    )


def _line_intersects_circle(
    x1: float, y1: float, x2: float, y2: float, cx: float, cy: float, radius: float
) -> bool:
    """
    Check if line segment from (x1,y1) to (x2,y2) intersects circle at (cx,cy) with given radius.
    """
    # Vector from point 1 to point 2
    dx = x2 - x1
    dy = y2 - y1

    # Vector from point 1 to circle center
    fx = x1 - cx
    fy = y1 - cy

    # Quadratic equation coefficients for line-circle intersection
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return False

    # Check if intersection points are within line segment
    sqrt_discriminant = discriminant**0.5
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)

    return (0 <= t1 <= 1) or (0 <= t2 <= 1)
