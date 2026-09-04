import pytest
import secrets

from pqmp.group import Group
from pqmp.threshold import distribute_key, partial_decrypt, combine
from pqmp.elgamal import encrypt

rng = secrets.SystemRandom()
t, n = 3, 5


@pytest.fixture
def G():
    return Group(23, 11, 2)

@pytest.fixture
def setup(G):
    return distribute_key(t, n, G)

def test_any_t_partials_recover_the_message(G, setup):
    pk, shares = setup
    m = G.random_subgroup_element()  
    v, c = encrypt(pk, m, G)

    for _ in range(100):
        chosen = rng.sample(shares, t)
        partials = [partial_decrypt(share, v, G) for share in chosen]
        m2 = combine(partials, c, G)
        assert m == m2


def test_fewer_than_t_partials_do_not_recover(G):
    results = []

    for _ in range(100):
        pk, shares = distribute_key(t, n, G)
        m = G.random_subgroup_element()  
        v, c = encrypt(pk, m, G)
        chosen = rng.sample(shares, t-1)
        partials = [partial_decrypt(share, v, G) for share in chosen]
        results.append(combine(partials, c, G) == m)

    assert not all(results)

def test_all_n_partials_recover_the_message(G):
    results = []
    
    for _ in range(100):
        pk, shares = distribute_key(t, n, G)
        m = G.random_subgroup_element()  
        v, c = encrypt(pk, m, G)
        chosen = rng.sample(shares, n)
        partials = [partial_decrypt(share, v, G) for share in chosen]
        results.append(combine(partials, c, G) == m)
    
    assert all(results)
    

def test_decryption_share_is_in_subgroup(G, setup):
    pk, shares = setup
    m = G.random_subgroup_element()  
    v, _ = encrypt(pk, m, G)
    for share in shares:
        _, w_i = partial_decrypt(share, v, G)
        assert G.in_subgroup(w_i)

def test_partial_decrypt_rejects_v_outside_subgroup(G, setup):
    _, shares = setup
    for share in shares:
        with pytest.raises(ValueError):
            partial_decrypt(share, 5, G)

def test_combine_rejects_duplicate_indices(G, setup):
    pk, shares = setup
    m = G.random_subgroup_element()  
    v, c = encrypt(pk, m, G)

    p1 = partial_decrypt(shares[0], v, G)
    p2 = partial_decrypt(shares[1], v, G)

    with pytest.raises(ValueError):
        combine([p1, p1, p2], c, G)
