import altair as alt
import pandas as pd


def create_trajectory_chart_with_tooltips(trajectory_df: pd.DataFrame) -> alt.Chart:
    """Create an interactive trajectory chart with velocity tooltips."""
    hover = alt.selection_single(
        fields=["x"], nearest=True, on="mouseover", empty="none"
    )

    # Calculate data range for equal scales
    x_min, x_max = trajectory_df["x"].min(), trajectory_df["x"].max()
    y_min, y_max = trajectory_df["y"].min(), trajectory_df["y"].max()

    # Use the larger range for both axes to maintain 1:1 ratio
    data_range = max(x_max - x_min, y_max - y_min)
    x_center, y_center = (x_min + x_max) / 2, (y_min + y_max) / 2

    x_domain = [x_center - data_range / 2, x_center + data_range / 2]
    y_domain = [y_center - data_range / 2, y_center + data_range / 2]

    # Main trajectory line with 1:1 aspect ratio
    lines = (
        alt.Chart(trajectory_df, title="Rock Trajectory")
        .mark_line()
        .encode(
            x=alt.X(
                "x:Q", title="X Position (meters)", scale=alt.Scale(domain=x_domain)
            ),
            y=alt.Y(
                "y:Q", title="Y Position (meters)", scale=alt.Scale(domain=y_domain)
            ),
        )
        .properties(width=400, height=400)
    )

    # Interactive points
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Tooltip rule
    tooltips = (
        alt.Chart(trajectory_df)
        .mark_rule()
        .encode(
            x="x:Q",
            y="y:Q",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("x:Q", title="X Position", format=".2f"),
                alt.Tooltip("y:Q", title="Y Position", format=".2f"),
                alt.Tooltip("velocity_norm:Q", title="Velocity", format=".2f"),
                alt.Tooltip("velocity_angle:Q", title="Angle", format=".1f"),
            ],
        )
        .add_selection(hover)
    )

    return lines + points + tooltips


def create_velocity_chart(velocity_df: pd.DataFrame) -> alt.Chart:
    """Create a velocity magnitude chart."""
    return (
        alt.Chart(velocity_df, title="Velocity vs Position")
        .mark_line()
        .encode(
            x=alt.X("x:Q", title="X Position (meters)"),
            y=alt.Y("velocity:Q", title="Velocity (m/s)"),
        )
    )
