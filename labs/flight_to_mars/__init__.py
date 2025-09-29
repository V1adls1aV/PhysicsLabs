from functools import partial

import streamlit as st

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.criteria import is_astronaut_dead
from labs.flight_to_mars.stage.earth.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.earth.criteria import does_rocket_left_the_earth
from labs.flight_to_mars.stage.earth.equation import rocket_flight_equation
from labs.flight_to_mars.stage.earth.simulation import simulate_flight
from labs.flight_to_mars.stage.stage import FlightStage
from labs.flight_to_mars.visualization.chart import (
    plot_acceleration,
    plot_mass,
    plot_velocity,
    plot_y_position,
)
from labs.flight_to_mars.visualization.entity import earth_shape, rocket_shape
from labs.flight_to_mars.visualization.render import render_animation
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, MARS_MASS, MARS_RADIUS, G

__all__ = ["page"]

SAMLING_DELTA = 0.5
st.session_state.sampling_delta = SAMLING_DELTA


def page() -> None:
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")
    st.title("Flight to Mars 🚀")

    with st.sidebar:
        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage", default=FlightStage.EARTH, options=list(FlightStage)
        )

        initial_mass: float = st.slider(
            "Initial mass, kg",
            min_value=10_000,
            max_value=500_000,
            value=80_000,
            step=1_000,
            key="initial_mass",
        )
        fuel_ratio: float = st.slider(
            "Fuel ratio, %",
            min_value=80.0,
            max_value=99.9,
            value=95.0,
            step=0.1,
            key="fuel_ratio",
        )
        fuel_mass: float = initial_mass * fuel_ratio / 100
        netto_mass: float = initial_mass - fuel_mass
        fuel_consumption: float = st.slider(
            "Fuel consumption, kg/s",
            min_value=1000,
            max_value=30_000,
            value=20_000,
            step=1000,
            key="fuel_consumption",
        )
        rocket_stream_velocity: float = st.slider(
            "Rocket stream velocity, m/s",
            min_value=1000,
            max_value=7000,
            value=4500,
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
            planet = earth_shape(x=0, y=0, radius=EARTH_RADIUS)
            rocket_shape_at = partial(rocket_shape, x=0, angle=0, size=EARTH_RADIUS / 100)
            animation = st.empty()
            initial_rocket = Rocket(
                y=EARTH_RADIUS,
                velocity=0,
                netto_mass=netto_mass,
                fuel_mass=fuel_mass,
                fuel_consumption=fuel_consumption,
                stream_velocity=rocket_stream_velocity,
            )
            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=rocket_flight_equation,
            )

            results = st.empty()
            st.subheader("Rocket Metrics Over Time")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Velocity (m/s)**")
                velocity_chart = st.empty()
                st.write("**Mass (kg)**")
                mass_chart = st.empty()
            with col2:
                st.write("**Y Position (m)**")
                y_chart = st.empty()
                st.write("**Acceleration (g)**")
                acceleration_chart = st.empty()

            rockets: list[Rocket] = list(simulate_flight(calculator, SAMLING_DELTA))

            figure = render_animation(rockets, rocket_shape_at, planet)
            animation.plotly_chart(figure, key="animation")
            plot_velocity(velocity_chart, rockets)
            plot_mass(mass_chart, rockets)
            plot_y_position(y_chart, rockets)
            plot_acceleration(acceleration_chart, rockets)

            status, warning = results.columns(2)
            with status.container(border=True):
                if rockets and does_rocket_left_the_earth(rockets[-1]):
                    st.markdown("You have successfully escaped Earth's gravitation!")
                else:
                    st.markdown("You have not reached the speed to overcome gravitation.")

            if is_astronaut_dead(rockets):
                warning.warning("The astronaut is dead. Try not to exceed 10G overload.")
        case FlightStage.SPACE:
            ...
        case FlightStage.MARS:
            ...
        case None:
            st.warning("Choose one of the stages to simulate.")
