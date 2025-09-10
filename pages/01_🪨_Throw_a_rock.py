import streamlit as st

from labs.model.enum import relation_degrees
from labs.model.vector import Vector2D, to_dataframe
from labs.throw_a_rock.trajectory import calculate_next_velocity, make_step

st.title("Throw a Rock 🪨")


with st.sidebar:
    sampling_rate: float = st.slider(
        "Sampling rate, sec", min_value=0.01, max_value=1.0, value=0.1, step=0.01
    )
    v: float = st.slider(
        "Velocity, m/s", min_value=0.0, max_value=334.0, value=10.0, step=0.01
    )
    angle: float = st.slider(
        "Angle, deg", min_value=0.0, max_value=90.0, value=45.0, step=1.0
    )
    mass: float = st.slider(
        "Mass, kg", min_value=0.001, max_value=10.0, value=1.0, step=0.001
    )

    resistance_type: str = st.radio("Air resistance type", relation_degrees)

    # K-resistance choice here


time_delta = 0.2
velocity = Vector2D(v / (2**0.5), v / (2**0.5))

previous_point = Vector2D(0, 0)
coordinates = [previous_point]


for i in range(20):
    new_point = make_step(previous_point, velocity, time_delta)
    velocity = calculate_next_velocity(velocity, time_delta)
    # Display vectors.
    # Keep axes ratio 1:1
    # chart.add_rows(to_dataframe([new_point]))
    previous_point = new_point
    coordinates.append(new_point)


chart = st.line_chart(to_dataframe(coordinates))
