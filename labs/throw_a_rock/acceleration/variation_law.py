from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class AccelerationVariationLaw:
    x: Callable[[float], float]
    y: Callable[[float], float]
