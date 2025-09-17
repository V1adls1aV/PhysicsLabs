import altair as alt
import pandas as pd


def _hover_selection(field: str) -> alt.Parameter:
    return alt.selection_single(
        fields=[field], nearest=True, on="mouseover", empty="none"
    )


def _interactive_points(
    layer: alt.Chart, hover: alt.Parameter, size: int = 65
) -> alt.Chart:
    return layer.transform_filter(hover).mark_circle(size=size)


def _tooltip_rule(
    data: pd.DataFrame,
    hover: alt.Parameter,
    x_field: str,
    y_field: str | None,
    tooltip_defs: list[alt.Tooltip],
) -> alt.Chart:
    encode_kwargs = {
        "x": f"{x_field}:Q",
        "opacity": alt.condition(hover, alt.value(0.3), alt.value(0)),
        "tooltip": tooltip_defs,
    }
    if y_field is not None:
        encode_kwargs["y"] = f"{y_field}:Q"
    return alt.Chart(data).mark_rule().encode(**encode_kwargs).add_selection(hover)


def create_trajectory_chart_with_tooltips(
    trajectory_df: pd.DataFrame,
) -> alt.LayerChart:
    """Create an interactive trajectory chart with velocity tooltips."""
    hover = _hover_selection("x")

    lines = (
        alt.Chart(trajectory_df, title="Rock Trajectory")
        .mark_line()
        .encode(
            x=alt.X("x:Q", title="X Position (meters)"),
            y=alt.Y("y:Q", title="Y Position (meters)"),
        )
        .properties(width=400, height=400)
    )

    points = _interactive_points(lines, hover)

    tooltips = _tooltip_rule(
        trajectory_df,
        hover,
        x_field="x",
        y_field="y",
        tooltip_defs=[
            alt.Tooltip("x:Q", title="X Position", format=".2f"),
            alt.Tooltip("y:Q", title="Y Position", format=".2f"),
            alt.Tooltip("velocity_norm:Q", title="Velocity", format=".2f"),
            alt.Tooltip("velocity_angle:Q", title="Angle", format=".1f"),
        ],
    )

    return lines + points + tooltips


def create_velocity_chart(velocity_df: pd.DataFrame) -> alt.LayerChart:
    """Create a velocity magnitude chart."""
    hover = _hover_selection("time")

    lines = (
        alt.Chart(velocity_df, title="Velocity by Time")
        .mark_line()
        .encode(
            x=alt.X("time:Q", title="Time (s)"),
            y=alt.Y("velocity:Q", title="Velocity (m/s)"),
        )
    )

    points = _interactive_points(lines, hover)

    tooltips = _tooltip_rule(
        velocity_df,
        hover,
        x_field="time",
        y_field=None,
        tooltip_defs=[
            alt.Tooltip("x:Q", title="X Position", format=".2f"),
            alt.Tooltip("y:Q", title="Y Position", format=".2f"),
            alt.Tooltip("velocity:Q", title="Velocity", format=".2f"),
            alt.Tooltip("velocity_angle:Q", title="Angle", format=".1f"),
        ],
    )

    return lines + points + tooltips
