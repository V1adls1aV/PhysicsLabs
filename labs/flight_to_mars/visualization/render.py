from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from labs.model.constant import EARTH_RADIUS


def render_frame(y: float, rocket: dict[str, Any], planet: dict[str, Any]) -> go.Figure:
    x_range, y_range = _adjust_axies(y)
    return go.Figure(
        layout={
            "shapes": [rocket],
            "images": [planet],
            "xaxis": {"range": x_range},
            "yaxis": {"range": y_range, "scaleanchor": "x", "scaleratio": 1},
        }
    )


def _adjust_axies(y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    # Compute dynamic ranges to keep planet and rocket visible
    x_range = (-EARTH_RADIUS * 0.2, EARTH_RADIUS * 0.2)
    y_range = (EARTH_RADIUS * 0.7, max(y + EARTH_RADIUS * 0.1, EARTH_RADIUS * 1.5))

    return x_range, y_range
