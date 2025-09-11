import streamlit as st


def constant_drag_factor() -> float:
    return st.session_state.constant_air_resistance_rate / st.session_state.rock_mass


def linear_drag_factor() -> float:
    return st.session_state.linear_air_resistance_rate / st.session_state.rock_mass


def quadratic_drag_factor() -> float:
    return st.session_state.quadratic_air_resistance_rate / st.session_state.rock_mass
