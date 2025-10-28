import math

import pytest

from labs.model.vector import Vector2D


def test_from_polar_zero() -> None:
    v = Vector2D.from_polar(0, math.pi / 4)
    assert v.x == 0
    assert v.y == 0


@pytest.mark.parametrize(
    ("norm", "angle", "expected"),
    [
        (1, 0, Vector2D(1, 0)),
        (1, math.pi / 2, Vector2D(0, 1)),
        (1, math.pi, Vector2D(-1, 0)),
        (2, math.pi / 4, Vector2D(round(math.sqrt(2), 15), round(math.sqrt(2), 15))),
    ],
)
def test_from_polar(norm: float, angle: float, expected: Vector2D) -> None:
    v = Vector2D.from_polar(norm, angle)
    assert math.isclose(v.x, expected.x, abs_tol=1e-12)
    assert math.isclose(v.y, expected.y, abs_tol=1e-12)


def test_to_polar() -> None:
    v = Vector2D(3, 4)
    norm, angle = v.to_polar()
    assert math.isclose(norm, 5.0)
    assert math.isclose(angle, math.atan2(4, 3))


def test_angle_and_norm_properties() -> None:
    v = Vector2D(0, 1)
    assert math.isclose(v.angle, math.pi / 2)
    assert math.isclose(v.norm, 1.0)


def test_addition() -> None:
    v1 = Vector2D(1, 2)
    v2 = Vector2D(3, 4)
    res = v1 + v2
    assert res == Vector2D(4, 6)


def test_subtraction() -> None:
    v1 = Vector2D(5, 7)
    v2 = Vector2D(2, 3)
    res = v1 - v2
    assert res == Vector2D(3, 4)


def test_scalar_multiplication() -> None:
    v = Vector2D(1, -2)
    res = v * 3
    assert res == Vector2D(3, -6)


def test_rotate_90_deg() -> None:
    v = Vector2D(1, 0)
    rotated = v.rotate(math.pi / 2)
    assert math.isclose(rotated.x, 0, abs_tol=1e-12)
    assert math.isclose(rotated.y, 1, abs_tol=1e-12)


def test_rotate_180_deg() -> None:
    v = Vector2D(1, 0)
    rotated = v.rotate(math.pi)
    assert math.isclose(rotated.x, -1, abs_tol=1e-12)
    assert math.isclose(rotated.y, 0, abs_tol=1e-12)


def test_rotate_preserves_norm() -> None:
    v = Vector2D(3, 4)
    rotated = v.rotate(math.pi / 3)
    assert math.isclose(v.norm, rotated.norm, abs_tol=1e-12)
