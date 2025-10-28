import math

import streamlit as st

from labs.model.constant import g
from labs.rolling_the_ball.model import Ball, Environment
from labs.rolling_the_ball.simulation import Calculator, simulate

from .config import SAMPLING_DELTA
from .visualization import plot_ball_property


def page() -> None:
    st.set_page_config(page_title="Rolling the ball ⚽", page_icon="⚽", layout="wide")

    st.title("Rolling the ball ⚽")

    with st.sidebar:
        ball = Ball(
            mass=st.slider(
                "Ball mass (kg)",
                min_value=0.01,
                max_value=10.0,
                value=0.42,
                step=0.01,
                format="%.2f",
            ),
            radius=(
                st.slider(
                    "Ball radius (cm)",
                    min_value=1.0,
                    max_value=100.0,
                    value=11.0,
                    step=0.1,
                    format="%.1f",
                )
                / 100
            ),
            translational_velocity=(
                st.slider(
                    "Initial translational velocity (m/s)",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.1,
                    format="%.1f",
                )
            ),
            angular_velocity=(
                st.slider(
                    "Initial angular velocity (rotations per second)",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                )
                * (2 * math.pi)
            ),
        )

        environment = Environment(
            incline_angle=math.radians(
                st.slider(
                    "Incline angle (deg)",
                    min_value=0.0,
                    max_value=89.9,
                    value=30.0,
                    step=0.1,
                    format="%.1f",
                )
            ),
            friction_coefficient=st.slider(
                "Friction coefficient",
                min_value=0.0,
                max_value=5.0,
                value=0.7,
                step=0.01,
                format="%.2f",
            ),
            plane_length=st.slider(
                "Plane length (m)",
                min_value=1.0,
                max_value=1000.0,
                value=20.0,
                step=0.1,
                format="%.1f",
            ),
        )

        with st.expander("Calculated parameters", expanded=True):
            st.html(
                f"Plane height: <b>{environment.plane_height:.2f} m</b>"
                f"<br>"
                f"Ball center position X: <b>{ball.get_position_x(environment):.2f} m</b>"
                f"<br>"
                f"Ball center position Y: <b>{ball.get_position_y(environment):.2f} m</b>"
            )

        with st.expander("Constants used"):
            st.html(f"g = {g} m/s<sup>2</sup>")

    calculator = Calculator(ball=ball, env=environment)
    balls = tuple(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    st.subheader("Ball parameters over time")

    column1, column2 = st.columns(2)

    column1.write("**Ball translational velocity (m/s)**")
    plot_ball_property(
        column1,
        balls,
        lambda b: b.translational_velocity,
        "Translational Velocity",
    )

    column2.write("**Ball angular velocity (rotations per second)**")
    plot_ball_property(
        column2,
        balls,
        lambda b: b.angular_velocity / (2 * math.pi),
        "Angular Velocity",
    )

    column1.write("**Ball position X (m)**")
    plot_ball_property(
        column1,
        balls,
        lambda b: b.get_position_x(environment),
        "Position X",
    )

    column2.write("**Ball position Y (m)**")
    plot_ball_property(
        column2,
        balls,
        lambda b: b.get_position_y(environment),
        "Position Y",
    )
