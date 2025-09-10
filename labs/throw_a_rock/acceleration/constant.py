import numpy as np

from labs.model.constant import G
from labs.throw_a_rock.acceleration.variation_law import AccelerationVariationLaw

from .drag import drag_factor


def acceleration_y(velocity: float) -> float:
    return -drag_factor() * np.sign(velocity) - G


def acceleration_x(_: float) -> float:
    return -drag_factor()


constant_acceleration_law = AccelerationVariationLaw(x=acceleration_x, y=acceleration_y)
