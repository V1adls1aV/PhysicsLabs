from typing import Any

from labs.flight_to_mars.visualization.entity.planet import planet_shape
from labs.model.constant import EARTH_RADIUS


def earth_shape(x: float, y: float) -> dict[str, Any]:
    return planet_shape("Earth.svg", x, y, EARTH_RADIUS)
