import pytest

from labs.rolling_the_ball.config import SAMPLING_DELTA
from labs.rolling_the_ball.simulation import Calculator, simulate

from .data import EPS, GRIPPING_INPUT, PlainInput


@pytest.mark.parametrize("data", GRIPPING_INPUT)
def test_instant_grip_on_incline(data: PlainInput) -> None:
    calculator = Calculator(ball=data.ball, env=data.environment)
    tuple(simulate(calculator, sampling_delta=SAMPLING_DELTA))
    assert check_slippage_not_started(calculator)


def check_slippage_not_started(calculator: Calculator) -> bool:
    return calculator.slippage_end_time is not None and calculator.slippage_end_time < EPS
