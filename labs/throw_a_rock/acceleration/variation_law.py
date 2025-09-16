from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class AccelerationVariationLaw:
    x: AccelerationVariationLawByAxis
    y: AccelerationVariationLawByAxis


@dataclass
class AccelerationVariationLawByAxis:
    equation: Callable[[float], float]
    jacobian: Callable[[float], float]
