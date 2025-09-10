import streamlit as st


def drag_factor() -> float:
    return st.session_state.air_resistance_rate / st.session_state.rock_mass
