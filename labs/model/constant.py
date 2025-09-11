import streamlit as st

G = 9.81


def linear_kdm() -> float:
    return st.session_state.linear_air_resistance_rate / st.session_state.rock_mass


def quadratic_kdm() -> float:
    return st.session_state.quadratic_air_resistance_rate / st.session_state.rock_mass
