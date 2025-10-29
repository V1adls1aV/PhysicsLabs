from dataclasses import dataclass
from functools import cached_property

from labs.util.trigonometry import sin_rounded


@dataclass(frozen=True)
class Environment:
    """Basic class for environmental settings"""

    incline_angle: float
    friction_coefficient: float
    plane_length: float

    @cached_property
    def plane_height(self) -> float:
        return self.plane_length * sin_rounded(self.incline_angle)
