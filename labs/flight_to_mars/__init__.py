# ruff: noqa: N806

from collections.abc import Sequence
from functools import partial
from math import pi

import streamlit as st

from labs.flight_to_mars.model.flight import FlightEquationType
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.model.stage import FlightStage
from labs.flight_to_mars.stage.criteria import is_astronaut_dead
from labs.flight_to_mars.stage.planet import flight_equations
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.criteria import did_rocket_left_the_planet
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.flight_to_mars.stage.space.calculator import RocketInterplanetaryFlightCalculator
from labs.flight_to_mars.stage.space.criteria import did_reach_the_target
from labs.flight_to_mars.stage.space.equation import (
    interplanetary_engine_off_equation,
)
from labs.flight_to_mars.stage.space.simulation import simulate_interplanetary_flight
from labs.flight_to_mars.visualization.chart import (
    plot_acceleration,
    plot_distance_to_target_chart,
    plot_mass,
    plot_velocity,
    plot_y_position,
)
from labs.flight_to_mars.visualization.entity import (
    earth_shape,
    mars_shape,
    orbit_shape,
    rocket_shape,
    sun_shape,
)
from labs.flight_to_mars.visualization.render import render_animation
from labs.model.constant import (
    EARTH_MARS_DISTANCE,
    EARTH_MASS,
    EARTH_RADIUS,
    MARS_MASS,
    MARS_RADIUS,
    MAX_HUMANLY_VIABLE_OVERLOAD,
    SUN_EARTH_DISTANCE,
    SUN_MARS_DISTANCE,
    SUN_RADIUS,
    G,
    g,
)

__all__ = ["page"]


