__all__ = ["page"]

import math

import streamlit as st

from ..model.constant import G
from ..model.enum import CorrelationType
from ..model.vector import Vector2D, trajectory_to_df
from .acceleration import acceleration_law_by_resistance_type
from .motion.compute import compute_flight_time
from .motion.simulation import simulate_flight
from .velocity import VelocityCalculator
from .visualization import create_trajectory_chart, create_velocity_chart


def page() -> None:
    st.set_page_config(page_title="Throw a rock", page_icon="🪨", layout="wide")

    with st.sidebar:
        resistance_type: CorrelationType | None = st.segmented_control(
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
            max_value=2.0,
            value=0.5,
            step=0.01,
            key="air_resistance_rate",
        )
        initial_velocity_norm: float = st.slider(
            "Velocity, m/s", min_value=0.0, max_value=343.0, value=30.0, step=0.1
        )
        angle: float = math.radians(
            st.slider("Angle, deg", min_value=0.0, max_value=90.0, value=30.0, step=0.1)
        )
        st.slider(
            "Mass, kg",
            min_value=0.01,
            max_value=10.0,
            value=1.0,
            step=0.01,
            key="rock_mass",
        )
        sampling_delta: float = 1.0 / st.select_slider(
            "Sampling steps per second",
            options=(2**x for x in range(11)),
            value=2**6,
            key="sampling_steps",
        )

        with st.expander("Constants used"):
            st.html(f"g = {G} m/s<sup>2</sup>")

    velocity_calculator = VelocityCalculator(
        initial_velocity=Vector2D.from_polar(initial_velocity_norm, angle),
        acceleration_law=acceleration_law_by_resistance_type[resistance_type],
        sampling_delta=sampling_delta,
    )
    trajectory_data = list(simulate_flight(velocity_calculator))
    trajectory_df = trajectory_to_df(trajectory_data)

    grounding_point = trajectory_data[-1][0]
    flight_time = compute_flight_time(trajectory_data, sampling_delta)

    st.title("Throw a rock 🪨")

    st.altair_chart(create_trajectory_chart(trajectory_df))
    st.altair_chart(create_velocity_chart(trajectory_df))

    st.markdown(
        f"""
        | Measure | Approximate value |
        | --- | --- |
        | Flight time | {flight_time:.2f} s |
        | Flight distance | {grounding_point.x:.2f} m |
        """
    )
