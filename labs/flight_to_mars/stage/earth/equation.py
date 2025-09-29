from labs.flight_to_mars.model.rocket import Rocket
from labs.model.constant import EARTH_MASS, G


def rocket_flight_equation(rocket: Rocket, y: float, velocity: float, mass: float) -> list[float]:
    g = G * EARTH_MASS / y**2

    if mass - rocket.netto_mass <= 0:
        return [velocity, -g, 0]

    dhdt = velocity
    dvdt = (rocket.fuel_consumption * rocket.stream_velocity / mass) - g
    dmdt = -rocket.fuel_consumption

    return [dhdt, dvdt, dmdt]
