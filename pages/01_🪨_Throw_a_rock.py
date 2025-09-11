import math

import streamlit as st

from labs.model.constant import G
from labs.model.enum import RelationDegree, relation_degrees
from labs.model.vector import Vector2D, vectors_to_df
from labs.throw_a_rock.trajectory import (
    compute_grounding_point,
    make_step,
)
from labs.throw_a_rock.velocity.calculator import VelocityCalculator

st.set_page_config(layout="wide")

with st.sidebar:
    sampling_delta: float = 1.0 / st.slider(
        "Sampling steps per second, step/sec",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
    )
    initial_velocity_norm: float = st.slider(
        "Velocity, m/s", min_value=0.0, max_value=334.0, value=10.0, step=0.01
    )
    angle: float = math.radians(
        st.slider("Angle, deg", min_value=0.0, max_value=90.0, value=45.0, step=1.0)
    )
    mass: float = st.slider(
        "Mass, kg",
        min_value=0.001,
        max_value=10.0,
        value=1.0,
        step=0.001,
        key="rock_mass",
    )

    resistance_type: RelationDegree = st.segmented_control(
        "Air resistance type", relation_degrees, default=RelationDegree.LINEAR
    )

    match resistance_type:
        case RelationDegree.NONE:
            st.session_state.linear_air_resistance_rate = 0
        case RelationDegree.LINEAR:
            st.slider(
                "Linear air resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
                key="linear_air_resistance_rate",
            )
        case RelationDegree.QUADRATIC:
            st.slider(
                "Quadratic air resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
                key="quadratic_air_resistance_rate",
            )

    with st.expander("Constants used"):
        st.text(f"g = {G} m/s")


st.title("Throw a Rock 🪨")

initial_velocity = Vector2D.from_polar(initial_velocity_norm, angle)
velocity_calculator = VelocityCalculator(
    initial_velocity=initial_velocity, sampling_delta=sampling_delta
)

velocity = Vector2D(0.0, 0.0)
previous_point = Vector2D(0.0, 0.0)
new_point = make_step(previous_point, initial_velocity, sampling_delta)

chart = st.line_chart(
    vectors_to_df([previous_point]),
    x="x",
    y="y",
    x_label="x, meters",
    y_label="y, meters",
)

while new_point.y >= 0.0:
    chart.add_rows(new_point.to_df())
    previous_point = new_point

    velocity = velocity_calculator()
    new_point = make_step(previous_point, velocity, sampling_delta)

grounding_point = compute_grounding_point(previous_point, velocity)
chart.add_rows(grounding_point.to_df())

st.text(f"Approximate grounding point is {grounding_point.x:.2f} meters.")
