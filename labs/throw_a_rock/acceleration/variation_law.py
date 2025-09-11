from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class AccelerationVariationLaw:
    x: AccelerationVariationLawByAxis
    y: AccelerationVariationLawByAxis


@dataclass
class AccelerationVariationLawByAxis:
    equation: Callable[[float], float]
    jacobian: Callable[[float], float]
