from math import cos, sin, tan

ROUNDING_PRECISION = 15


def sin_rounded(angle: float) -> float:
    return round(sin(angle), ROUNDING_PRECISION)


def cos_rounded(angle: float) -> float:
    return round(cos(angle), ROUNDING_PRECISION)


def tan_rounded(angle: float) -> float:
    return round(tan(angle), ROUNDING_PRECISION)
