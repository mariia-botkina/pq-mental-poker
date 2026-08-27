import pytest

from pqmp.field import Field


@pytest.fixture
def F():
    return Field(7919)


def test_mul_by_inverse_gives_one(F):
    for _ in range(100):
        a = F.random_nonzero()
        assert F.mul(a, F.inv(a)) == 1, f"failed for a={a}"


def test_div_then_mul_returns_original(F):
    for _ in range(100):
        a = F.random_element()
        b = F.random_nonzero()
        assert F.mul(F.div(a, b), b) == a, f"failed for a={a}, b={b}"


def test_inv_of_zero_raises(F):
    with pytest.raises(ZeroDivisionError):
        F.inv(0)


def test_inv_of_modulus_raises(F):
    with pytest.raises(ZeroDivisionError):
        F.inv(F.modulus)


def test_mul_distributes_over_add(F):
    for _ in range(100):
        a = F.random_element()
        b = F.random_element()
        c = F.random_element()
        assert F.mul(a, F.add(b, c)) == F.add(F.mul(a, b), F.mul(a, c)), (
            f"failed for a={a}, b={b}, c={c}"
        )


def test_random_nonzero_never_returns_zero(F):
    for _ in range(1000):
        assert F.random_nonzero() != 0
