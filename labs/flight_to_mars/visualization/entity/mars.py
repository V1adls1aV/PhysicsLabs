from typing import Any

from labs.flight_to_mars.visualization.entity.planet import planet_shape
from labs.model.constant import MARS_RADIUS


def mars_shape(x: float, y: float, radius: float = MARS_RADIUS) -> dict[str, Any]:
    return planet_shape("Mars.svg", x, y, radius)
