import math

import streamlit as st

from labs.model.constant import G
from labs.model.enum import CorrelationType
from labs.model.vector import Vector2D, trajectory_to_df, trajectory_to_time_velocity_df
from labs.throw_a_rock.acceleration import acceleration_law_by_resistance_type
from labs.throw_a_rock.motion.compute import compute_flight_time
from labs.throw_a_rock.motion.simulation import simulate_flight
from labs.throw_a_rock.velocity.calculator import VelocityCalculator
from labs.throw_a_rock.visualization.charts import (
    create_trajectory_chart_with_tooltips,
    create_velocity_chart,
)

st.set_page_config(layout="wide")

with st.sidebar:
    resistance_type: CorrelationType = st.segmented_control(
        "Air resistance type",
        options=list(CorrelationType),
        default=CorrelationType.LINEAR,
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
    st.slider(
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


velocity_calculator = VelocityCalculator(
    initial_velocity=Vector2D.from_polar(initial_velocity_norm, angle),
    acceleration_law=acceleration_law_by_resistance_type[resistance_type],
    sampling_delta=sampling_delta,
)
trajectory_data = list(simulate_flight(velocity_calculator))
grounding_point = trajectory_data[-1][0]
flight_time = compute_flight_time(trajectory_data, sampling_delta)


st.title("Throw a Rock 🪨")

st.altair_chart(
    create_trajectory_chart_with_tooltips(trajectory_to_df(trajectory_data)),
    use_container_width=True,
)

st.altair_chart(
    create_velocity_chart(
        trajectory_to_time_velocity_df(trajectory_data, sampling_delta)
    ),
    use_container_width=True,
)

st.markdown(
    f"""
    | Measure | Approximate value |
    | --- | --- |
    | Grounding point | {grounding_point.x:.2f} meters |
    | Flight time | {flight_time:.2f} seconds |
    """
)
