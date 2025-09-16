import math

import streamlit as st

from labs.model.constant import G
from labs.model.enum import CorrelationType, relation_degrees
from labs.model.vector import Vector2D
from labs.throw_a_rock.acceleration import acceleration_law_by_resistance_type
from labs.throw_a_rock.motion.simulation import simulate_flight
from labs.throw_a_rock.velocity.calculator import VelocityCalculator

st.set_page_config(layout="wide")

with st.sidebar:
    resistance_type: CorrelationType = st.segmented_control(
        "Air resistance type", relation_degrees, default=CorrelationType.LINEAR
    )
    if resistance_type is None:
        st.warning("Choose the resistance type! Linear one is used now.")
        resistance_type = CorrelationType.LINEAR

    st.slider(
        "Air resistance rate",
        min_value=0.0,
        max_value=5.0,
        value=0.5,
        step=0.01,
        key="air_resistance_rate",
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
    sampling_delta: float = 1.0 / 2 ** st.slider(
        "Log2 of sampling steps per second",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        help="The formula of the real steps per second used is 2^(chosen number). By default: 5 -> 32 sps",
    )

    with st.expander("Constants used"):
        st.text(f"g = {G} m/s")


st.title("Throw a Rock 🪨")

velocity_calculator = VelocityCalculator(
    initial_velocity=Vector2D.from_polar(initial_velocity_norm, angle),
    acceleration_law=acceleration_law_by_resistance_type[resistance_type],
    sampling_delta=sampling_delta,
)

chart = st.line_chart(
    Vector2D(0.0, 0.0).to_df(), x="x", y="y", x_label="x, meters", y_label="y, meters"
)

point = Vector2D(0.0, 0.0)
for point in simulate_flight(velocity_calculator):
    chart.add_rows(point.to_df())

st.text(f"Approximate grounding point is {point.x:.2f} meters.")
