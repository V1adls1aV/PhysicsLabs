import math
from collections.abc import Sequence
from copy import deepcopy

from plotly.graph_objects import Figure, Frame

from ..model import PendulumState


def render_pendulum_animation(
    states: Sequence[PendulumState],
    extreme_states: Sequence[PendulumState],
    *,
    frame_duration: int = 3,
    pin_radius: float = 0.015,
    pendulum_width: float = 3,
) -> Figure:
    time_to_extreme_state = {state.time: state for state in extreme_states}
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
        "line": {"width": 0},
    }

    initial_pendulum_shape = {
        "type": "line",
        "x0": 0,
        "y0": 0,
        "x1": math.sin(first_state.angle) * first_state.length,
        "y1": -math.cos(first_state.angle) * first_state.length,
        "line": {"width": pendulum_width, "color": "white"},
    }

    pendulum_extreme_shapes = []
    frames = []
    for state in states:
        pendulum_shape = {
            "type": "line",
            "x0": 0,
            "y0": 0,
            "x1": math.sin(state.angle) * state.length,
            "y1": -math.cos(state.angle) * state.length,
            "line": {"width": pendulum_width, "color": "white"},
        }

        if state.time in time_to_extreme_state:
            extreme_pendulum_shape = deepcopy(pendulum_shape)
            extreme_pendulum_shape["line"]["color"] = "gray"
            pendulum_extreme_shapes.append(extreme_pendulum_shape)

        frames.append(
            Frame(layout={"shapes": [*pendulum_extreme_shapes, pendulum_shape, pin_shape]})
        )

    return Figure(
        frames=frames,
        layout={
            "shapes": [initial_pendulum_shape, pin_shape],
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
