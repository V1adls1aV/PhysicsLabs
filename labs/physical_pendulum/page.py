from math import radians

import streamlit as st

from .calculations import AngleCalculator, simulate
from .model import PendulumState


def page() -> None:
    st.title("Pendulum[DEBUG]")

    start_state = PendulumState(
        weight=st.sidebar.slider("Weight, kg", 0.1, 10.0, 1.0),
        length=st.sidebar.slider("Length, m", 0.1, 10.0, 1.0),
        angle=radians(st.sidebar.slider("Angle, degree", 0.0, 90.0, 30.0)),
    )

    calculator = AngleCalculator(
        initial_state=start_state, friction_coefficient=st.sidebar.slider("Friction", 0.0, 5.0, 1.0)
    )

    if st.button("Calculate"):
        values = tuple(simulate(calculator, 0.01, 5))
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
