from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rocket:
    x: float
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

    def rotate(self) -> Rocket:
        return Rocket(
            x=self.y,
            y=self.x,
            velocity=self.velocity,
            netto_mass=self.netto_mass,
            fuel_mass=self.fuel_mass,
            stream_velocity=self.stream_velocity,
            fuel_consumption=self.fuel_consumption,
            acceleration=self.acceleration,
        )
