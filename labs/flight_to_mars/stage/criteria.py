import streamlit as st

from labs.flight_to_mars.model.rocket import Rocket


def is_astronaut_dead(rocket_logs: list[Rocket]) -> bool:
    for i in range(len(rocket_logs) - 1):
        approximate_acceleration = (
            rocket_logs[i + 1].velocity - rocket_logs[i].velocity
        ) / st.session_state.sampling_delta

        if approximate_acceleration >= 10:
            return True
    return False
