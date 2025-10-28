from collections.abc import Callable, Sequence
from functools import lru_cache

from streamlit.delta_generator import DeltaGenerator

from ..config import SAMPLING_DELTA
from ..model import Ball


def plot_ball_property(
    container: DeltaGenerator,
    balls: Sequence[Ball],
    property_callable: Callable[[Ball], float],
    label: str,
    color: str = "#1f77b4",
) -> None:
    timeline = _time_axis(len(balls))
    values = [property_callable(ball) for ball in balls]

    container.line_chart(
        {
            "Time (s)": timeline,
            label: values,
        },
        x="Time (s)",
        y=[label],
        color=[color],
    )


@lru_cache
def _time_axis(size: int) -> list[float]:
    return [i * SAMPLING_DELTA for i in range(size)]
