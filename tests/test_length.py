from math import sqrt

import pytest  # type: ignore
from hypothesis import given

from ppb_vector import Vector
from utils import isclose, vectors


@pytest.mark.parametrize(
    "x, y, expected",
    [(6,   8, 10),
     (8,   6, 10),
     (0,   0, 0),
     (-6, -8, 10),
     (1,   2, 2.23606797749979)],
)
def test_length(x, y, expected):
    vector = Vector(x, y)
    assert vector.length == expected


@given(v=vectors())
def test_length_dot(v: Vector):
    """Test that |v| ≃ √v²."""
    assert isclose(v.length, sqrt(v * v))
