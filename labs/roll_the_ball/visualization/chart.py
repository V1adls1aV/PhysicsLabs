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
    color: str,
    *,
    trim_last: bool = False,
) -> None:
    timeline = _time_axis(len(balls))
    values = tuple(property_callable(ball) for ball in balls)

    if trim_last:
        timeline = timeline[:-1]
        values = values[:-1]

    container.line_chart(
        {
            "Time (s)": timeline,
            label: values,
        },
        x="Time (s)",
        y=label,
        color=color,
    )


@lru_cache(maxsize=1)
def _time_axis(size: int) -> tuple[float, ...]:
    return tuple(i * SAMPLING_DELTA for i in range(size))
