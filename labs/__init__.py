__all__ = ["pages"]

import streamlit as st

from .flight_to_mars import page as flight_to_mars_page
from .roll_the_ball import page as roll_the_ball_page
from .swing_the_pendulum import page as swing_the_pendulum_page
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
        swing_the_pendulum_page,
        title="Swing the pendulum",
        icon="🦯",
        url_path="swing-the-pendulum",
    ),
]
