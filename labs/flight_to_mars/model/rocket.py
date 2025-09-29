from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rocket:
    y: float
    velocity: float
    netto_mass: float
    fuel_mass: float
    fuel_consumption: float
    stream_velocity: float

    @property
    def mass(self) -> float:
        return self.netto_mass + self.fuel_mass
