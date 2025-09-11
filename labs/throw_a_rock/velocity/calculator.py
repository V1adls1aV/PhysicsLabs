from scipy.integrate import ode

from labs.model.vector import Vector2D

from ...model.constant import linear_kdm
from .linear_resistance import acceleration_x, acceleration_y


class VelocityCalculator:
    def __init__(self, initial_velocity: Vector2D, sampling_delta: float):
        self.sampling_delta = sampling_delta
        self.equation_x = (
            ode(
                f=lambda _, y: acceleration_x(y),
                jac=lambda _, y: -linear_kdm() * acceleration_x(y),
            )
            .set_integrator("lsoda")
            .set_initial_value(initial_velocity.x)
        )
        self.equation_y = (
            ode(
                f=lambda _, y: acceleration_y(y),
                jac=lambda _, y: -linear_kdm() * acceleration_y(y),
            )
            .set_integrator("vode", method="bdf")
            .set_initial_value(initial_velocity.y)
        )

    def __call__(self) -> Vector2D:
        return Vector2D(
            x=float(
                self.equation_x.integrate(self.equation_x.t + self.sampling_delta)[0]
            ),
            y=float(
                self.equation_y.integrate(self.equation_y.t + self.sampling_delta)[0]
            ),
        )
