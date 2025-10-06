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
        self.previous_velocity = rocket.velocity

    def __call__(self, time_delta: float) -> Rocket:
        x, velocity = self.equation_x.integrate(self.equation_x.t + time_delta)
        acceleration = (velocity - self.previous_velocity) / time_delta
        self.previous_velocity = velocity
        return Rocket(
            x=x,
            y=self.rocket.y,
            velocity=velocity,
            fuel_mass=self.rocket.fuel_mass,
            acceleration=acceleration,
            stream_velocity=self.rocket.stream_velocity,
            netto_mass=self.rocket.netto_mass,
        )
