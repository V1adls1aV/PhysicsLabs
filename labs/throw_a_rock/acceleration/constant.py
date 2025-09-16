import numpy as np

from labs.model.constant import G
from labs.throw_a_rock.acceleration.variation_law import (
    AccelerationVariationLaw,
    AccelerationVariationLawByAxis,
)

from .drag import drag_factor


def acceleration_y(velocity: float) -> float:
    return -drag_factor() * np.sign(velocity) - G


def acceleration_x(_: float) -> float:
    return -drag_factor()


def acceleration_x_jacobian(_: float) -> float:
    return 0.0


def acceleration_y_jacobian(_: float) -> float:
    return 0.0


constant_acceleration_law = AccelerationVariationLaw(
    x=AccelerationVariationLawByAxis(
        equation=acceleration_x, jacobian=acceleration_x_jacobian
    ),
    y=AccelerationVariationLawByAxis(
        equation=acceleration_y, jacobian=acceleration_y_jacobian
    ),
)
