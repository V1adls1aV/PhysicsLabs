from __future__ import annotations

from typing import Any

import plotly.graph_objects as go


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
    # Compute dynamic ranges to keep planet (radius=1 at origin) and rocket visible
    visual_margin = 0.5
    y_min = min(-1.0, y - visual_margin)
    y_max = max(1.0, y + visual_margin)
    y_span = y_max - y_min

    # Maintain 1:1 scale and at least initial x-span
    x_half_span = max(2.0, y_span / 2.0)
    x_range = (-x_half_span, x_half_span)
    y_range = (y_min, y_max)

    return x_range, y_range
