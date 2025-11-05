import math

import streamlit as st

from labs.model.constant import g

from .model import PendulumState
from .simulation import PendulumCalculator, simulate
from .simulation.util import calculate_mean_period, calculate_theoretical_period


def page() -> None:
    st.set_page_config(page_title="Swing the pendulum 🦯", page_icon="🦯", layout="wide")

    st.title("Swing the pendulum 🦯")

    with st.sidebar:
        start_state = PendulumState(
            weight=st.slider("Weight, kg", 0.1, 100.0, 1.0),
            length=st.slider("Length, m", 0.1, 10.0, 1.0),
            angle=math.radians(st.slider("Angle, deg", 0.0, 179.0, 3.0)),
        )

        friction_coefficient = st.slider("Friction coefficient", 0.0, 10.0, 1.0)

        simulation_time = st.number_input("Simulation time", 0.2, 50.0, 5.0)

        with st.expander("Constants used"):
            st.html(f"g = {g} m/s<sup>2</sup>")

    calculator = PendulumCalculator(
        initial_state=start_state,
        friction_coefficient=friction_coefficient,
    )
    states, extreme_states = tuple(simulate(calculator, 0.01, simulation_time))

    st.subheader("Pendulum parameters over time")

    chart_column_1, chart_column_2 = st.columns(2)

    chart_column_1.line_chart(
        states,
        x="time",
        y="angle",
        x_label="Time (s)",
        y_label="Angle (rad)",
        color="#1f77b4",
    )
    chart_column_2.line_chart(
        states,
        x="time",
        y="angular_velocity",
        x_label="Time (s)",
        y_label="Angular velocity (rad/s)",
        color="#1f77b4",
    )

    st.line_chart(
        [
            {
                "Time (s)": state.time,
                "Full energy (J)": state.full_energy,
                "Potential energy (J)": state.potential_energy,
                "Rotational energy (J)": state.rotational_energy,
            }
            for state in states
        ],
        x="Time (s)",
        color=("#1f77b4", "#ff7f0e", "#00bb54"),
    )

    with st.container(horizontal=True, horizontal_alignment="center", gap="large"):
        st.metric(
            "Theoretical period",
            f"{calculate_theoretical_period(start_state.length):.3f} s",
            width="content",
        )
        st.metric(
            "Calculated period",
            (
                f"{calculate_mean_period(extreme_states):.3f} s"
                if len(extreme_states) >= 2
                else None
            ),
            width="content",
        )

    _, center_column, _ = st.columns(3)

    with center_column:
        st.subheader("Extreme states", width="content")
        st.table(
            [
                {
                    "angle": f"{state.angle:+.4f} rad",
                    "time": f"{state.time:.2f} s",
                }
                for state in extreme_states
            ]
        )
