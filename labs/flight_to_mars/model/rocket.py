from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rocket:
    x: float
    y: float
    velocity_x: float
    velocity_y: float
    netto_mass: float
    fuel_mass: float
    stream_velocity: float
    fuel_consumption: float | None = field(default=None)
    acceleration_x: float | None = field(default=None)
    acceleration_y: float | None = field(default=None)

    @property
    def mass(self) -> float:
        return self.netto_mass + self.fuel_mass

    @property
    def velocity(self) -> float:
        return (self.velocity_x**2 + self.velocity_y**2) ** 0.5

    @property
    def acceleration(self) -> float:
        return (self.acceleration_x**2 + self.acceleration_y**2) ** 0.5
