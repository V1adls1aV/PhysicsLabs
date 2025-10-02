from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any

import plotly.graph_objects as go

from labs.flight_to_mars.model.rocket import Rocket


def render_animation(
    rockets: Sequence[Rocket],
    rocket_shape_at: Callable,
    planets: list[dict[str, Any]],
    orbits: Iterable[dict[str, Any]] = (),
) -> go.Figure:
    """Create animated Plotly figure with frames for rocket flight."""
    max_x = max(max(rocket.x for rocket in rockets), max(planet["x"] for planet in planets))
    max_y = max(max(rocket.y for rocket in rockets), max(planet["y"] for planet in planets))
    x_range, y_range = _adjust_axies(max_x, max_y)

    frames = []
    for i, rocket in enumerate(rockets):
        rocket_shape = rocket_shape_at(x=rocket.x, y=rocket.y)
        frames.append(
            go.Frame(
                data=[],  # No data needed, shapes are in layout
                name=str(i),
                layout={"shapes": [*orbits, rocket_shape]},
            )
        )

    # Initial frame
    initial_rocket = rockets[0]
    initial_rocket_shape = rocket_shape_at(x=initial_rocket.x, y=initial_rocket.y)

    return go.Figure(
        data=[],  # No data needed, shapes are in layout
        frames=frames,
        layout={
            "shapes": [*orbits, initial_rocket_shape],
            "images": planets,
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
                            "args": [None, {"frame": {"duration": 5}}],
                        },
                    ],
                }
            ],
        },
    )


def _adjust_axies(x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Compute dynamic ranges to keep planet and rocket visible."""
    zoom = 1.1
    x_range = (-x * zoom, x * zoom)
    y_range = (-y * zoom, y * zoom)
    return x_range, y_range
