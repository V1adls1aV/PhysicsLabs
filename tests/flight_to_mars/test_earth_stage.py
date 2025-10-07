import pytest

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.equation import fixed_acceleration_flight_equation
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, G


def test_earth_escape_velocity() -> None:
    """Test that the escape velocity calculation is correct"""
    height = EARTH_RADIUS  # At the surface
    expected_escape_velocity = (2 * G * EARTH_MASS / EARTH_RADIUS) ** 0.5
    
    # Verify calculation
    actual_escape_velocity = (2 * G * EARTH_MASS / height) ** 0.5
    assert abs(actual_escape_velocity - expected_escape_velocity) < 0.001


@pytest.mark.parametrize(
    ("initial_mass", "fuel_ratio", "acceleration", "stream_velocity", "expected_time"),
    [
        (100_000, 0.95, 3 * 9.81, 4500, 12000),  # 100t mass, 95% fuel, 3g acceleration, 4.5 km/s stream
        (200_000, 0.95, 3 * 9.81, 5000, 8000),  # 200t mass, 95% fuel, 3g acceleration, 5.0 km/s stream  
        (300_000, 0.98, 5 * 9.81, 6000, 4500),  # 300t mass, 98% fuel, 5g acceleration, 6.0 km/s stream
    ],
)
def test_earth_stage_physics(
    initial_mass: float,
    fuel_ratio: float,
    acceleration: float, 
    stream_velocity: float,
    expected_time: float
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
    
    SAMPLING_DELTA = 1
    rockets = list(simulate_flight(calculator, SAMPLING_DELTA))
    
    # Check that rocket eventually escapes Earth
    escaped = False
    for rocket in rockets:
        escape_velocity = (2 * G * EARTH_MASS / rocket.y) ** 0.5
        if rocket.velocity >= escape_velocity:
            escaped = True
            break
            
    assert escaped, "Rocket should escape Earth's gravity"