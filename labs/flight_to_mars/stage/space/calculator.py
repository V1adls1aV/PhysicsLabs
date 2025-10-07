from collections.abc import Callable

from scipy.integrate import ode

from labs.flight_to_mars.model.planet import Planet
from labs.flight_to_mars.model.rocket import Rocket


class RocketInterplanetaryFlightCalculator:
    def __init__(
        self,
        rocket: Rocket,
        flight_equation: Callable[[float, float, float, float, list[Planet]], list[float]],
        planets: list[Planet],
    ) -> None:
        x0 = (rocket.x, rocket.y, rocket.velocity_x, rocket.velocity_y)
        self.rocket = rocket
        self.equation = (
            ode(f=lambda _, v: flight_equation(v[0], v[1], v[2], v[3], planets))
            .set_integrator("dopri5")
            .set_initial_value(x0, 0)
        )
        self.previous_velocity_x = rocket.velocity_x
        self.previous_velocity_y = rocket.velocity_y

    def __call__(self, time_delta: float) -> Rocket:
        if time_delta == 0:
            return self.rocket

        x, y, velocity_x, velocity_y = self.equation.integrate(self.equation.t + time_delta)
        acceleration_x = (velocity_x - self.previous_velocity_x) / time_delta
        acceleration_y = (velocity_y - self.previous_velocity_y) / time_delta
        self.previous_velocity_x = velocity_x
        self.previous_velocity_y = velocity_y
        return Rocket(
            x=x,
            y=y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            acceleration_x=acceleration_x,
            acceleration_y=acceleration_y,
            stream_velocity=self.rocket.stream_velocity,
            netto_mass=self.rocket.netto_mass,
            fuel_mass=self.rocket.fuel_mass,
        )
