from pqmp.shamir import split, lagrange_coefficients
from pqmp.group import Group

def distribute_key(t: int, n: int, G: Group) -> tuple[int, list[tuple[int, int]]]:
    """Generate a threshold key pair.

    Returns (pk, shares) where pk = g^sk is the shared public key and shares
    are a t-out-of-n Shamir sharing of sk over Z_q. The full sk exists only
    inside this function; see section 22.4 for distributed key generation
    that never assembles it at all.
    """

    sk = G.random_exponent()
    pk = G.power(G.g, sk)
    shares = split(sk, t, n, G.Fq)

    return pk, shares


def partial_decrypt(share: tuple[int, int], v: int, G: Group) -> tuple[int, int]: 
    """Compute this party's decryption share.

    Takes (i, sk_i) — one Shamir share of the secret key — and v, the
    ephemeral public key from the ciphertext. Returns (i, v^sk_i); the
    index travels with the value because the combiner needs it to compute
    the Lagrange coefficients.

    The second ciphertext component c is not needed here: a party can
    contribute to decryption without seeing what is being decrypted.
    """

    if not G.in_subgroup(v):
        raise ValueError(f"{v} must be an element of the order-{G.q} subgroup")

    i, sk_i = share

    if i == 0:
        raise ValueError("share index 0 is the secret key itself, not a share")


    return i, G.power(v, sk_i)
    


def combine(partials: list[tuple[int, int]], c: int, G: Group) -> int:
    """Reconstruct the plaintext from t decryption shares.

    Interpolation in the exponent: the Lagrange coefficients are computed
    in Z_q and applied to group elements as exponents, giving
    w = prod_j w_j^lam_j = v^sk without any party revealing its share.
    """

    lams = lagrange_coefficients([i for i, _ in partials], G.Fq)
    w = G.identity
    for j, w_j in partials:
        w = G.mul(w, G.power(w_j, lams[j]))

    return G.div(c, w)
