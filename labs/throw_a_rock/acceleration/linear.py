from labs.model.constant import g

from .drag import drag_factor
from .variation_law import AccelerationVariationLaw


def acceleration_y(velocity: float) -> float:
    return -(drag_factor() * velocity) - g


def acceleration_x(velocity: float) -> float:
    return -(drag_factor() * velocity)


linear_acceleration_law = AccelerationVariationLaw(x=acceleration_x, y=acceleration_y)
