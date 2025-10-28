from ..model import Ball, Environment
from .movement import move_with_slippage, move_without_slippage
from .utils import is_movement_without_slippage_possible, is_slippage_finished


class Calculator:
    def __init__(self, ball: Ball, env: Environment) -> None:
        self.env = env
        self.current_ball = ball

    def __call__(self, time_delta: float) -> Ball:
        if not is_movement_without_slippage_possible(self.env):
            return move_with_slippage(self.current_ball, self.env, time_delta)
        if is_slippage_finished(self.current_ball):
            return move_without_slippage(self.current_ball, self.env, time_delta)
        return move_with_slippage(self.current_ball, self.env, time_delta)


def is_simulation_finished(ball: Ball, env: Environment) -> bool:
    return ball.position >= env.plane_length
