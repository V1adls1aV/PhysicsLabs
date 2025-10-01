from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import EARTH_MASS, G


def fixed_fuel_rate_flight_equation(
    rocket: Rocket, y: float, velocity: float, mass: float
) -> list[float]:
    if rocket.fuel_consumption is None:
        raise ValueError("Fuel consumption is not set")

    g = G * EARTH_MASS / y**2

    if mass - rocket.netto_mass <= 0:
        return [velocity, -g, 0]

    dhdt = velocity
    dvdt = (rocket.fuel_consumption * rocket.stream_velocity / mass) - g
    dmdt = -rocket.fuel_consumption

    return [dhdt, dvdt, dmdt]


def fixed_acceleration_flight_equation(
    rocket: Rocket, y: float, velocity: float, mass: float
) -> list[float]:
    if rocket.acceleration is None:
        raise ValueError("Acceleration is not set")

    g = G * EARTH_MASS / y**2

    if mass - rocket.netto_mass <= 0:
        return [velocity, -g, 0]

    dhdt = velocity
    dvdt = rocket.acceleration
    dmdt = -(mass / rocket.stream_velocity) * (rocket.acceleration + g)

    return [dhdt, dvdt, dmdt]
