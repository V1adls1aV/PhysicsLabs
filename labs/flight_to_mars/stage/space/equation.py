from labs.model.constant import (
    EARTH_MARS_DISTANCE,
    EARTH_MASS,
    MARS_MASS,
    SUN_EARTH_DISTANCE,
    SUN_MASS,
    G,
)


def interplanetary_engine_off_equation(
    x: float,
    y: float,
    velocity_x: float,
    velocity_y: float,
) -> list[float]:
    dxdt = velocity_x
    dydt = velocity_y
    dvxdt = mars_g(x) - earth_g(x) - sun_g(x)
    dvydt = mars_g(y) - earth_g(y) - sun_g(y)
    return [dxdt, dydt, dvxdt, dvydt]


def earth_g(x: float) -> float:
    return G * EARTH_MASS / (x * x)


def mars_g(x: float) -> float:
    return G * MARS_MASS / (EARTH_MARS_DISTANCE - x) ** 2


def sun_g(x: float) -> float:
    return G * SUN_MASS / (SUN_EARTH_DISTANCE + x) ** 2
