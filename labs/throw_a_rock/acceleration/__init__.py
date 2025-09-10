from labs.model.enum import CorrelationType
from labs.throw_a_rock.acceleration.constant import constant_acceleration_law
from labs.throw_a_rock.acceleration.linear import linear_acceleration_law
from labs.throw_a_rock.acceleration.quadratic import quadratic_acceleration_law
from labs.throw_a_rock.acceleration.variation_law import AccelerationVariationLaw

acceleration_law_by_resistance_type: dict[CorrelationType, AccelerationVariationLaw] = {
    CorrelationType.CONSTANT: constant_acceleration_law,
    CorrelationType.LINEAR: linear_acceleration_law,
    CorrelationType.QUADRATIC: quadratic_acceleration_law,
}
