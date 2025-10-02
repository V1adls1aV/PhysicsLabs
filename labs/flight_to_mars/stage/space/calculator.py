from collections.abc import Callable

from scipy.integrate import ode

from labs.flight_to_mars.model.rocket import Rocket


class RocketInterplanetaryFlightCalculator:
    def __init__(
        self,
        rocket: Rocket,
        flight_equation: Callable[[float, float], list[float]],
    ) -> None:
        x0 = [rocket.x, rocket.velocity]
        self.rocket = rocket
        self.equation_x = (
            ode(f=lambda _, v: flight_equation(*v))
            .set_integrator("dopri5")
            .set_initial_value(x0, 0)
        )

    def __call__(self, time_delta: float) -> Rocket:
        x, velocity = self.equation_x.integrate(self.equation_x.t + time_delta)
        return self.rocket.with_xyvf(
            x=x, y=self.rocket.y, velocity=velocity, fuel_mass=self.rocket.fuel_mass
        )
