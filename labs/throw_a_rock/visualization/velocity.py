import altair as alt
import pandas as pd

from .util import hover_selection, interactive_points, tooltip_rule


def create_velocity_chart(velocity_df: pd.DataFrame) -> alt.LayerChart:
    """Create a velocity magnitude chart."""
    hover = hover_selection("time")

    lines = (
        alt.Chart(velocity_df, title="Velocity by Time")
        .mark_line()
        .encode(
            x=alt.X("time:Q", title="Time (s)"),
            y=alt.Y("velocity_norm:Q", title="Velocity (m/s)"),
        )
    )

    points = interactive_points(lines, hover)
    tooltips = tooltip_rule(velocity_df, hover, x_field="time", y_field="velocity_norm")

    return lines + points + tooltips
