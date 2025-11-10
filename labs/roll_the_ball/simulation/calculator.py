from ..model import Ball, Environment
from .movement import move_with_slippage, move_without_slippage
from .util import is_movement_without_slippage_possible, is_slippage_finished


class Calculator:
    def __init__(self, ball: Ball, env: Environment) -> None:
        self.env = env
        self.current_ball = ball

        self.current_time = 0
        self.slippage_end_time: float | None = None

    def _compute_next(self, time_delta: float) -> Ball:
        if not is_movement_without_slippage_possible(self.env):
            if self.slippage_end_time is None:
                self.slippage_end_time = 0

            return move_with_slippage(self.current_ball, self.env, time_delta)

        if is_slippage_finished(self.current_ball):
            if self.slippage_end_time is None:
                self.slippage_end_time = self.current_time

            return move_without_slippage(self.current_ball, self.env, time_delta)

        return move_with_slippage(self.current_ball, self.env, time_delta)

    def __call__(self, time_delta: float) -> Ball:
        self.current_ball = self._compute_next(time_delta)
        self.current_time += time_delta
        return self.current_ball
