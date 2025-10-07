from __future__ import annotations

from labs.flight_to_mars.model.planet import Planet


def interplanetary_engine_off_equation(
    x: float,
    y: float,
    velocity_x: float,
    velocity_y: float,
    planets: list[Planet],
) -> list[float]:
    dxdt = velocity_x
    dydt = velocity_y

    planet_gravities = [planet.calculate_gravity(x, y) for planet in planets]

    dvxdt = sum(gravity.x for gravity in planet_gravities)
    dvydt = sum(gravity.y for gravity in planet_gravities)
    return [dxdt, dydt, dvxdt, dvydt]
