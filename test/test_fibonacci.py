import pytest
from zrTest.functions import fibonacci as fibonacci_normal
from zrTest.functions import fibonacci_memo as fibonacci_memoized

@pytest.mark.parametrize("n, expected", [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (10, 55),
    (20, 6765),
    (30, 832040),
    (-1, -1)
])

# TODO: BIG NUMBERS

def test_fibonacci_basic(n, expected):
    assert fibonacci_normal(n) == expected
    assert fibonacci_memoized(n) == expected

@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 6, 10, 20, 30])
def test_fibonacci_consistency(n):
    assert fibonacci_normal(n) == fibonacci_memoized(n)