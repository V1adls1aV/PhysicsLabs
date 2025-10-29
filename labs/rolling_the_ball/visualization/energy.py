from collections.abc import Sequence

from plotly.graph_objects import Figure, Scatter

from labs.model.constant import g

from ..config import SAMPLING_DELTA
from ..model import Ball, Environment


def plot_energy(balls: Sequence[Ball], env: Environment) -> Figure:
    timeline = tuple(i * SAMPLING_DELTA for i in range(len(balls)))

    kinetic_energies = []
    rotational_energies = []
    potential_energies = []
    total_energies = []

    for b in balls:
        kinetic = b.mass * b.translational_velocity**2 / 2
        rotational = b.rotational_inertia * b.angular_velocity**2 / 2
        potential = b.mass * g * b.get_position_y(env)

        kinetic_energies.append(kinetic)
        rotational_energies.append(rotational)
        potential_energies.append(potential)
        total_energies.append(kinetic + rotational + potential)

    return Figure(
        data=[
            Scatter(
                x=timeline,
                y=kinetic_energies,
                mode="lines",
                name="Kinetic energy",
                line={"color": "#1f77b4"},
            ),
            Scatter(
                x=timeline,
                y=rotational_energies,
                mode="lines",
                name="Rotational energy",
                line={"color": "#ff7f0e"},
            ),
            Scatter(
                x=timeline,
                y=potential_energies,
                mode="lines",
                name="Potential energy",
                line={"color": "#00bb54"},
            ),
            Scatter(
                x=timeline,
                y=total_energies,
                mode="lines",
                name="Total energy",
                line={"color": "#d62728", "width": 2},
            ),
        ],
        layout={
            "title": "Energy over time",
            "xaxis": {"title": "Time (s)"},
            "yaxis": {"title": "Energy (J)"},
            "height": 500,
        },
    )
