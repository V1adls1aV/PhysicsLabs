from collections.abc import Callable

from scipy.integrate import ode

from labs.flight_to_mars.model.rocket import Rocket


class RocketFlightCalculator:
    def __init__(
        self,
        rocket: Rocket,
        flight_equation: Callable[[Rocket, float, float, float], list[float]],
    ) -> None:
        y0 = [rocket.y, rocket.velocity, rocket.mass]
        self.rocket = rocket
        self.equation_y = (
            ode(f=lambda _, v: flight_equation(rocket, *v))
            .set_integrator("dopri5")
            .set_initial_value(y0, 0)
        )

    def __call__(self, time_delta: float) -> Rocket:
        y, velocity, mass = self.equation_y.integrate(self.equation_y.t + time_delta)
        return Rocket(
            y=y,
            velocity=velocity,
            netto_mass=self.rocket.netto_mass,
            fuel_mass=mass - self.rocket.netto_mass,
            fuel_consumption=self.rocket.fuel_consumption,
            stream_velocity=self.rocket.stream_velocity,
        )
