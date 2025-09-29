from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import plotly.graph_objects as go

from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import EARTH_RADIUS


def render_animation(
    rockets: Sequence[Rocket], rocket_shape_at: Callable, planet: dict[str, Any]
) -> go.Figure:
    """Create animated Plotly figure with frames for rocket flight."""
    max_y = max(rocket.y for rocket in rockets) if rockets else EARTH_RADIUS
    x_range, y_range = _adjust_axies(max_y)

    frames = []
    for i, rocket in enumerate(rockets):
        # Create frame with updated rocket shape
        rocket_shape = rocket_shape_at(y=rocket.y)
        frames.append(
            go.Frame(
                data=[],  # No data needed, shapes are in layout
                name=str(i),
                layout={"shapes": [rocket_shape]},
            )
        )

    # Initial frame
    initial_rocket = rockets[0] if rockets else Rocket(0, 0, 0, 0, 0, 0)
    initial_rocket_shape = rocket_shape_at(y=initial_rocket.y)

    return go.Figure(
        data=[],  # No data needed, shapes are in layout
        frames=frames,
        layout={
            "shapes": [initial_rocket_shape],
            "images": [planet],
            "xaxis": {"range": x_range},
            "yaxis": {"range": y_range, "scaleanchor": "x", "scaleratio": 1},
            "updatemenus": [
                {
                    "type": "buttons",
                    "showactive": False,
                    "buttons": [
                        {
                            "label": "Play",
                            "method": "animate",
                            "args": [None, {"frame": {"duration": 100}}],
                        },
                        {
                            "label": "Pause",
                            "method": "animate",
                            "args": [[None], {"frame": {"duration": 0}}],
                        },
                    ],
                }
            ],
        },
    )


def _adjust_axies(y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Compute dynamic ranges to keep planet and rocket visible."""
    x_range = (-EARTH_RADIUS * 0.1, EARTH_RADIUS * 0.1)
    y_range = (EARTH_RADIUS * 0.8, max(y + EARTH_RADIUS * 0.1, EARTH_RADIUS * 1.1))
    return x_range, y_range
