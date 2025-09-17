from labs.model.constant import G
from labs.throw_a_rock.acceleration.variation_law import AccelerationVariationLaw

from .drag import drag_factor


def acceleration_y(velocity: float) -> float:
    return -(drag_factor() * velocity**2) - G


def acceleration_x(velocity: float) -> float:
    return -(drag_factor() * velocity**2)


def acceleration_x_jacobian(velocity: float) -> float:
    return -2 * drag_factor() * velocity * acceleration_x(velocity)


def acceleration_y_jacobian(velocity: float) -> float:
    return -2 * drag_factor() * velocity * acceleration_y(velocity)


quadratic_acceleration_law = AccelerationVariationLaw(
    x=acceleration_x, y=acceleration_y
)
