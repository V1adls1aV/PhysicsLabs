from dataclasses import dataclass
from functools import cached_property

from labs.util.trigonometry import cos_rounded, sin_rounded

from .environment import Environment


@dataclass
class Ball:
    mass: float
    radius: float

    translational_velocity: float
    angular_velocity: float

    position: float = 0
    angle: float = 0

    # accelerations are computed inside movement and then assigned
    translational_acceleration: float = 0
    angular_acceleration: float = 0

    def get_position_x(self, env: Environment) -> float:
        return (
            (env.plane_length - self.position) * cos_rounded(env.incline_angle)
            - self.radius * sin_rounded(env.incline_angle)
        )  # fmt: skip

    def get_position_y(self, env: Environment) -> float:
        return (
            (env.plane_length - self.position) * sin_rounded(env.incline_angle)
            + self.radius * cos_rounded(env.incline_angle)
        )  # fmt: skip

    @cached_property
    def rotational_inertia(self) -> float:
        return 2 / 5 * self.mass * self.radius * self.radius
