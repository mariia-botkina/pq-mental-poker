"""Multiplicative ElGamal encryption over a prime-order subgroup.

Messages are group elements, not arbitrary integers: m is masked by
multiplication, which keeps ciphertexts re-randomisable — a property the
hashed variant does not have and that shuffling will rely on.

Reference: Boneh & Shoup, A Graduate Course in Applied Cryptography,
section 11.5 and exercise 11.5 (multiplicative variant).

Educational implementation. Not constant-time, not audited.
"""

def keygen(G) -> tuple[int, int]:
    """Generate an ElGamal key pair.

    Returns (sk, pk) where sk is a uniform non-zero exponent from Z_q
    and pk = g^sk is the corresponding public key in the subgroup.
    """

    sk = G.random_exponent()
    pk = G.power(G.g, sk)
    
    return sk, pk


def encrypt(pk: int, m: int, G) -> tuple[int, int]:
    """Multiplicative ElGamal.

    Returns (v, c) where v = g^beta is the ephemeral public key
    and c = m * pk^beta is the masked message.
    """

    if not G.in_subgroup(m):
        raise ValueError(f"message {m} must be an element of the order-{G.q} subgroup")
    if not G.in_subgroup(pk):
        raise ValueError(f"public key {pk} must be an element of the order-{G.q} subgroup")

    beta = G.random_exponent()
    v = G.power(G.g, beta)
    c = G.mul(m, G.power(pk, beta))

    return v, c



def decrypt(sk: int, ciphertext: tuple[int, int], G) -> int:
    """Decrypt an ElGamal ciphertext.

    Recovers m = c / v^sk, using the fact that v^sk = g^(beta*sk) = pk^beta 
    is the same mask the sender applied.
    """

    if not G.is_valid_exponent(sk):
        raise ValueError("secret key must not be zero mod q")
    
    v, c = ciphertext

    if not G.in_subgroup(v):
        raise ValueError(f"ephemeral public key {v} must be an element of the order-{G.q} subgroup")
    if not G.in_subgroup(c):
        raise ValueError(f"masked message {c} must be an element of the order-{G.q} subgroup")

    sk = G.normalize_exponent(sk)
    m = G.div(c, G.power(v, sk))

    return m