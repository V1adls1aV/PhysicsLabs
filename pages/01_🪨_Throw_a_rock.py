import streamlit as st

from labs.model.enum import relation_degrees, RelationDegree
from labs.model.vector import Vector2D, to_dataframe
from labs.throw_a_rock.trajectory import calculate_next_velocity, make_step

st.set_page_config(layout="wide")

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

    resistance_type: RelationDegree = st.radio("Air resistance type", relation_degrees)

    match resistance_type:
        case RelationDegree.LINEAR:
            linear_resistance_rate: float = st.slider(
                "Linear resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
            )
        case RelationDegree.QUADRATIC:
            quadratic_resistance_rate: float = st.slider(
                "Quadratic resistance rate",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.01,
            )


st.title("Throw a Rock 🪨")

time_delta = 0.2
velocity = Vector2D(v / (2**0.5), v / (2**0.5))

previous_point = Vector2D(0.0, 0.0)
coordinates = [previous_point]

chart = st.scatter_chart(
    to_dataframe(coordinates), x="x", y="y", x_label="x, meters", y_label="y, meters"
)

while previous_point.y >= 0.0:
    new_point = make_step(previous_point, velocity, time_delta)
    velocity = calculate_next_velocity(velocity, time_delta)
    # Display vectors.
    # chart.add_rows(to_dataframe([new_point]))
    previous_point = new_point
    coordinates.append(new_point)
    chart.add_rows(to_dataframe([new_point]))
