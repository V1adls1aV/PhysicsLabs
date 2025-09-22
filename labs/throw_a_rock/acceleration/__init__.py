__all__ = ["AccelerationVariationLaw", "acceleration_law_by_resistance_type"]

from labs.model.enum import CorrelationType

from .linear import linear_acceleration_law
from .quadratic import quadratic_acceleration_law
from .variation_law import AccelerationVariationLaw

acceleration_law_by_resistance_type: dict[CorrelationType, AccelerationVariationLaw] = {
    CorrelationType.LINEAR: linear_acceleration_law,
    CorrelationType.QUADRATIC: quadratic_acceleration_law,
}
