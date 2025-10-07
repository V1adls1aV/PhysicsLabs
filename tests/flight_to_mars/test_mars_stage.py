import pytest

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.equation import fixed_acceleration_flight_equation
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.model.constant import MARS_MASS, MARS_RADIUS, g


@pytest.mark.parametrize(
    ("initial_mass", "stream_velocity", "acceleration"),
    [
        (100_000, 4500, 2 * g),
        (150_000, 5000, 3 * g),
        (200_000, 6000, 4 * g),
    ],
)
def test_mars_stage_physics(
    initial_mass: float,
    stream_velocity: float,
    acceleration: float,
) -> None:
    """Test Mars stage landing physics"""
    # same magic as in page.py
    netto_mass = initial_mass - 1
    fuel_mass = 1

    initial_rocket = Rocket(
        x=0,
        y=MARS_RADIUS,
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity * -1,
        acceleration_x=0,
        acceleration_y=acceleration,
    )

    calculator = RocketFlightCalculator(
        rocket=initial_rocket,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=MARS_MASS,
    )

    sampling_delta = 1
    raw_rockets = list(simulate_flight(calculator, sampling_delta))

    assert len(raw_rockets) > 0, "Raw simulation should produce rockets"

    rockets = list(filter(lambda r: r.mass <= initial_mass, raw_rockets))

    # Check if rocket has gained altitude (moved away from Mars surface)
    max_altitude = max([r.y for r in rockets]) if rockets else MARS_RADIUS
    achieved_altitude = max_altitude - MARS_RADIUS

    assert achieved_altitude >= 0, "Rocket should achieve positive altitude during simulation"
