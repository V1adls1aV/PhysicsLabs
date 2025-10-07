import pytest

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.equation import fixed_acceleration_flight_equation
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, G, g
from tests.util import relative_error_check


@pytest.mark.parametrize(
    ("initial_mass", "fuel_ratio", "acceleration", "stream_velocity", "expected_time"),
    [
        (
            100_000,
            0.90,
            3 * g,
            6500,
            337,
        ),
        (
            200_000,
            0.95,
            2 * g,
            5000,
            486,
        ),
        (
            300_000,
            0.98,
            5 * g,
            6000,
            209,
        ),
    ],
)
def test_earth_stage_physics(
    initial_mass: float,
    fuel_ratio: float,
    acceleration: float,
    stream_velocity: float,
    expected_time: float,
) -> None:
    """Test Earth stage escape physics with expected values from calculations"""
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass

    # Create initial rocket
    initial_rocket = Rocket(
        x=0,
        y=EARTH_RADIUS,  # Start at Earth's surface
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity,
        acceleration_x=0,
        acceleration_y=acceleration,
    )

    # Create calculator and simulate flight
    calculator = RocketFlightCalculator(
        rocket=initial_rocket,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )

    sampling_delta = 1
    rockets = list(simulate_flight(calculator, sampling_delta))

    last_rocket = rockets[-1]
    escape_velocity = (2 * G * EARTH_MASS / last_rocket.y) ** 0.5

    assert last_rocket.velocity >= escape_velocity, "Rocket should escape Earth's gravity"
    assert relative_error_check(len(rockets) - 1, expected_time / sampling_delta, 0.01)
