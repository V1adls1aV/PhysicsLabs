import math
from collections.abc import Sequence

from plotly.graph_objects import Figure, Frame

from ..model import Ball, Environment


def _circle_bbox(
    center_x: float, center_y: float, radius: float
) -> tuple[float, float, float, float]:
    """Return (x0, y0, x1, y1) for a plotly circle shape."""
    return center_x - radius, center_y - radius, center_x + radius, center_y + radius


def render_ball_animation(
    balls: Sequence[Ball],
    env: Environment,
    *,
    frame_duration: int = 3,
    dot_fraction: float = 0.5,
) -> Figure:
    """
    Create a Plotly animation showing the ball rolling on the incline.

    Args:
        balls: sequence of Ball snapshots (time-ordered).
        env: environment with incline.
        frame_duration: ms per frame.
        dot_fraction: relative size of the rim-dot compared to ball radius.
    """
    # plane endpoints
    theta = env.incline_angle
    x_end = env.plane_length * math.cos(theta)
    y_end = env.plane_height

    # axes ranges - include plane and ball radius
    max_coord = max(env.plane_length, *(b.position + b.radius for b in balls))
    pad = max_coord * 0.05 + max(b.radius for b in balls)
    x_range = (-pad, x_end + pad)
    y_range = (-pad, max(y_end, *(b.get_position_y(env) for b in balls)) + pad)

    # top-level layout: static plane drawn once
    plane_shape = {
        "type": "line",
        "x0": 0 - 0.64 * balls[0].radius,
        "y0": y_end,
        "x1": x_end - 0.64 * balls[0].radius,
        "y1": 0,
        "line": {"width": 2, "color": "gray"},
    }

    # initial ball (first frame)
    first = balls[0]
    cx = first.get_position_x(env)
    cy = first.get_position_y(env)
    r = first.radius

    x0, y0, x1, y1 = _circle_bbox(cx, cy, r)
    ball_shape_initial = {
        "type": "circle",
        "xref": "x",
        "yref": "y",
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "line": {"color": "white"},
        "fillcolor": "rgba(255,255,255,0.1)",
    }

    # dot (rim indicator) initial coords
    dot_r = r * dot_fraction
    dot_angle = -first.angle - math.pi / 2 - env.incline_angle
    dot_x = cx + r * math.cos(dot_angle)
    dot_y = cy + r * math.sin(dot_angle)
    dx0, dy0, dx1, dy1 = _circle_bbox(dot_x, dot_y, dot_r)
    dot_shape_initial = {
        "type": "circle",
        "xref": "x",
        "yref": "y",
        "x0": dx0,
        "y0": dy0,
        "x1": dx1,
        "y1": dy1,
        "line": {"color": "black"},
        "fillcolor": "crimson",
    }

    frames = []
    for i, b in enumerate(balls):
        cx = b.get_position_x(env)
        cy = b.get_position_y(env)
        r = b.radius
        x0, y0, x1, y1 = _circle_bbox(cx, cy, r)
        ball_shape = {
            "type": "circle",
            "xref": "x",
            "yref": "y",
            "x0": x0,
            "y0": y0,
            "x1": x1,
            "y1": y1,
            "line": {"color": "white"},
            "fillcolor": "rgba(255,255,255,0.08)",
        }

        # rim-dot (rotating)
        dot_r = r * dot_fraction
        dot_angle = -b.angle - math.pi / 2 - env.incline_angle
        dot_x = cx + r * math.cos(dot_angle)
        dot_y = cy + r * math.sin(dot_angle)
        dx0, dy0, dx1, dy1 = _circle_bbox(dot_x, dot_y, dot_r)
        dot_shape = {
            "type": "circle",
            "xref": "x",
            "yref": "y",
            "x0": dx0,
            "y0": dy0,
            "x1": dx1,
            "y1": dy1,
            "line": {"color": "black"},
            "fillcolor": "crimson",
        }

        # Each frame only includes changing shapes (ball + dot). Keep plane static in layout.
        frames.append(
            Frame(data=[], name=str(i), layout={"shapes": [plane_shape, ball_shape, dot_shape]})
        )

    return Figure(
        data=[],  # no top-level traces
        frames=frames,
        layout={
            "shapes": [plane_shape, ball_shape_initial, dot_shape_initial],
            "xaxis": {"range": x_range},
            "yaxis": {"range": y_range, "scaleanchor": "x", "scaleratio": 1},
            "height": 600,
            "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
            "updatemenus": [
                {
                    "type": "buttons",
                    "showactive": False,
                    "y": 1.05,
                    "x": 0.05,
                    "xanchor": "left",
                    "buttons": [
                        {
                            "label": "Play",
                            "method": "animate",
                            "args": [
                                None,
                                {
                                    "frame": {"duration": frame_duration, "redraw": False},
                                    "fromcurrent": True,
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                        {
                            "label": "Pause",
                            "method": "animate",
                            "args": [
                                [None],
                                {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"},
                            ],
                        },
                    ],
                }
            ],
        },
    )
