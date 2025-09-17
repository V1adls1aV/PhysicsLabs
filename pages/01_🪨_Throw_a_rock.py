import math

import pandas as pd
import streamlit as st

from labs.model.constant import G
from labs.model.enum import CorrelationType, relation_degrees
from labs.model.vector import Vector2D, trajectory_to_df
from labs.throw_a_rock.acceleration import acceleration_law_by_resistance_type
from labs.throw_a_rock.motion.simulation import simulate_flight
from labs.throw_a_rock.velocity.calculator import VelocityCalculator
from labs.throw_a_rock.visialization.charts import (
    create_trajectory_chart_with_tooltips,
    create_velocity_chart,
)

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
    sampling_delta: float = 1.0 / st.select_slider(
        "Sampling steps per second", options=(2**x for x in range(11)), value=32
    )

    with st.expander("Constants used"):
        st.text(f"g = {G} m/s")


st.title("Throw a Rock 🪨")

velocity_calculator = VelocityCalculator(
    initial_velocity=Vector2D.from_polar(initial_velocity_norm, angle),
    acceleration_law=acceleration_law_by_resistance_type[resistance_type],
    sampling_delta=sampling_delta,
)

# Collect trajectory data
trajectory_data = list(simulate_flight(velocity_calculator))
point = trajectory_data[-1][0]  # Get final point for grounding distance

# Create trajectory chart with tooltips
trajectory_df = trajectory_to_df(trajectory_data)
trajectory_chart = create_trajectory_chart_with_tooltips(trajectory_df)
st.altair_chart(trajectory_chart, use_container_width=True)

# Display grounding point
result_field = st.empty()
result_field.text(f"Approximate grounding point is {point.x:.2f} meters.")

# Create velocity chart
velocity_data = [(point.x, velocity.norm) for point, velocity in trajectory_data]
velocity_df = pd.DataFrame(velocity_data, columns=["x", "velocity"])
velocity_chart = create_velocity_chart(velocity_df)
st.altair_chart(velocity_chart, use_container_width=True)
