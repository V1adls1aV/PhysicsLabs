import math
from dataclasses import dataclass

from labs.roll_the_ball.model import Ball, Environment


@dataclass
class PlainInput:
    environment: Environment
    ball: Ball


EPS = 3e-2

HIGH_INCLINE_LENGTH = 100
MEDIUM_INCLINE_LENGTH = 50
SHORT_INCLINE_LENGTH = 10

PLAIN_INPUT = [
    PlainInput(
        Environment(
            incline_angle=math.radians(30),
            friction_coefficient=0.7,
            plane_length=SHORT_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.11, translational_velocity=4.0, angular_velocity=0),
    ),
    PlainInput(
        Environment(
            incline_angle=math.radians(25),
            friction_coefficient=0.43,
            plane_length=SHORT_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.26, translational_velocity=3.1, angular_velocity=0),
    ),
    PlainInput(
        Environment(
            incline_angle=math.radians(22.5),
            friction_coefficient=0.53,
            plane_length=SHORT_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.175, translational_velocity=6.0, angular_velocity=0),
    ),
]


SLIPPING_INPUT = [
    PlainInput(  # should be lower than $\mu = 2/7 tg(10deg) = 0.05$
        Environment(
            incline_angle=math.radians(10),
            friction_coefficient=0.03,
            plane_length=HIGH_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.11, translational_velocity=1, angular_velocity=0),
    ),
    PlainInput(  # k=0, v=1
        Environment(
            incline_angle=math.radians(30),
            friction_coefficient=0.0,
            plane_length=HIGH_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.15, translational_velocity=1, angular_velocity=0),
    ),
    PlainInput(  # k=0, v=0
        Environment(
            incline_angle=math.radians(30),
            friction_coefficient=0.0,
            plane_length=HIGH_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.15, translational_velocity=0, angular_velocity=0),
    ),
]

# There are oposite cases to the slipping input
NON_FULLY_SLIPPING_INPUT = [
    PlainInput(
        Environment(
            incline_angle=math.radians(10),
            friction_coefficient=0.15,
            plane_length=SHORT_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.11, translational_velocity=1, angular_velocity=0),
    ),
]

GRIPPING_INPUT = [
    PlainInput(
        Environment(
            incline_angle=math.radians(10),
            friction_coefficient=0.7,
            plane_length=MEDIUM_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.11, translational_velocity=0, angular_velocity=0),
    ),
    PlainInput(
        Environment(
            incline_angle=math.radians(40),
            friction_coefficient=0.8,
            plane_length=MEDIUM_INCLINE_LENGTH,
        ),
        Ball(mass=1, radius=0.11, translational_velocity=0, angular_velocity=0),
    ),
    PlainInput(
        Environment(
            incline_angle=math.radians(60),
            friction_coefficient=2.3,
            plane_length=MEDIUM_INCLINE_LENGTH,
        ),
        Ball(mass=3, radius=0.51, translational_velocity=0, angular_velocity=0),
    ),
]
