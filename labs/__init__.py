__all__ = ["pages"]

import streamlit as st

from .throw_a_rock import page as throw_a_rock_page

pages = [
    st.Page(
        throw_a_rock_page,
        title="Throw a rock",
        icon="🪨",
        url_path="throw-a-rock",
    ),
]
