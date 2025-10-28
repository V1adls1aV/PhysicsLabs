from dataclasses import dataclass


@dataclass(frozen=True)
class Environment:
    """Basic class for environmental settings"""

    incline_angle: float
    friction_coefficient: float
    plane_length: float
