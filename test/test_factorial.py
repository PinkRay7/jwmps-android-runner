import pytest
from zrTest.functions import factorial, factorial_memo

@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800)
])

def test_factorial_zero(n, expected):
    assert factorial(n) == expected
    assert factorial_memo(n) == expected