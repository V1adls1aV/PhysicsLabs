from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class PendulumState:
    length: float
    weight: float
    angle: float
    time: float = 0.0

    @cached_property
    def moment_of_inertia(self) -> float:
        return 1 / 3 * self.weight * self.length * self.length
