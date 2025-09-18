import altair as alt
import pandas as pd

from .util import hover_selection, interactive_points, tooltip_rule


def create_trajectory_chart(trajectory_df: pd.DataFrame) -> alt.LayerChart:
    """Create an interactive trajectory chart with velocity tooltips."""
    hover = hover_selection("x")

    lines = (
        alt.Chart(trajectory_df, title="Rock Trajectory")
        .mark_line()
        .encode(
            x=alt.X("x:Q", title="X Position (meters)"),
            y=alt.Y("y:Q", title="Y Position (meters)"),
        )
    )

    points = interactive_points(lines, hover)
    tooltips = tooltip_rule(trajectory_df, hover, x_field="x", y_field="y")

    return lines + points + tooltips
