from dataclasses import dataclass
from functools import cached_property
from math import cos

from labs.model.constant import g

EPS = 1e-1


@dataclass(frozen=True)
class PendulumState:
    length: float
    weight: float

    angle: float
    angular_velocity: float = 0.0
    time: float = 0.0

    @cached_property
    def moment_of_inertia(self) -> float:
        return 1 / 3 * self.weight * self.length * self.length

    @cached_property
    def potential_energy(self) -> float:
        return self.length * self.weight * g * (1 - round(cos(self.angle), 15)) / 2

    @cached_property
    def rotational_energy(self) -> float:
        return self.moment_of_inertia * self.angular_velocity * self.angular_velocity / 2

    @cached_property
    def full_energy(self) -> float:
        return self.rotational_energy + self.potential_energy

    @cached_property
    def is_extreme(self) -> bool:
        return abs(self.angular_velocity) < EPS
