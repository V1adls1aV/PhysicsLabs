from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rocket:
    y: float
    velocity: float
    netto_mass: float
    fuel_mass: float
    stream_velocity: float
    fuel_consumption: float | None = field(default=None)
    acceleration: float | None = field(default=None)

    @property
    def mass(self) -> float:
        return self.netto_mass + self.fuel_mass
