__all__ = ["pages"]

import streamlit as st

from .flight_to_mars import page as flight_to_mars_page
from .throw_a_rock import page as throw_a_rock_page

pages = [
    st.Page(
        throw_a_rock_page,
        title="Throw a rock",
        icon="🪨",
        url_path="throw-a-rock",
    ),
    st.Page(
        flight_to_mars_page,
        title="Flight to Mars",
        icon="🚀",
        url_path="flight-to-mars",
    ),
]
