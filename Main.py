import streamlit as st

st.set_page_config(page_title="Greeting", page_icon="👋")

st.title("Hi there!")

st.markdown(
    """
    You can find here **interactive labs** (experiment simulations),
    play with parameters and enjoy materialized results!
    
    Each page represents a separate lab, where you can find experiment description,
    limits of applicability, and the playground itself.
    """
)
