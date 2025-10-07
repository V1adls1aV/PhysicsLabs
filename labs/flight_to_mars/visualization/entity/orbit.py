from typing import Any

from labs.model.vector import Vector2D


def orbit_shape(center: Vector2D, semi_major: float, semi_minor: float) -> dict[str, Any]:
    """Create ellipse shape dict for Plotly orbit visualization."""
    return {
        "type": "circle",
        "xref": "x",
        "yref": "y",
        "x0": center.x - semi_major,
        "y0": center.y - semi_minor,
        "x1": center.x + semi_major,
        "y1": center.y + semi_minor,
        "line": {"color": "rgba(255,255,255,0.1)", "width": 1},
        "fillcolor": "rgba(0,0,0,0)",
    }
