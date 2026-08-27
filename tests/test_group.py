import pytest

from pqmp.group import Group


@pytest.fixture
def G():
    return Group(23, 11, 2)


def test_generator_is_in_subgroup(G):
    assert G.in_subgroup(G.g)


def test_identity_is_in_subgroup(G):
    assert G.in_subgroup(G.identity)


def test_zero_is_not_an_element(G):
    assert not G.is_element(0)


def test_modulus_is_not_an_element(G):
    assert not G.is_element(G.p)


def test_element_outside_subgroup_is_still_a_group_element(G):
    element = 5
    assert G.is_element(element)
    assert not G.in_subgroup(element)


def test_random_subgroup_element_is_in_subgroup(G):
    for _ in range(100):
        assert G.in_subgroup(G.random_subgroup_element())


def test_subgroup_is_closed_under_multiplication(G):
    for _ in range(100):
        assert G.in_subgroup(
            G.mul(G.random_subgroup_element(), G.random_subgroup_element())
        )


def test_inverse_is_in_subgroup_and_cancels(G):
    for _ in range(100):
        x = G.random_subgroup_element()
        assert G.in_subgroup(G.inv(x))
        assert G.mul(x, G.inv(x)) == G.identity


def test_generator_has_order_q(G):
    for k in range(1, G.q):
        assert G.power(G.g, k) != 1, f"g^k = 1 for k={k}, order is not q"
    assert G.power(G.g, G.q) == 1


def test_raises_when_p_is_not_2q_plus_1():
    with pytest.raises(ValueError):
        Group(25, 11, 2)


def test_raises_when_g_is_identity():
    with pytest.raises(ValueError):
        Group(23, 11, 1)


def test_raises_when_g_not_in_subgroup():
    with pytest.raises(ValueError):
        Group(23, 11, 5)


def test_raises_when_parameters_are_not_prime():
    with pytest.raises(ValueError):
        Group(9, 4, 2)
