from math import radians

import streamlit as st

from .calculations import AngleCalculator, simulate
from .calculations.util import calculate_mean_period, calculate_theoretical_period
from .model import PendulumState


def page() -> None:
    st.title("Pendulum[DEBUG]")

    start_state = PendulumState(
        weight=st.sidebar.slider("Weight, kg", 0.1, 10.0, 1.0),
        length=st.sidebar.slider("Length, m", 0.1, 10.0, 1.0),
        angle=radians(st.sidebar.slider("Angle, degree", 0.0, 90.0, 30.0)),
    )

    calculator = AngleCalculator(
        initial_state=start_state,
        friction_coefficient=st.sidebar.slider("Friction", 0.0, 10.0, 1.0),
    )

    simulation_time = st.sidebar.number_input("Simulation time", 0.2, 10.0, 5.0)

    if st.sidebar.button("Calculate"):
        st.write("## Charts")

        values, extremes = tuple(simulate(calculator, 0.01, simulation_time))

        st.line_chart(values, x="time", y="angle")
        st.line_chart(values, x="time", y="angular_velocity")
        st.line_chart(
            [
                {
                    "energy": value.full_energy,
                    "potential": value.potential_energy,
                    "rotational": value.rotational_energy,
                    "time": value.time,
                }
                for value in values
            ],
            x="time",
        )

        if calculator.friction_coefficient == 0:
            col1, col2 = st.columns(2)
            with col1:
                st.write("#### Theoretical period")
                st.write(f"{calculate_theoretical_period(start_state.length):.4f} s")
            with col2:
                st.write("#### Actual period")
                st.write(f"{calculate_mean_period(extremes):.4f} s")

        st.write("## Extremes")
        st.table(
            [
                {
                    "angle": value.angle,
                    "time": value.time,
                }
                for value in extremes
            ]
        )
