from dataclasses import dataclass
from functools import cached_property
from math import cos, sin


@dataclass(frozen=True)
class Ball:
    weight: float
    radius: float

    translational_velocity: float
    angular_velocity: float

    position: float
    angle: float

    def get_position_x(self, angle: float) -> float:
        return self.position * round(cos(angle), 15)

    def get_position_y(self, angle: float) -> float:
        return self.position * round(sin(angle), 15)

    @cached_property
    def moment_of_inertia(self) -> float:
        return 2 / 5 * self.weight * self.radius * self.radius
