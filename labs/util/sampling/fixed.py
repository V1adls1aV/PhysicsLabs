class FixedSampler:
    def __init__(self, period: float) -> None:
        self._period = period

    def get_delta(self) -> float:
        return self._period
