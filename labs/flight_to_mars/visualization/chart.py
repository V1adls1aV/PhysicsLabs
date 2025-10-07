from __future__ import annotations

from collections.abc import Sequence

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from labs.flight_to_mars.model.planet import Planet, norm
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.criteria import get_planet_escape_velocity
from labs.model.constant import DAY, g


def _time_axis(rockets: Sequence[Rocket]) -> list[float]:
    """Generate time axis based on sampling delta."""
    sampling_delta = float(st.session_state.get("sampling_delta", 1))
    return [i * sampling_delta for i in range(len(rockets))]


def plot_velocity(
    container: DeltaGenerator,
    rockets: Sequence[Rocket],
    planet_mass: float | None = None,
    *,
    in_days: bool = False,
) -> None:
    """Plot velocity chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    time_label = "Time (s)"
    if in_days:
        time = [t / DAY for t in time]
        time_label = "Time (days)"

    velocity = [r.velocity / 1000 for r in rockets]
    if planet_mass:
        escape_velocity = [get_planet_escape_velocity(r.y, planet_mass) / 1000 for r in rockets]
        velocity_gap = [e - v for v, e in zip(velocity, escape_velocity, strict=True)]

    # noinspection PyUnboundLocalVariable
    container.line_chart(
        {
            time_label: time,
            "Velocity (km/s)": velocity,
        }
        | (
            {"Escape Velocity (km/s)": escape_velocity, "Velocity Gap (km/s)": velocity_gap}
            if planet_mass
            else {}
        ),
        x=time_label,
        y=[
            "Velocity (km/s)",
            *(["Escape Velocity (km/s)", "Velocity Gap (km/s)"] if planet_mass else {}),
        ],
        color=["#1f77b4", *(["#ff7f0e", "#5e5e5e"] if planet_mass else {})],
    )


def plot_mass(container: DeltaGenerator, rockets: Sequence[Rocket]) -> None:
    """Plot mass chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    mass = [r.mass / 1000 for r in rockets]
    netto_mass = [r.netto_mass / 1000 for r in rockets]
    container.line_chart(
        {"Time (s)": time, "Mass (ton)": mass, "Netto Mass (ton)": netto_mass},
        x="Time (s)",
        y=["Mass (ton)", "Netto Mass (ton)"],
    )


def plot_y_position(
    container: DeltaGenerator, rockets: Sequence[Rocket], planet_radius: float
) -> None:
    """Plot height chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    y_values = [(r.y - planet_radius) / 1000 for r in rockets]
    container.line_chart({"Time (s)": time, "Height (km)": y_values}, x="Time (s)", y="Height (km)")


def plot_distance_to_target_chart(
    container: DeltaGenerator,
    rockets: Sequence[Rocket],
    target_planet: Planet,
    *,
    in_days: bool = False,
) -> None:
    """Plot distance to target chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    distance_to_target = [
        norm(target_planet.x - r.x, target_planet.y - r.y) / 1000 for r in rockets
    ]
    time_label = "Time (s)"
    if in_days:
        time = [t / DAY for t in time]
        time_label = "Time (days)"
    container.line_chart(
        {time_label: time, "Distance to Target (km)": distance_to_target},
        x=time_label,
        y="Distance to Target (km)",
    )
    container.markdown(
        f"**Minimal** distance to target planet (radius): "
        f"{(min(distance_to_target) * 1000 - target_planet.radius) / target_planet.radius:.02f}"
    )


def plot_acceleration(
    container: DeltaGenerator, rockets: Sequence[Rocket], *, in_days: bool = False
) -> None:
    """Plot acceleration chart with all data at once."""
    if not rockets:
        return

    time = _time_axis(rockets)
    time_label = "Time (s)"
    if in_days:
        time = [t / DAY for t in time]
        time_label = "Time (days)"

    acceleration = [abs(rockets[i].acceleration / g) for i in range(len(rockets))]
    container.line_chart(
        {time_label: time, "Acceleration (g)": acceleration},
        x=time_label,
        y="Acceleration (g)",
    )
