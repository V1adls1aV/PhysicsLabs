from collections.abc import Sequence
from functools import partial

import streamlit as st

from labs.flight_to_mars.model.flight import FlightEquationType
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.model.stage import FlightStage
from labs.flight_to_mars.stage.criteria import is_astronaut_dead
from labs.flight_to_mars.stage.planet import flight_equations
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.criteria import did_rocket_left_the_planet
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.flight_to_mars.visualization.chart import (
    plot_acceleration,
    plot_mass,
    plot_velocity,
    plot_y_position,
)
from labs.flight_to_mars.visualization.entity import earth_shape, rocket_shape
from labs.flight_to_mars.visualization.entity.mars import mars_shape
from labs.flight_to_mars.visualization.render import render_animation
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, MARS_MASS, MARS_RADIUS, G, g

__all__ = ["page"]

SAMLING_DELTA = 0.5


def page() -> None:
    st.session_state.sampling_delta = SAMLING_DELTA
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")

    with st.sidebar:
        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage", default=FlightStage.EARTH, options=list(FlightStage)
        )
        flight_equation_type = FlightEquationType.FIXED_ACCELERATION

        initial_mass: float = 1000 * st.slider(
            "Initial mass, ton",
            min_value=10,
            max_value=500,
            value=80,
            step=1,
        )
        fuel_ratio: float = st.slider(
            "Fuel ratio, %",
            min_value=80.0,
            max_value=99.9,
            value=95.0,
            step=0.1,
        )
        fuel_mass: float = initial_mass * fuel_ratio / 100
        netto_mass: float = initial_mass - fuel_mass

        acceleration: float = g * st.slider(
            "Acceleration, g",
            min_value=1.0,
            max_value=15.0,
            value=7.0,
            step=0.1,
            help="The rocket engine operates in a mode that maintains constant rocket acceleration to protect the astronaut from excessive force.",
        )

        rocket_stream_velocity: float = 1000 * st.slider(
            "Rocket stream velocity, km/s",
            min_value=1.0,
            max_value=7.0,
            value=4.5,
            step=0.1,
        )

        with st.expander("Calculated parameters", expanded=True):
            st.markdown(f"Fuel mass: {fuel_mass / 1000} ton")

        with st.expander("Constants used"):
            st.html(f"G = {G} N·m<sup>2</sup>/kg<sup>2</sup>")
            st.html(f"Earth mass = {EARTH_MASS:.3e} kg")
            st.html(f"Earth radius = {EARTH_RADIUS} m")
            st.html(f"Mars mass = {MARS_MASS:.3e} kg")
            st.html(f"Mars radius = {MARS_RADIUS} m")

    st.title("Flight to Mars 🚀")
    match flight_stage:
        case FlightStage.EARTH:
            planet = earth_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, x=0, angle=0, size=EARTH_RADIUS / 100)
            initial_rocket = Rocket(
                y=EARTH_RADIUS,
                velocity=0,
                netto_mass=netto_mass,
                fuel_mass=fuel_mass,
                stream_velocity=rocket_stream_velocity,
                acceleration=acceleration,
            )
            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=EARTH_MASS,
            )
            rockets: list[Rocket] = list(simulate_flight(calculator, SAMLING_DELTA))

            figure = render_animation(rockets, rocket_shape_at, planet)
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            telemetry_charts(rockets, EARTH_MASS, EARTH_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning("The astronaut is dead. Try not to exceed 10G overload.")
            else:
                status = results.empty()

            with status.container(border=True):
                if rockets and did_rocket_left_the_planet(rockets[-1], EARTH_MASS):
                    st.markdown("You have successfully escaped Earth's gravitation!")
                else:
                    st.markdown("You have not reached the speed to overcome gravitation.")

        case FlightStage.SPACE:
            ...

        case FlightStage.MARS:
            planet = mars_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, x=0, angle=0, size=MARS_RADIUS / 100)
            initial_rocket = Rocket(
                y=MARS_RADIUS,
                velocity=0,
                netto_mass=netto_mass,
                fuel_mass=1,  # Magic!
                stream_velocity=rocket_stream_velocity * -1,  # A little bit more magic.
                acceleration=acceleration,
            )

            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=MARS_MASS,
            )
            rockets: list[Rocket] = list(
                filter(lambda r: r.mass <= initial_mass, simulate_flight(calculator, SAMLING_DELTA))
            )

            figure = render_animation(rockets[::-1], rocket_shape_at, planet)
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            telemetry_charts(rockets[::-1], MARS_MASS, MARS_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning("The astronaut is dead. Try not to exceed 10G overload.")
            else:
                status = results.empty()

            with status.container(border=True):
                if rockets and did_rocket_left_the_planet(rockets[-1], MARS_MASS):
                    st.markdown(
                        f"You have to turn on engine at {(rockets[-1].y - MARS_RADIUS) / 1000:.01f}km above to successfully land on Mars. You should have only {rockets[-1].fuel_mass / fuel_mass * 100:.02f}% ({rockets[-1].fuel_mass:.02f} ton) of a fuel tank to be full."
                    )
                else:
                    st.markdown("You probably have been smashed into pieces.")

        case None:
            st.warning("Choose one of the stages to simulate.")


def telemetry_charts(rockets: Sequence[Rocket], planet_mass: float, planet_radius: float) -> None:
    st.subheader("Rocket Metrics Over Time")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Velocity (km/s)**")
        velocity_chart = st.empty()
        st.write("**Mass (ton)**")
        mass_chart = st.empty()
    with col2:
        st.write("**Y Position (km)**")
        y_chart = st.empty()
        st.write("**Acceleration (g)**")
        acceleration_chart = st.empty()

    plot_velocity(velocity_chart, rockets, planet_mass)
    plot_mass(mass_chart, rockets)
    plot_y_position(y_chart, rockets, planet_radius)
    plot_acceleration(acceleration_chart, rockets)
