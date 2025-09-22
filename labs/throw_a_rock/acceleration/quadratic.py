from labs.model.constant import G

from .drag import drag_factor
from .variation_law import AccelerationVariationLaw


def acceleration_y(velocity: float) -> float:
    return -(drag_factor() * velocity**2) - G


def acceleration_x(velocity: float) -> float:
    return -(drag_factor() * velocity**2)


quadratic_acceleration_law = AccelerationVariationLaw(x=acceleration_x, y=acceleration_y)
