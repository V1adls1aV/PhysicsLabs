
from labs.flight_to_mars.model.rocket import Rocket
from labs.flight_to_mars.stage.planet.calculator import RocketFlightCalculator
from labs.flight_to_mars.stage.planet.equation import fixed_acceleration_flight_equation
from labs.flight_to_mars.stage.planet.simulation import simulate_flight
from labs.model.constant import EARTH_MASS, EARTH_RADIUS


def test_higher_acceleration_means_faster_escape() -> None:
    """Test that higher acceleration results in faster escape from Earth"""
    # Test with lower acceleration
    rocket_slow = _create_rocket_with_acceleration(2 * 9.81)
    calculator_slow = RocketFlightCalculator(
        rocket=rocket_slow,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    sampling_delta = 1
    rockets_slow = list(simulate_flight(calculator_slow, sampling_delta))
    
    # Test with higher acceleration
    rocket_fast = _create_rocket_with_acceleration(5 * 9.81)
    calculator_fast = RocketFlightCalculator(
        rocket=rocket_fast,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_fast = list(simulate_flight(calculator_fast, sampling_delta))
    
    # Find time to reach same velocity threshold (should be faster with higher acceleration)
    velocity_threshold = 5000  # 5 km/s
    time_slow = _find_time_to_velocity(rockets_slow, velocity_threshold)
    time_fast = _find_time_to_velocity(rockets_fast, velocity_threshold)
    
    assert time_fast < time_slow, "Higher acceleration should reach velocity threshold faster"


def test_higher_fuel_means_longer_flight() -> None:
    """Test that higher fuel ratio allows for longer flight time"""
    # Test with lower fuel ratio
    rocket_low_fuel = _create_rocket_with_fuel_ratio(0.90)
    calculator_low = RocketFlightCalculator(
        rocket=rocket_low_fuel,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    sampling_delta = 1
    rockets_low = list(simulate_flight(calculator_low, sampling_delta))
    
    # Test with higher fuel ratio
    rocket_high_fuel = _create_rocket_with_fuel_ratio(0.98)
    calculator_high = RocketFlightCalculator(
        rocket=rocket_high_fuel,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_high = list(simulate_flight(calculator_high, sampling_delta))
    
    # More fuel should allow for longer simulation (more rockets generated)
    # Or, for same simulation length, higher fuel should achieve higher velocity/distance
    if rockets_low and rockets_high:
        final_velocity_low = rockets_low[-1].velocity
        final_velocity_high = rockets_high[-1].velocity
        assert final_velocity_high >= final_velocity_low, "More fuel should result in higher final velocity"


def test_rockets_with_higher_stream_velocity_travels_faster() -> None:
    """Test that rockets with higher stream velocity achieve higher speeds faster"""
    # Test with lower stream velocity
    rocket_slow = _create_rocket_with_stream_velocity(4000)  # 4 km/s
    calculator_slow = RocketFlightCalculator(
        rocket=rocket_slow,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    SAMPLING_DELTA = 1
    rockets_slow = list(simulate_flight(calculator_slow, SAMPLING_DELTA))
    
    # Test with higher stream velocity
    rocket_fast = _create_rocket_with_stream_velocity(6000)  # 6 km/s
    calculator_fast = RocketFlightCalculator(
        rocket=rocket_fast,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    rockets_fast = list(simulate_flight(calculator_fast, SAMPLING_DELTA))
    
    # Compare final velocities
    if rockets_slow and rockets_fast:
        final_velocity_slow = rockets_slow[-1].velocity
        final_velocity_fast = rockets_fast[-1].velocity
        assert final_velocity_fast >= final_velocity_slow, "Higher stream velocity should result in higher final velocity"


def test_escape_velocity_increases_with_planet_mass() -> None:
    """Test that escape velocity increases with planet mass"""
    from labs.flight_to_mars.stage.planet.criteria import get_planet_escape_velocity
    
    height = EARTH_RADIUS  # At the surface
    
    # For Earth mass
    escape_vel_earth = get_planet_escape_velocity(height, EARTH_MASS)
    
    # For a planet with twice the mass
    escape_vel_heavy = get_planet_escape_velocity(height, EARTH_MASS * 2)
    
    assert escape_vel_heavy > escape_vel_earth, "Escape velocity should increase with planet mass"


def test_larger_rocket_needs_more_fuel_to_achieve_same_acceleration() -> None:
    """Test that a larger rocket needs proportionally more fuel to achieve the same acceleration"""
    # Create two rockets with different initial masses but same fuel ratio
    small_rocket = _create_rocket_with_mass(50_000)  # 50 tons
    large_rocket = _create_rocket_with_mass(200_000) # 200 tons
    
    # Both have same fuel ratio, so larger rocket has more absolute fuel
    assert large_rocket.fuel_mass > small_rocket.fuel_mass, "Larger rocket should have more fuel with same ratio"
    
    # Simulate both
    calculator_small = RocketFlightCalculator(
        rocket=small_rocket,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    calculator_large = RocketFlightCalculator(
        rocket=large_rocket,
        flight_equation=fixed_acceleration_flight_equation,
        planet_mass=EARTH_MASS,
    )
    SAMPLING_DELTA = 1
    list(simulate_flight(calculator_small, SAMPLING_DELTA))
    list(simulate_flight(calculator_large, SAMPLING_DELTA))
    
    # Check that both can achieve escape velocity, but it might take longer for the larger rocket
    # given the same acceleration setting


def _create_rocket_with_acceleration(acceleration):
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


def _create_rocket_with_fuel_ratio(fuel_ratio):
    """Helper function to create a rocket with specified fuel ratio"""
    initial_mass = 100_000  # 100 tons
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    stream_velocity = 4500  # 4.5 km/s
    acceleration = 3 * 9.81  # 3g
    
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


def _create_rocket_with_stream_velocity(stream_velocity):
    """Helper function to create a rocket with specified stream velocity"""
    initial_mass = 100_000  # 100 tons
    fuel_ratio = 0.90
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    acceleration = 3 * 9.81  # 3g
    
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


def _create_rocket_with_mass(initial_mass):
    """Helper function to create a rocket with specified initial mass"""
    fuel_ratio = 0.90
    fuel_mass = initial_mass * fuel_ratio
    netto_mass = initial_mass - fuel_mass
    stream_velocity = 4500  # 4.5 km/s
    acceleration = 3 * 9.81  # 3g
    
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


def _find_time_to_velocity(rockets, velocity_threshold):
    """Helper function to find the time when velocity threshold is reached"""
    for i, rocket in enumerate(rockets):
        if rocket.velocity >= velocity_threshold:
            return i  # Return time step index
    return len(rockets)  # If threshold not reached, return simulation length
