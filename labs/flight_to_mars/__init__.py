from labs.flight_to_mars.stage.stage import FlightStage
from labs.flight_to_mars.visualization.render import render_frame

__all__ = ["page"]

import time

import streamlit as st

from labs.flight_to_mars.visualization.entity import earth_shape, rocket_shape
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, MARS_MASS, MARS_RADIUS, G

POINT_COUNT_THRESHOLD = 2**6


def page() -> None:
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")
    st.title("Flight to Mars 🚀")

    with st.sidebar:
        launched = st.button("Launch the rocket 🚀", type="primary")

        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage", default=FlightStage.EARTH, options=list(FlightStage)
        )

        initial_mass: float = st.slider(
            "Initial mass, kg",
            min_value=100,
            max_value=100_000,
            value=10_000,
            step=100,
            key="initial_mass",
        )
        fuel_ratio: float = st.slider(
            "Fuel ratio, %",
            min_value=10,
            max_value=99,
            value=70,
            step=1,
            key="fuel_ratio",
        )
        fuel_mass: float = initial_mass * fuel_ratio / 100
        fuel_consumption: float = st.slider(
            "Fuel consumption, kg/s",
            min_value=1,
            max_value=100,
            value=10,
            step=1,
            key="fuel_consumption",
        )
        rocket_stream_velocity: float = st.slider(
            "Rocket stream velocity, m/s",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            key="rocket_stream_velocity",
        )

        with st.expander("Calculated parameters", expanded=True):
            st.markdown(f"Fuel mass: {fuel_mass} kg")
            st.markdown(f"Estimated engine utilization time: {fuel_mass / fuel_consumption:.2f} s")

        with st.expander("Constants used"):
            st.html(f"G = {G} N·m<sup>2</sup>/kg<sup>2</sup>")
            st.html(f"Earth mass = {EARTH_MASS:.3e} kg")
            st.html(f"Earth radius = {EARTH_RADIUS} m")
            st.html(f"Mars mass = {MARS_MASS:.3e} kg")
            st.html(f"Mars radius = {MARS_RADIUS} m")

    match flight_stage:
        case FlightStage.EARTH:
            planet = earth_shape(x=0, y=0)
            rocket = rocket_shape(x=0, y=1, angle=0)
            y_positions = [1, 1.5, 2, 2.5, 3]  # , 5, 8, 15]

            animation = st.empty()
            print(rocket_stream_velocity)

            if launched:
                for y in y_positions:
                    figure = render_frame(y, rocket_shape(x=0, y=y, angle=0), planet)
                    animation.plotly_chart(figure)
                    time.sleep(0.25)
            else:
                figure = render_frame(y_positions[0], rocket, planet)
                animation.plotly_chart(figure)
        case FlightStage.SPACE:
            ...
        case FlightStage.MARS:
            ...
        case None:
            st.warning("Choose one of the stages to simulate.")
