from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property

import pandas as pd


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    @classmethod
    def from_polar(cls, norm: float, angle: float) -> Vector2D:
        return Vector2D(norm * math.cos(angle), norm * math.sin(angle))

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame({"x": [self.x], "y": [self.y]})

    @cached_property
    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Vector2D:
        return Vector2D(self.x * other, self.y * other)

    def __matmul__(self, other: Vector2D) -> float:
        return self.x * other.x + self.y * other.y


def vectors_to_df(vectors: Iterable[Vector2D]) -> pd.DataFrame:
    return pd.DataFrame({"x": [v.x for v in vectors], "y": [v.y for v in vectors]})
