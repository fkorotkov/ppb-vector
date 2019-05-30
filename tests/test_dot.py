from math import sqrt

from hypothesis import assume, given, note

from ppb_vector import Vector
from utils import angles, floats, isclose, vector_likes, vectors


@given(vector=vectors())
def test_dot_axis(vector: Vector):
    assert vector * (1, 0) == vector.x
    assert vector * (0, 1) == vector.y


@given(x=vectors(), y=vectors())
def test_dot_commutes(x: Vector, y: Vector):
    assert x * y == y * x


@given(x=vectors())
def test_dot_length(x: Vector):
    assert isclose(x * x, x.length * x.length)


@given(x=vectors(), y=vectors())
def test_cauchy_schwarz(x: Vector, y: Vector):
    """Test the Cauchy-Schwarz inequality: |x·y| ⩽ |x| |y|"""
    assert abs(x * y) <= (1 + 1e-12) * x.length * y.length


@given(x=vectors(), y=vectors(), angle=angles())
def test_dot_rotational_invariance(x: Vector, y: Vector, angle: float):
    """Test that rotating vectors doesn't change their dot product."""
    t = x.angle(y)
    cos_t, _ = Vector._trig(t)
    note(f"θ: {t}")
    note(f"cos θ: {cos_t}")

    # Exclude near-orthogonal test inputs
    assume(abs(cos_t) > 1e-6)
    assert isclose(x * y, x.rotate(angle) * y.rotate(angle), rel_to=(x, y), rel_exp=2)


MAGNITUDE = 1e10


@given(
    x=vectors(max_magnitude=MAGNITUDE),
    z=vectors(max_magnitude=MAGNITUDE),
    y=vectors(max_magnitude=sqrt(MAGNITUDE)),
    scalar=floats(max_magnitude=sqrt(MAGNITUDE)),
)
def test_dot_linear(x: Vector, y: Vector, z: Vector, scalar: float):
    """Test that x · (λ y + z) = λ x·y + x·z"""
    inner, outer = x * (scalar * y + z), scalar * x * y + x * z
    note(f"inner: {inner}")
    note(f"outer: {outer}")
    assert isclose(inner, outer, rel_to=(x, scalar, y, z), rel_exp=2)


@given(x=vectors(max_magnitude=1e7), y=vectors(max_magnitude=1e7))
def test_dot_from_angle(x: Vector, y: Vector):
    """Test x · y == |x| · |y| · cos(θ)"""
    t = x.angle(y)
    cos_t, _ = Vector._trig(t)

    # Dismiss near-othogonal test inputs
    assume(abs(cos_t) > 1e-6)

    min_len, max_len = sorted((x.length, y.length))
    geometric = min_len * (max_len * cos_t)

    note(f"θ: {t}")
    note(f"cos θ: {cos_t}")
    note(f"algebraic: {x * y}")
    note(f"geometric: {geometric}")
    assert isclose(x * y, geometric, rel_to=(x, y), rel_exp=2)


@given(x=vectors(), y=vectors())
def test_dot_rmul(x: Vector, y: Vector):
    for x_like in vector_likes(x):
        assert x_like * y == x * y
