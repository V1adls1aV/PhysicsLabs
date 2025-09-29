from typing import Any

from labs.flight_to_mars.visualization.entity.planet import planet_shape


def earth_shape(x: float, y: float, radius: float = 1.0) -> dict[str, Any]:
    return planet_shape("Earth.png", x, y, radius)
