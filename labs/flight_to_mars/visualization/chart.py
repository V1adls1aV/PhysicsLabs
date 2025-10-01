from __future__ import annotations

from collections.abc import Sequence

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.earth.criteria import get_earth_escape_velocity
from labs.model.constant import EARTH_RADIUS, g


def _time_axis(rockets: Sequence[Rocket]) -> list[float]:
    """Generate time axis based on sampling delta."""
    sampling_delta = float(st.session_state.get("sampling_delta", 1))
    return [i * sampling_delta for i in range(len(rockets))]


def plot_velocity(container: DeltaGenerator, rockets: Sequence[Rocket]) -> None:
    """Plot velocity chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    velocity = [r.velocity for r in rockets]
    escape_velocity = [get_earth_escape_velocity(r.y) for r in rockets]
    velocity_gap = [e - v for v, e in zip(velocity, escape_velocity, strict=True)]

    container.line_chart(
        {
            "Time (s)": time,
            "Velocity (m/s)": velocity,
            "Escape Velocity (m/s)": escape_velocity,
            "Velocity Gap (m/s)": velocity_gap,
        },
        x="Time (s)",
        y=["Velocity (m/s)", "Escape Velocity (m/s)", "Velocity Gap (m/s)"],
        color=["#1f77b4", "#ff7f0e", "#5e5e5e"],
    )


def plot_mass(container: DeltaGenerator, rockets: Sequence[Rocket]) -> None:
    """Plot mass chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    mass = [r.mass for r in rockets]
    netto_mass = [r.netto_mass for r in rockets]
    container.line_chart(
        {"Time (s)": time, "Mass (kg)": mass, "Netto Mass (kg)": netto_mass},
        x="Time (s)",
        y=["Mass (kg)", "Netto Mass (kg)"],
    )


def plot_y_position(container: DeltaGenerator, rockets: Sequence[Rocket]) -> None:
    """Plot height chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    y_values = [r.y - EARTH_RADIUS for r in rockets]
    container.line_chart({"Time (s)": time, "Height (m)": y_values}, x="Time (s)", y="Height (m)")


def plot_acceleration(container: DeltaGenerator, rockets: Sequence[Rocket]) -> None:
    """Plot acceleration chart with all data at once."""
    if len(rockets) < 2:
        return

    sampling_delta = float(st.session_state.get("sampling_delta", 1))
    time = _time_axis(rockets)[:-1]  # Exclude last point since we need i+1
    acceleration = [
        (rockets[i + 1].velocity - rockets[i].velocity) / sampling_delta / g
        for i in range(len(rockets) - 1)
    ]
    container.line_chart(
        {"Time (s)": time, "Acceleration (g)": acceleration},
        x="Time (s)",
        y="Acceleration (g)",
    )
