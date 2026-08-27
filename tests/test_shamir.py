import pytest

from pqmp.field import Field
from pqmp.shamir import reconstruct, split


@pytest.fixture
def F():
    return Field(7919)


def test_t_shares_reconstruct_the_secret(F):
    assert reconstruct(split(42, t=3, n=5, F=F)[:3], F) == 42


def test_any_t_shares_reconstruct_the_secret(F):
    assert reconstruct(split(42, t=3, n=5, F=F)[2:], F) == 42


def test_fewer_than_t_shares_do_not_reconstruct(F):
    for _ in range(10):
        assert reconstruct(split(42, t=3, n=5, F=F)[:2], F) != 42, "collision happened"


def test_threshold_equal_to_n_works(F):
    assert reconstruct(split(42, t=5, n=5, F=F), F) == 42, "reconstruction failed"


def test_split_returns_n_shares_indexed_from_one(F):
    shares = split(42, t=3, n=5, F=F)
    assert len(shares) == 5, "less share than expected"
    assert [x for x, _ in shares] == [1, 2, 3, 4, 5], "wrong numeration"


def test_duplicate_share_indices_raise(F):
    with pytest.raises(ValueError):
        reconstruct([(1, 5), (1, 9), (3, 4)], F)


def test_share_at_index_zero_raises(F):
    with pytest.raises(ValueError):
        reconstruct([(0, 42), (1, 5), (2, 9)], F)


def test_empty_shares_raise(F):
    with pytest.raises(ValueError):
        reconstruct([], F)


def test_split_raises_when_t_exceeds_n(F):
    with pytest.raises(ValueError):
        split(42, t=6, n=5, F=F)


def test_split_raises_when_n_reaches_modulus(F):
    with pytest.raises(ValueError):
        split(42, t=5, n=F.modulus, F=F)
