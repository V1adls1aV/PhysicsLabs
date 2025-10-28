class AdaptiveSampler:
    """Adjusts sampling rate based on feedback."""

    def __init__(self, period: float) -> None:
        self._period = period

    def get_delta(self) -> float:
        raise NotImplementedError
