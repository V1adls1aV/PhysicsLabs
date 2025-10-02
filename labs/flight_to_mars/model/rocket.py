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

    def with_xyvf(self, x: float, y: float, velocity: float, fuel_mass: float) -> Rocket:
        return Rocket(
            x=x,
            y=y,
            velocity=velocity,
            netto_mass=self.netto_mass,
            fuel_mass=fuel_mass,
            stream_velocity=self.stream_velocity,
            fuel_consumption=self.fuel_consumption,
            acceleration=self.acceleration,
        )

    def rotate(self) -> Rocket:
        return self.with_xyvf(self.y, self.x, self.velocity, self.fuel_mass)
