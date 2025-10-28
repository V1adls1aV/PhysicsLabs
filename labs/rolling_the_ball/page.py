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
                    value=3.0,
                    step=0.1,
                    format="%.1f",
                )
            ),
            angular_velocity=0,
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
                max_value=100.0,
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

    if (
        environment.incline_angle == 0
        and ball.translational_velocity == 0
        and ball.angular_velocity == 0
    ):
        st.warning("The ball will not move with no velocity on a horizontal plane.")
        return

    calculator = Calculator(ball=ball, env=environment)
    balls = tuple(simulate(calculator, sampling_delta=SAMPLING_DELTA))

    st.subheader("Ball parameters over time")

    with st.container(horizontal=True, horizontal_alignment="center", gap="large"):
        st.metric(
            "Finish time",
            f"{len(balls) * SAMPLING_DELTA:.2f} s",
            width="content",
        )
        st.metric(
            "Slippage end time",
            (
                f"{calculator.slippage_end_time:.2f} s"
                if calculator.slippage_end_time is not None
                else None
            ),
            help="If zero — no slippage occurred. If not present — slippage never ended.",
            width="content",
        )

    chart_column_1, chart_column_2 = st.columns(2)

    chart_column_1.html("<b>Ball position X (m)</b>")
    plot_ball_property(
        container=chart_column_1,
        balls=balls,
        property_callable=lambda b: b.get_position_x(environment),
        label="Position X",
        color="#1f77b4",
    )

    chart_column_2.html("<b>Ball position Y (m)</b>")
    plot_ball_property(
        container=chart_column_2,
        balls=balls,
        property_callable=lambda b: b.get_position_y(environment),
        label="Position Y",
        color="#1f77b4",
    )

    chart_column_1.html("<b>Ball translational velocity (m/s)</b>")
    plot_ball_property(
        container=chart_column_1,
        balls=balls,
        property_callable=lambda b: b.translational_velocity,
        label="Translational velocity",
        color="#ff7f0e",
    )

    chart_column_2.html("<b>Ball angular velocity (rot/s)</b>")
    plot_ball_property(
        container=chart_column_2,
        balls=balls,
        property_callable=lambda b: b.angular_velocity / (2 * math.pi),
        label="Angular velocity",
        color="#ff7f0e",
    )

    chart_column_1.html("<b>Ball translational acceleration (m/s<sup>2</sup>)</b>")
    plot_ball_property(
        container=chart_column_1,
        balls=balls,
        property_callable=lambda b: b.translational_acceleration,
        label="Translational acceleration",
        trim_last=True,
        color="#00bb54",
    )

    chart_column_2.html("<b>Ball angular acceleration (rot/s<sup>2</sup>)</b>")
    plot_ball_property(
        container=chart_column_2,
        balls=balls,
        property_callable=lambda b: b.angular_acceleration / (2 * math.pi),
        label="Angular acceleration",
        trim_last=True,
        color="#00bb54",
    )
