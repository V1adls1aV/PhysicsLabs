__all__ = ["pages"]

import streamlit as st

from .flight_to_mars import page as flight_to_mars_page
from .physical_pendulum import page as physical_pendulum_page
from .roll_the_ball import page as roll_the_ball_page
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
    st.Page(
        roll_the_ball_page,
        title="Roll the ball",
        icon="⚽",
        url_path="roll-the-ball",
    ),
    st.Page(
        physical_pendulum_page,
        title="Physical Pendulum",
        url_path="physical-pendulum",
    ),
]
