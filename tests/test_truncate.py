from typing import Type, Union

from hypothesis import assume, event, example, given, note

from ppb_vector import Vector
from utils import floats, lengths, vectors


@given(x=vectors(), max_length=lengths())
def test_truncate_length(x: Vector, max_length: float):
    assert x.truncate(max_length).length <= (1 + 1e-14) * max_length


@given(x=vectors(), max_length=lengths(max_value=1e150))
def test_truncate_invariant(x: Vector, max_length: float):
    assume(x.length <= max_length)
    assert x.truncate(max_length) == x


@given(x=vectors(max_magnitude=1e150), max_length=floats())
@example(  # Large example where x.length == max_length but 1 * x != x
    x=Vector(0.0, 7.1e62), max_length=7.1e62,
)
def test_truncate_equivalent_to_scale(x: Vector, max_length: float):
    """Vector.scale_to and truncate are equivalent when max_length <= x.length"""
    assume(max_length <= x.length)
    note(f"x.length = {x.length}")
    if max_length > 0:
        note(f"x.length = {x.length / max_length} * max_length")

    scale: Union[Vector, Type[Exception]]
    truncate: Union[Vector, Type[Exception]]

    try:
        truncate = x.truncate(max_length)
    except Exception as e:
        truncate = type(e)

    try:
        scale = x.scale_to(max_length)
    except Exception as e:
        event(f"Exception {type(e).__name__} thrown")
        scale = type(e)

    if isinstance(scale, Vector) and x.length == max_length:
        # Permit some edge-case where truncation and scaling aren't equivalent
        assert isinstance(truncate, Vector)
        assert scale.isclose(truncate, abs_tol=0, rel_tol=1e-12)

    else:
        assert scale == truncate
