from labs.model.constant import G, linear_kdm


def acceleration_y(velocity: float) -> float:
    return -G - linear_kdm() * velocity


def acceleration_x(velocity: float) -> float:
    return -linear_kdm() * velocity
