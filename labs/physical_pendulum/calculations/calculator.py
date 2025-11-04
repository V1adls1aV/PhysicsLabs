# ruff: noqa: ARG002
from math import sin

from scipy.integrate import ode

from labs.model.constant import g

from ..model import PendulumState


class AngleCalculator:
    def __init__(self, initial_state: PendulumState, friction_coefficient: float) -> None:
        self.initial_state = initial_state
        self.weight = initial_state.weight
        self.length = initial_state.length
        self.moment_of_inertia = initial_state.moment_of_inertia

        self.friction_coefficient = friction_coefficient

        self.solver = ode(self.__system).set_initial_value(
            t=0.0, y=[initial_state.angle, initial_state.angular_velocity]
        )

    def __system(self, t: float, y: list[float]) -> list[float]:
        angle, angular_vel = y

        d_angle = angular_vel
        d_vel = -self.weight * g * self.length * round(sin(angle), 15) / 2 / self.moment_of_inertia

        d_vel -= (
            self.friction_coefficient * (self.length**3) * angular_vel / self.moment_of_inertia / 3
        )

        return [
            d_angle,
            d_vel,
        ]

    def __call__(self, time_delta: float) -> PendulumState:
        angle, angular_velocity = self.solver.integrate(self.solver.t + time_delta)

        return PendulumState(
            length=self.length,
            weight=self.weight,
            angle=angle,
            time=self.solver.t,
            angular_velocity=angular_velocity,
        )
