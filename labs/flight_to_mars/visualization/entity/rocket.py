from __future__ import annotations

from typing import Any

import numpy as np
from cachetools.func import lru_cache


def rocket_shape(
    x: float, y: float, angle: float, size: float = 0.2, color: str = "#ff4b4b"
) -> dict[str, Any]:
    rocket = move_shape(_rocket_shape(size), x, y, angle)
    path = "M " + " L ".join(f"{px} {py}" for px, py in rocket) + " Z"
    return {"type": "path", "path": path, "fillcolor": color, "line_color": color}


def move_shape(shape: np.ndarray, x: float, y: float, angle: float) -> np.ndarray:
    angle -= np.pi / 2
    cos, sin = np.cos(angle), np.sin(angle)
    rotation = np.array([[cos, -sin], [sin, cos]])
    return shape @ rotation.T + [x, y]


@lru_cache
def _rocket_shape(size: float) -> np.ndarray:
    w, s = size * 0.6, size
    return np.array(
        [
            [0.0,       1.8 * s],  # nose
            [0.45 * w,  0.8 * s],  # right shoulder
            [0.5 * w,   0.3 * s],
            [0.7 * s,   -0.30 * s],  # right fin tip
            [0.5 * w,   -0.25 * s],  # right fin root
            [0.0,       0.0],
            [-0.5 * w,  -0.25 * s],  # left fin root
            [-0.7 * s,  -0.30 * s],  # left fin tip
            [-0.5 * w,  0.3 * s],
            [-0.45 * w, 0.8 * s],  # left shoulder
        ]
    )  # fmt: skip
