from collections.abc import Callable

from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import HUMAN_EXPIRATION_TIME, MAX_HUMANLY_VIABLE_OVERLOAD


def is_astronaut_dead(rocket_logs: list[Rocket]) -> bool:
    for i in range(len(rocket_logs)):
        if rocket_logs[i].acceleration > MAX_HUMANLY_VIABLE_OVERLOAD:
            return True
    return False


def get_is_astronaut_dead_from_hunger_checker() -> Callable[[], bool]:
    days_count = 0

    def is_astronaut_dead_from_hunger() -> bool:
        nonlocal days_count
        days_count += 1
        return days_count > HUMAN_EXPIRATION_TIME

    return is_astronaut_dead_from_hunger
