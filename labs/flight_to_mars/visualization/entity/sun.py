from typing import Any

from labs.flight_to_mars.visualization.entity.planet import planet_shape
from labs.model.constant import SUN_RADIUS


def sun_shape(x: float, y: float, radius: float = SUN_RADIUS) -> dict[str, Any]:
    return planet_shape("Sun.png", x, y, radius)
