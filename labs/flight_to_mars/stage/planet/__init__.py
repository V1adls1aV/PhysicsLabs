__all__ = ["flight_equations"]

from labs.flight_to_mars.model.flight import FlightEquationType

from .equation import fixed_acceleration_flight_equation, fixed_fuel_rate_flight_equation

flight_equations = {
    FlightEquationType.FIXED_FUEL_RATE: fixed_fuel_rate_flight_equation,
    FlightEquationType.FIXED_ACCELERATION: fixed_acceleration_flight_equation,
}
