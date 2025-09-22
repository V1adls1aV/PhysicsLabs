import pytest
import streamlit as st

from labs.model.enum import CorrelationType
from labs.throw_a_rock.motion.compute import compute_flight_time

from .util import SAMPLING_DELTA, assert_accuracy, compute_trajectory


@pytest.mark.parametrize(
    (
        "initial_velocity",
        "angle",
        "mass",
        "resistance_rate",
        "expected_flight_time",
        "expected_flight_distance",
    ),
    [
        (42,   42,  4.2,   0.42,  5.27,   127.83),
        (69,   69,  6.9,   0.69,  11.12,  165.91),
        (228,  28,  2.28,  0.28,  16.56,  1424.79),
    ],
)  # fmt: skip
def test_linear(
    initial_velocity: float,
    angle: float,
    mass: float,
    resistance_rate: float,
    expected_flight_time: float,
    expected_flight_distance: float,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(st.session_state, "air_resistance_rate", resistance_rate)
    monkeypatch.setitem(st.session_state, "rock_mass", mass)
    trajectory = compute_trajectory(initial_velocity, angle, CorrelationType.LINEAR)

    flight_distance = trajectory[-1][0].x
    flight_time = compute_flight_time(trajectory, SAMPLING_DELTA)

    assert_accuracy(flight_time, flight_distance, expected_flight_time, expected_flight_distance)
