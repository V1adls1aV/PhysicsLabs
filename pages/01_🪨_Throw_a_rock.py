import math

import streamlit as st

from labs.model.constant import G
from labs.model.enum import CorrelationType, relation_degrees
from labs.model.vector import Vector2D
from labs.throw_a_rock.acceleration import acceleration_law_by_resistance_type
from labs.throw_a_rock.trajectory import (
    compute_grounding_point,
    compute_next_point,
)
from labs.throw_a_rock.velocity.calculator import VelocityCalculator

st.set_page_config(layout="wide")

with st.sidebar:
    resistance_type: CorrelationType = st.segmented_control(
        "Air resistance type", relation_degrees, default=CorrelationType.LINEAR
    )

    match resistance_type:
        case CorrelationType.CONSTANT:
            st.slider(
                "Constant air resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=0.01,
                key="constant_air_resistance_rate",
            )
        case CorrelationType.LINEAR:
            st.slider(
                "Linear air resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
                key="linear_air_resistance_rate",
            )
        case CorrelationType.QUADRATIC:
            st.slider(
                "Quadratic air resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
                key="quadratic_air_resistance_rate",
            )

    initial_velocity_norm: float = st.slider(
        "Velocity, m/s", min_value=0.0, max_value=334.0, value=40.0, step=0.1
    )
    angle: float = math.radians(
        st.slider("Angle, deg", min_value=0.0, max_value=90.0, value=30.0, step=0.25)
    )
    mass: float = st.slider(
        "Mass, kg",
        min_value=0.001,
        max_value=10.0,
        value=1.0,
        step=0.001,
        key="rock_mass",
    )

    sampling_delta: float = 1.0 / st.slider(
        "Sampling steps per second, step/sec",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
    )

    with st.expander("Constants used"):
        st.text(f"g = {G} m/s")


st.title("Throw a Rock 🪨")

velocity = Vector2D.from_polar(initial_velocity_norm, angle)
velocity_calculator = VelocityCalculator(
    initial_velocity=velocity,
    acceleration_law=acceleration_law_by_resistance_type[resistance_type],
    sampling_delta=sampling_delta,
)

previous_point = Vector2D(0.0, 0.0)
new_point = compute_next_point(previous_point, velocity, sampling_delta)

chart = st.line_chart(
    previous_point.to_df(),
    x="x",
    y="y",
    x_label="x, meters",
    y_label="y, meters",
)

while new_point.y >= 0.0:
    chart.add_rows(new_point.to_df())
    previous_point = new_point

    velocity = velocity_calculator()
    new_point = compute_next_point(previous_point, velocity, sampling_delta)

grounding_point = compute_grounding_point(previous_point, velocity)
chart.add_rows(grounding_point.to_df())

st.text(f"Approximate grounding point is {grounding_point.x:.2f} meters.")
