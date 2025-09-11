from enum import StrEnum


class CorrelationType(StrEnum):
    CONSTANT = "constant"
    LINEAR = "linear"
    QUADRATIC = "quadratic"


relation_degrees = [
    CorrelationType.CONSTANT,
    CorrelationType.LINEAR,
    CorrelationType.QUADRATIC,
]
