import math
from dataclasses import dataclass

from labs.model.constant import RELATIVE_PLANET_ORBIT_RADIUS, G
from labs.model.vector import Vector2D


@dataclass
class Planet:
    x: float
    y: float
    mass: float
    radius: float

    def calculate_gravity(self, x: float, y: float) -> Vector2D:
        """Calculate gravitational force."""
        distance_x = self.x - x
        distance_y = self.y - y
        distance = norm(distance_x, distance_y)

        if distance == 0:
            return Vector2D(0, 0)

        force_magnitude = G * self.mass / (distance * distance)
        return Vector2D(
            force_magnitude * (distance_x / distance), force_magnitude * (distance_y / distance)
        )

    @property
    def orbit_radius(self) -> float:
        return self.radius * RELATIVE_PLANET_ORBIT_RADIUS


def norm(x: float, y: float) -> float:
    return math.sqrt(x * x + y * y)
