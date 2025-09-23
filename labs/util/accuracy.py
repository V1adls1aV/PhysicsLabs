import math


def round_to_significant(value: float, significant: int = 3) -> float:
    if value == 0:
        return 0
    return round(value, -math.floor(math.log10(abs(value))) + significant - 1)
