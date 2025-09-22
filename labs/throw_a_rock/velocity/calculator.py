from scipy.integrate import ode

from labs.model.vector import Vector2D

from ..acceleration.variation_law import AccelerationVariationLaw


class VelocityCalculator:
    def __init__(
        self,
        initial_velocity: Vector2D,
        acceleration_law: AccelerationVariationLaw,
        sampling_delta: float,
    ) -> None:
        self.initial_velocity = initial_velocity
        self.sampling_delta = sampling_delta
        self.equation_x = (
            ode(f=lambda _, v: acceleration_law.x(v))
            .set_integrator("lsoda")
            .set_initial_value(initial_velocity.x)
        )
        self.equation_y = (
            ode(f=lambda _, v: acceleration_law.y(v))
            .set_integrator("vode", method="bdf")
            .set_initial_value(initial_velocity.y)
        )

    def __call__(self) -> Vector2D:
        return Vector2D(
            x=float(self.equation_x.integrate(self.equation_x.t + self.sampling_delta)[0]),
            y=float(self.equation_y.integrate(self.equation_y.t + self.sampling_delta)[0]),
        )
