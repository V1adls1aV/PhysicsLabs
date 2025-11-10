import pytest

from labs.roll_the_ball.config import SAMPLING_DELTA
from labs.roll_the_ball.simulation import Calculator, simulate

from .data import SLIPPING_INPUT, PlainInput


@pytest.mark.parametrize("data", SLIPPING_INPUT)
def test_instant_slippage_on_incline(data: PlainInput) -> None:
    calculator = Calculator(ball=data.ball, env=data.environment)
    tuple(simulate(calculator, sampling_delta=SAMPLING_DELTA))
    assert not check_slippage_did_not_start(calculator)


def check_slippage_did_not_start(calculator: Calculator) -> bool:
    return calculator.slippage_end_time is None
