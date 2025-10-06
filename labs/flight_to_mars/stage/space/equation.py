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
    velocity: float,
) -> list[float]:
    dhdt = velocity
    dvdt = mars_g_by_x(x) - earth_g_by_x(x) - sun_g_by_x(x)
    return [dhdt, dvdt]


def earth_g_by_x(x: float) -> float:
    return 0
    return G * EARTH_MASS / (x * x)


def mars_g_by_x(x: float) -> float:
    return G * MARS_MASS / (EARTH_MARS_DISTANCE - x) ** 2


def sun_g_by_x(x: float) -> float:
    return G * SUN_MASS / (SUN_EARTH_DISTANCE + x) ** 2
