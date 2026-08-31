import pytest

from pqmp.group import Group
from pqmp.elgamal import keygen, encrypt, decrypt


@pytest.fixture
def G():
    return Group(23, 11, 2)


@pytest.fixture
def keys(G):
    return keygen(G)


def test_decrypt_inverts_encrypt(G, keys):
    sk, pk = keys
    for _ in range(100):
        m = G.random_subgroup_element()
        assert decrypt(sk, encrypt(pk, m, G), G) == m


def test_encryption_is_randomised(G, keys):
    _, pk = keys
    m = G.random_subgroup_element()
    ciphertexts = {encrypt(pk, m, G) for _ in range(50)}
    assert len(ciphertexts) > 1


def test_ciphertext_components_are_in_subgroup(G, keys):
    _, pk = keys
    for _ in range(100):
        m = G.random_subgroup_element()
        v, c = encrypt(pk, m, G)
        assert G.in_subgroup(v), f"v={v} must be in subgroup"
        assert G.in_subgroup(c), f"c={c} must be in subgroup"


def test_encrypt_rejects_message_outside_subgroup(G, keys):
    _, pk = keys
    with pytest.raises(ValueError):
        encrypt(pk, 5, G)


def test_decrypt_rejects_zero_secret_key(G, keys):
    _, pk = keys
    m = G.random_subgroup_element()
    ct = encrypt(pk, m, G)

    with pytest.raises(ValueError):
        decrypt(0, ct, G)
    with pytest.raises(ValueError):
        decrypt(G.q, ct, G)


def test_decrypt_rejects_ciphertext_outside_subgroup(G, keys):
    sk, pk = keys
    m = G.random_subgroup_element()
    v, c = encrypt(pk, m, G)

    with pytest.raises(ValueError):
        decrypt(sk, (5, c), G)
    with pytest.raises(ValueError):
        decrypt(sk, (v, 5), G)
