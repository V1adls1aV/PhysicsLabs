from collections.abc import Callable

from scipy.integrate import ode

from labs.flight_to_mars.model.rocket import Rocket


class RocketFlightCalculator:
    def __init__(
        self,
        rocket: Rocket,
        planet_mass: float,
        flight_equation: Callable[[Rocket, float, float, float], list[float]],
    ) -> None:
        y0 = [rocket.y, rocket.velocity_y, rocket.mass]
        self.rocket = rocket
        self.planet_mass = planet_mass
        self.equation_y = (
            ode(f=lambda _, v: flight_equation(rocket, planet_mass, *v))
            .set_integrator("dopri5")
            .set_initial_value(y0, 0)
        )

    def __call__(self, time_delta: float) -> Rocket:
        y, velocity_y, mass = self.equation_y.integrate(self.equation_y.t + time_delta)
        return Rocket(
            x=self.rocket.x,
            y=y,
            velocity_x=self.rocket.velocity_x,
            velocity_y=velocity_y,
            netto_mass=self.rocket.netto_mass,
            fuel_mass=mass - self.rocket.netto_mass,
            stream_velocity=self.rocket.stream_velocity,
            fuel_consumption=None,
            acceleration_x=self.rocket.acceleration_x,
            acceleration_y=self.rocket.acceleration_y,
        )
