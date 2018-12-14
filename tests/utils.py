from ppb_vector import Vector2
import hypothesis.strategies as st


def vectors(max_magnitude=1e300):
    return st.builds(Vector2,
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude),
                     st.floats(min_value=-max_magnitude, max_value=max_magnitude)
    )

@st.composite
def units(draw, elements=st.floats(min_value=0, max_value=360)):
    angle = draw(elements)
    return Vector2(1, 0).rotate(angle)


def angle_isclose(x, y, epsilon = 6.5e-5):
    d = (x - y) % 360
    return (d < epsilon) or (d > 360 - epsilon)


# List of operations that (Vector2, Vector2) -> Vector2
BINARY_OPS = [
    Vector2.__add__,
    Vector2.__sub__,
    Vector2.reflect,
]

# List of operations that (Vector2, Real) -> Vector2
SCALAR_OPS = [
    Vector2.scale_by,
    Vector2.rotate,
    Vector2.truncate,
    Vector2.scale_to,
]

# List of operations that (Vector2) -> Vector2
UNARY_OPS = [
    lambda v: type(v).convert(v),
    Vector2.__neg__,
    Vector2.normalize,
]
