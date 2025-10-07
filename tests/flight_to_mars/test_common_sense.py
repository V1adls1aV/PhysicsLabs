import pytest

from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.criteria import get_planet_escape_velocity
from labs.flight_to_mars.stage.planet.equation import fixed_acceleration_flight_equation
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.model.constant import EARTH_MASS, EARTH_RADIUS, g


def test_higher_acceleration_means_faster_escape() -> None:
    """Test that higher acceleration results in faster escape from Earth"""
    rocket_slow = _create_rocket_with_acceleration(2 * g)
    calculator_slow = RocketFlightCalculator(
        rocket=rocket_slow,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    sampling_delta = 1
    rockets_slow = list(simulate_flight(calculator_slow, sampling_delta))

    rocket_fast = _create_rocket_with_acceleration(5 * g)
    calculator_fast = RocketFlightCalculator(
        rocket=rocket_fast,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_fast = list(simulate_flight(calculator_fast, sampling_delta))

    velocity_threshold = 5000  # 5 km/s
    time_slow = _find_time_to_velocity(rockets_slow, velocity_threshold)
    time_fast = _find_time_to_velocity(rockets_fast, velocity_threshold)

    assert time_fast < time_slow, "Higher acceleration should reach velocity threshold faster"


def test_rockets_with_higher_stream_velocity_travels_faster() -> None:
    """Test that rockets with higher stream velocity achieve higher speeds faster"""
    rocket_slow = _create_rocket_with_stream_velocity(4000)  # 4 km/s
    calculator_slow = RocketFlightCalculator(
        rocket=rocket_slow,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    sampling_delta = 1
    rockets_slow = list(simulate_flight(calculator_slow, sampling_delta))

    rocket_fast = _create_rocket_with_stream_velocity(6000)  # 6 km/s
    calculator_fast = RocketFlightCalculator(
        rocket=rocket_fast,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_fast = list(simulate_flight(calculator_fast, sampling_delta))

    if rockets_slow and rockets_fast:
        final_velocity_slow = rockets_slow[-1].velocity
        final_velocity_fast = rockets_fast[-1].velocity
        assert final_velocity_fast >= final_velocity_slow, (
            "Higher stream velocity should result in higher final velocity"
        )


def test_escape_velocity_increases_with_planet_mass() -> None:
    """Test that escape velocity increases with planet mass"""
    height = EARTH_RADIUS

    escape_vel_earth = get_planet_escape_velocity(height, EARTH_MASS)
    escape_vel_heavy = get_planet_escape_velocity(height, EARTH_MASS * 2)

    assert escape_vel_heavy > escape_vel_earth, "Escape velocity should increase with planet mass"


@pytest.mark.filterwarnings("ignore:.*step size.*")
def test_higher_fuel_means_longer_flight() -> None:
    """Test that higher fuel ratio allows for longer flight time"""
    sampling_delta = 1

    rocket_low_fuel = _create_rocket_with_fuel_ratio(0.90)
    calculator_low = RocketFlightCalculator(
        rocket=rocket_low_fuel,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_low = list(simulate_flight(calculator_low, sampling_delta))

    rocket_high_fuel = _create_rocket_with_fuel_ratio(0.98)
    calculator_high = RocketFlightCalculator(
        rocket=rocket_high_fuel,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_high = list(simulate_flight(calculator_high, sampling_delta))

    if rockets_low and rockets_high:
        final_altitude_low = rockets_low[-1].y - EARTH_RADIUS
        final_altitude_high = rockets_high[-1].y - EARTH_RADIUS

        assert final_altitude_high >= final_altitude_low, (
            "More fuel should result in higher altitude with same acceleration"
        )
        assert len(rockets_high) >= len(rockets_low), (
            "More fuel should allow for longer flight simulation"
        )


def _create_rocket_with_acceleration(acceleration: float) -> Rocket:
    """Helper function to create a rocket with specified acceleration"""
    initial_mass = 100_000  # 100 tons
    fuel_ratio = 0.90
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    stream_velocity = 4500  # 4.5 km/s

    return Rocket(
        x=0,
        y=EARTH_RADIUS,
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity,
        acceleration_x=0,
        acceleration_y=acceleration,
    )


def _create_rocket_with_fuel_ratio(fuel_ratio: float) -> Rocket:
    """Helper function to create a rocket with specified fuel ratio"""
    initial_mass = 100_000  # 100 tons
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    stream_velocity = 4500  # 4.5 km/s
    acceleration = 3 * g

    return Rocket(
        x=0,
        y=EARTH_RADIUS,
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity,
        acceleration_x=0,
        acceleration_y=acceleration,
    )


def _create_rocket_with_stream_velocity(stream_velocity: float) -> Rocket:
    """Helper function to create a rocket with specified stream velocity"""
    initial_mass = 100_000  # 100 tons
    fuel_ratio = 0.90
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    acceleration = 3 * g  # 3g

    return Rocket(
        x=0,
        y=EARTH_RADIUS,
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity,
        acceleration_x=0,
        acceleration_y=acceleration,
    )


def _create_rocket_with_mass(initial_mass: float) -> Rocket:
    """Helper function to create a rocket with specified initial mass"""
    fuel_ratio = 0.90
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    stream_velocity = 4500  # 4.5 km/s
    acceleration = 3 * g  # 3g

    return Rocket(
        x=0,
        y=EARTH_RADIUS,
        velocity_x=0,
        velocity_y=0,
        netto_mass=netto_mass,
        fuel_mass=fuel_mass,
        stream_velocity=stream_velocity,
        acceleration_x=0,
        acceleration_y=acceleration,
    )


def _find_time_to_velocity(rockets: list[Rocket], velocity_threshold: float) -> int:
    """Helper function to find the time when velocity threshold is reached"""
    for i, rocket in enumerate(rockets):
        if rocket.velocity >= velocity_threshold:
            return i
    return len(rockets)
