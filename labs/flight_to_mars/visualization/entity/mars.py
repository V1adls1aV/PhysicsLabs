from typing import Any

from labs.flight_to_mars.visualization.entity.planet import planet_shape


def mars_shape(x: float, y: float, radius: float = 1.0) -> dict[str, Any]:
    return planet_shape("Mars.png", x, y, radius)
