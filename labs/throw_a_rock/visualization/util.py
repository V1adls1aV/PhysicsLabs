import altair as alt
import pandas as pd


def hover_selection(field: str) -> alt.Parameter:
    return alt.selection_point(fields=[field], nearest=True, on="mouseover", empty=False)


def interactive_points(layer: alt.Chart, hover: alt.Parameter, size: int = 65) -> alt.Chart:
    return layer.transform_filter(hover).mark_circle(size=size)


def tooltip_rule(data: pd.DataFrame, hover: alt.Parameter, x_field: str, y_field: str) -> alt.Chart:
    encode_kwargs = {
        "x": f"{x_field}:Q",
        "y": f"{y_field}:Q",
        "opacity": alt.condition(hover, alt.value(0.3), alt.value(0)),
        "tooltip": [
            alt.Tooltip("x:Q", title="X position"),
            alt.Tooltip("y:Q", title="Y position"),
            alt.Tooltip("velocity_norm:Q", title="Velocity"),
            alt.Tooltip("velocity_angle:Q", title="Angle"),
        ],
    }
    return alt.Chart(data).mark_rule().encode(**encode_kwargs).add_params(hover)