def page() -> None:
    SAMLING_DELTA = 1
    st.session_state.sampling_delta = SAMLING_DELTA
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")

    with st.sidebar:
        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage", default=FlightStage.EARTH, options=list(FlightStage)
        )
        flight_equation_type = FlightEquationType.FIXED_ACCELERATION

        if flight_stage == FlightStage.SPACE:
            show_real_size: bool = st.checkbox("Show real planets size")

            initial_velocity: float = 1000 * st.slider(
                "Initial velocity (km/s)", min_value=10.0, max_value=23.5, value=21.91, step=0.01
            )
        else:
            initial_mass: float = 1000 * st.slider(
                "Initial mass, ton",
                min_value=10.0,
                max_value=500.0,
                value=80.0,
                step=0.1,
            )

            fuel_ratio: float = st.slider(
                "Fuel ratio, %",
                min_value=80.0,
                max_value=99.9,
                value=96.0,
                step=0.05,
            )
            fuel_mass: float = initial_mass * fuel_ratio / 100
            netto_mass: float = initial_mass - fuel_mass

            acceleration: float = g * st.slider(
                "Acceleration, g",
                min_value=1.0,
                max_value=10.0,
                value=2.0,
                step=0.05,
                help=(
                    "The rocket engine operates in a mode that maintains constant rocket "
                    "acceleration to protect the astronaut from excessive force."
                ),
            )

            rocket_stream_velocity: float = 1000 * st.slider(
                "Rocket stream velocity, km/s",
                min_value=1.0,
                max_value=7.0,
                value=4.5,
                step=0.02,
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

    #####################################################################################

    match flight_stage:
        case FlightStage.EARTH:
            planet = earth_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, angle=0, size=EARTH_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
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

            # Швабры держат потолок
            if not rockets:
                st.rerun()

            figure = render_animation(rockets, rocket_shape_at, [planet])
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            telemetry_charts(rockets, EARTH_MASS, EARTH_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning(
                    f"The astronaut is dead. Try not to exceed {MAX_HUMANLY_VIABLE_OVERLOAD}G overload."
                )
            else:
                status = results.empty()

            with status.container(border=True):
                if rockets and did_rocket_left_the_planet(rockets[-1], EARTH_MASS):
                    st.markdown("You have successfully escaped Earth's gravitation!")
                else:
                    st.markdown("You have not reached the speed to overcome gravitation.")

        #################################################################################

        case FlightStage.SPACE:
            SAMLING_DELTA = 60 * 60 * 1  # one hour
            st.session_state.sampling_delta = SAMLING_DELTA

            sun_radius = SUN_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 20
            earth_radius = EARTH_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 50
            mars_radius = MARS_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 65

            sun = sun_shape(x=-SUN_EARTH_DISTANCE, y=0, radius=sun_radius)
            earth = earth_shape(x=0, y=0, radius=earth_radius)
            mars = mars_shape(x=EARTH_MARS_DISTANCE, y=0, radius=mars_radius)
            rocket_shape_at = partial(rocket_shape, angle=-pi / 2, size=earth_radius / 3)

            earth_orbit = orbit_shape(
                center_x=-SUN_EARTH_DISTANCE,
                center_y=0,
                semi_major=SUN_EARTH_DISTANCE,
                semi_minor=SUN_EARTH_DISTANCE,
            )
            mars_orbit = orbit_shape(
                center_x=-SUN_EARTH_DISTANCE,
                center_y=0,
                semi_major=SUN_MARS_DISTANCE,
                semi_minor=SUN_MARS_DISTANCE,
            )

            APROXIMATE_TAKE_OFF_HEIGHT = 2_336_000
            APROXIMATE_LANDING_HEIGHT  =   555_000  # fmt: skip
            TARGET_X = EARTH_MARS_DISTANCE - MARS_RADIUS - APROXIMATE_LANDING_HEIGHT
            initial_rocket = Rocket(
                x=EARTH_RADIUS + APROXIMATE_TAKE_OFF_HEIGHT,
                y=0,
                velocity=initial_velocity,
                netto_mass=0,
                fuel_mass=0,
                stream_velocity=0,
                acceleration=0,
            )

            rockets = list(
                simulate_interplanetary_flight(
                    RocketInterplanetaryFlightCalculator(
                        initial_rocket, interplanetary_engine_off_equation
                    ),
                    sampling_delta=SAMLING_DELTA,
                    target_x=TARGET_X,
                )
            )

            # Швабры держат потолок
            if not rockets:
                st.rerun()

            figure = render_animation(
                rockets, rocket_shape_at, [earth, mars, sun], [earth_orbit, mars_orbit]
            )
            st.plotly_chart(figure, key="animation")

            status = st.empty()
            with status.container(border=True):
                if did_reach_the_target(TARGET_X, rockets[-1]):
                    st.markdown("Succesfully reached the Mars!")
                else:
                    st.markdown("You failed to maintain enough speed to reach the Mars.")

            st.subheader("Rocket Metrics Over Time")
            col1, col2 = st.columns(2)
            col1.write("**Distance to Target (km)**")
            plot_distance_to_target_chart(col1, rockets, TARGET_X, in_days=True)
            col1.write("**Velocity (km/s)**")
            plot_velocity(col1, rockets[:-1], in_days=True)
            col2.write("**Acceleration (g)**")
            plot_acceleration(col2, rockets[:-1], in_days=True)

        #################################################################################

        case FlightStage.MARS:
            planet = mars_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, angle=0, size=MARS_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
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
            raw_rockets: list[Rocket] = list(simulate_flight(calculator, SAMLING_DELTA))
            rockets: list[Rocket] = list(filter(lambda r: r.mass <= initial_mass, raw_rockets))

            # Швабры держат потолок
            if not rockets:
                st.rerun()

            figure = render_animation(rockets[::-1], rocket_shape_at, [planet])
            st.plotly_chart(figure, key="animation")

            results = st.empty()
            if did_rocket_left_the_planet(rockets[-1], MARS_MASS):
                telemetry_charts(rockets[::-1], MARS_MASS, MARS_RADIUS)

            if is_astronaut_dead(rockets):
                status, warning = results.columns(2)
                warning.warning(
                    f"The astronaut is dead. Try not to exceed {MAX_HUMANLY_VIABLE_OVERLOAD}G overload."
                )
            else:
                status = results.empty()

            with status.container(border=True):
                if rockets and did_rocket_left_the_planet(rockets[-1], MARS_MASS):
                    st.markdown(
                        f"You have to turn on engine at {(rockets[-1].y - MARS_RADIUS) / 1000:.01f}km above "
                        f"to successfully land on Mars. You should have only {rockets[-1].fuel_mass / fuel_mass * 100:.02f}% "
                        f"({rockets[-1].fuel_mass:.02f} ton) of a fuel tank to be full."
                    )
                else:
                    st.markdown(
                        f"You probably have been smashed into pieces. You must have {(raw_rockets[-1].fuel_mass / fuel_mass - 1) * 100:.02f}% "
                        f"more fuel ({rockets[-1].fuel_mass:.02f} ton totaly) while maintaining the same payload mass."
                    )

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
