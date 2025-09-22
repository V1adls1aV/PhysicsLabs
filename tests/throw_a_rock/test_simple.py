import pytest
import streamlit as st

from labs.model.enum import CorrelationType
from labs.throw_a_rock.motion.compute import compute_flight_time

from .util import SAMPLING_DELTA, assert_accuracy, compute_trajectory


@pytest.mark.parametrize(
    ("initial_velocity", "angle", "expected_flight_time", "expected_flight_distance"),
    [
        (42,   42,  5.73,   178.83),
        (69,   69,  13.13,  324.74),
        (228,  28,  21.82,  4393.13),
    ],
)  # fmt: skip
def test_simple(
    initial_velocity: float,
    angle: float,
    expected_flight_time: float,
    expected_flight_distance: float,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(st.session_state, "air_resistance_rate", 0)
    monkeypatch.setitem(st.session_state, "rock_mass", 1)  # does not really matter
    trajectory = compute_trajectory(initial_velocity, angle, CorrelationType.LINEAR)

    flight_distance = trajectory[-1][0].x
    flight_time = compute_flight_time(trajectory, SAMPLING_DELTA)

    assert_accuracy(flight_time, flight_distance, expected_flight_time, expected_flight_distance)
