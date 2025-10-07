# ruff: noqa: N806
import math
from collections.abc import Sequence
from functools import partial

import streamlit as st

from labs.flight_to_mars.model.flight import FlightEquationType
from labs.flight_to_mars.model.planet import Planet
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.model.stage import FlightStage
from labs.flight_to_mars.stage.criteria import is_astronaut_dead
from labs.flight_to_mars.stage.planet import flight_equations
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.criteria import did_rocket_left_the_planet
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.flight_to_mars.stage.space.calculator import RocketInterplanetaryFlightCalculator
from labs.flight_to_mars.stage.space.criteria import check_planet_reach
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
    DAY,
    EARTH_MARS_DISTANCE,
    EARTH_MASS,
    EARTH_ORBITAL_VELOCITY,
    EARTH_RADIUS,
    HUMAN_EXPIRATION_TIME,
    MARS_MASS,
    MARS_RADIUS,
    MAX_HUMANLY_VIABLE_OVERLOAD,
    SUN_EARTH_DISTANCE,
    SUN_MARS_DISTANCE,
    SUN_MASS,
    SUN_RADIUS,
    G,
    g,
)
from labs.model.vector import Vector2D

__all__ = ["page"]


def page() -> None:
    SAMPLING_DELTA = 1
    st.session_state.sampling_delta = SAMPLING_DELTA
    st.set_page_config(page_title="Flight to Mars 🚀", page_icon="🚀", layout="wide")

    with st.sidebar:
        flight_stage: FlightStage | None = st.segmented_control(
            "Flight stage", default=FlightStage.EARTH, options=list(FlightStage)
        )
        flight_equation_type = FlightEquationType.FIXED_ACCELERATION

        if flight_stage == FlightStage.SPACE:
            show_real_size: bool = st.checkbox("Show real planets size")

            relative_rocket_velocity_norm: float = 1000 * st.slider(
                "Relative initial velocity (km/s)",
                min_value=5.0,
                max_value=20.0,
                value=11.3,
                step=0.01,
            )

            rocket_angle = math.radians(
                st.slider(
                    "Start angle, deg", min_value=-90.0, max_value=90.0, value=-1.73, step=0.01
                )
            )

            earth_position: Vector2D = Vector2D.from_polar(
                SUN_EARTH_DISTANCE,
                math.radians(
                    st.slider(
                        "Earth position, deg",
                        min_value=-180.0,
                        max_value=180.0,
                        value=-50.0,
                        step=0.1,
                    )
                ),
            )

            def relavite_position(v: Vector2D) -> Vector2D:
                return v - earth_position + Vector2D(SUN_EARTH_DISTANCE, 0)

            relative_rocket_velocity = Vector2D.from_polar(
                relative_rocket_velocity_norm, angle=rocket_angle
            )
            earth_velocity = Vector2D.from_polar(
                EARTH_ORBITAL_VELOCITY, earth_position.angle + math.pi / 2
            )
            rocket_velocity = relative_rocket_velocity + earth_velocity

            with st.expander("Calculated parameters", expanded=True):
                st.markdown(f"Initial velocity: {rocket_velocity.norm / 1000:.02f} km/s")
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
            rocket_shape_at = partial(rocket_shape, size=EARTH_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
                y=EARTH_RADIUS,
                velocity_x=0,
                velocity_y=0,
                netto_mass=netto_mass,
                fuel_mass=fuel_mass,
                stream_velocity=rocket_stream_velocity,
                acceleration_x=0,
                acceleration_y=acceleration,
            )
            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=EARTH_MASS,
            )
            rockets: list[Rocket] = list(simulate_flight(calculator, SAMPLING_DELTA))

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
            SAMPLING_DELTA = 60 * 60 * 4  # 4 hours
            st.session_state.sampling_delta = SAMPLING_DELTA

            sun_radius = SUN_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 20
            earth_radius = EARTH_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 50
            mars_radius = MARS_RADIUS if show_real_size else SUN_EARTH_DISTANCE / 65

            earth = Planet(x=0, y=0, mass=EARTH_MASS, radius=EARTH_RADIUS)
            mars_position = relavite_position(Vector2D(EARTH_MARS_DISTANCE, 0))
            mars = Planet(x=mars_position.x, y=mars_position.y, mass=MARS_MASS, radius=MARS_RADIUS)
            sun_position = relavite_position(Vector2D(-SUN_EARTH_DISTANCE, 0))
            sun = Planet(x=sun_position.x, y=sun_position.y, mass=SUN_MASS, radius=SUN_RADIUS)

            sun_shape_at = sun_shape(x=sun.x, y=sun.y, radius=sun_radius)
            earth_shape_at = earth_shape(x=earth.x, y=earth.y, radius=earth_radius)
            mars_shape_at = mars_shape(x=mars.x, y=mars.y, radius=mars_radius)

            earth_orbit = orbit_shape(
                center=sun_position,
                semi_major=SUN_EARTH_DISTANCE,
                semi_minor=SUN_EARTH_DISTANCE,
            )
            mars_orbit = orbit_shape(
                center=sun_position,
                semi_major=SUN_MARS_DISTANCE,
                semi_minor=SUN_MARS_DISTANCE,
            )

            APROXIMATE_TAKE_OFF_HEIGHT = 2_336_000

            rocket_start_point = Vector2D.from_polar(
                EARTH_RADIUS + APROXIMATE_TAKE_OFF_HEIGHT, angle=rocket_angle
            )
            rocket_shape_at = partial(rocket_shape, size=earth_radius / 3)

            initial_rocket = Rocket(
                x=rocket_start_point.x,
                y=rocket_start_point.y,
                velocity_x=rocket_velocity.x,
                velocity_y=rocket_velocity.y,
                netto_mass=0,
                fuel_mass=0,
                stream_velocity=0,
                acceleration_x=0,
                acceleration_y=0,
            )

            rockets = list(
                simulate_interplanetary_flight(
                    RocketInterplanetaryFlightCalculator(
                        initial_rocket, interplanetary_engine_off_equation, [earth, mars, sun]
                    ),
                    sampling_delta=SAMPLING_DELTA,
                    target_planet=mars,
                )
            )

            # Швабры держат потолок
            if not rockets:
                st.rerun()

            figure = render_animation(
                rockets,
                rocket_shape_at,
                [earth_shape_at, mars_shape_at, sun_shape_at],
                [earth_orbit, mars_orbit],
            )
            st.plotly_chart(figure, key="animation")

            status = st.empty()
            with status.container(border=True):
                if check_planet_reach(rockets[-2], rockets[-1], mars):
                    st.markdown("Succesfully reached the Mars!")
                elif len(rockets) * SAMPLING_DELTA > HUMAN_EXPIRATION_TIME:
                    st.markdown(
                        f"The astronaut is dead from hunger. Try not to exceed {HUMAN_EXPIRATION_TIME / DAY} days."
                    )
                else:
                    st.markdown("You failed to maintain enough speed to reach the Mars.")

            st.subheader("Rocket Metrics Over Time")
            col1, col2 = st.columns(2)

            col1.write("**Velocity (km/s)**")
            plot_velocity(col1, rockets[:-1], in_days=True)

            col1.write("**Distance to Target (km)**")
            plot_distance_to_target_chart(col1, rockets, mars, in_days=True)

            col2.write("**Pure Acceleration (g)**")
            plot_acceleration(col2, rockets, in_days=True)

        #################################################################################

        case FlightStage.MARS:
            planet = mars_shape(x=0, y=0)
            rocket_shape_at = partial(rocket_shape, size=MARS_RADIUS / 100)
            initial_rocket = Rocket(
                x=0,
                y=MARS_RADIUS,
                velocity_x=0,
                velocity_y=0,
                netto_mass=netto_mass,
                fuel_mass=1,  # Magic!
                stream_velocity=rocket_stream_velocity * -1,  # A little bit more magic.
                acceleration_x=0,
                acceleration_y=acceleration,
            )

            calculator = RocketFlightCalculator(
                rocket=initial_rocket,
                flight_equation=flight_equations[flight_equation_type],
                planet_mass=MARS_MASS,
            )
            raw_rockets: list[Rocket] = list(simulate_flight(calculator, SAMPLING_DELTA))
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
