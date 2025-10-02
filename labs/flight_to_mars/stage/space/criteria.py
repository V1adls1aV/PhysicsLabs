from labs.flight_to_mars.model.rocket import Rocket


def does_reach_the_target(target_x: float, rocket: Rocket) -> bool:
    return target_x <= rocket.x


def does_turn_back(rocket: Rocket) -> bool:
    return rocket.velocity < 0
