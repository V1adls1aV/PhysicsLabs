from labs.flight_to_mars.model.rocket import Rocket


def did_reach_the_target(target_x: float, rocket: Rocket) -> bool:
    return target_x <= rocket.x


def did_turn_back(rocket: Rocket) -> bool:
    return rocket.velocity_x < 0
