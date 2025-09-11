from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd


@dataclass
class Vector2D:
    x: float
    y: float

    @classmethod
    def from_polar(cls, norm: float, angle: float) -> Vector2D:
        return Vector2D(norm * math.cos(angle), norm * math.sin(angle))

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame({"x": [self.x], "y": [self.y]})

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Vector2D:
        return Vector2D(self.x * other, self.y * other)

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError


def vectors_to_df(vectors: list[Vector2D]) -> pd.DataFrame:
    return pd.DataFrame({"x": [v.x for v in vectors], "y": [v.y for v in vectors]})


def get_last_vector(data: pd.DataFrame) -> Vector2D:
    row = data.iloc[-1]
    return Vector2D(row.name, row.y)
