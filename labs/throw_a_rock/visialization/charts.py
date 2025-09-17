from __future__ import annotations

import altair as alt
import pandas as pd


def _equal_scale_domains(
    df: pd.DataFrame, x_col: str, y_col: str
) -> tuple[list[float], list[float]]:
    x_min, x_max = df[x_col].min(), df[x_col].max()
    y_min, y_max = df[y_col].min(), df[y_col].max()
    data_range = max(x_max - x_min, y_max - y_min)
    x_center, y_center = (x_min + x_max) / 2, (y_min + y_max) / 2
    return [x_center - data_range / 2, x_center + data_range / 2], [
        y_center - data_range / 2,
        y_center + data_range / 2,
    ]


def _hover_selection(field: str) -> alt.Selection:
    return alt.selection_single(
        fields=[field], nearest=True, on="mouseover", empty="none"
    )


def _interactive_points(
    layer: alt.Chart, hover: alt.Selection, size: int = 65
) -> alt.Chart:
    return layer.transform_filter(hover).mark_circle(size=size)


def _tooltip_rule(
    data: pd.DataFrame,
    hover: alt.Selection,
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


def create_trajectory_chart_with_tooltips(trajectory_df: pd.DataFrame) -> alt.Chart:
    """Create an interactive trajectory chart with velocity tooltips."""
    hover = _hover_selection("x")

    x_domain, y_domain = _equal_scale_domains(trajectory_df, "x", "y")

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


def create_velocity_chart(velocity_df: pd.DataFrame) -> alt.Chart:
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
