# ruff: noqa

import math
from collections.abc import Sequence

from plotly.graph_objects import Figure, Frame

from ..model import PendulumState


def render_pendulum_animation(
    states: Sequence[PendulumState],
    extreme_states: Sequence[PendulumState],
    *,
    frame_duration: int = 3,
    pin_radius: float = 0.1,
    pendulum_witdth: float = 0.05,
) -> Figure:
    first_state = states[0]

    right_border = math.sin(first_state.angle)
    left_border = -right_border
    top_border = pin_radius
    bottom_border = -first_state.length

    pad = 0.05
    x_range = (left_border - pad, right_border + pad)
    y_range = (bottom_border - pad, top_border + pad)

    pin_shape = {
        "type": "circle",
        "x0": -pin_radius,
        "y0": -pin_radius,
        "x1": pin_radius,
        "y1": pin_radius,
        "fillcolor": "crimson",
    }

    return Figure()
