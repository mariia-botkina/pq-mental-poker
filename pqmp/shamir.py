"""Shamir's t-out-of-n secret sharing over a prime field.

Reference: Boneh & Shoup, A Graduate Course in Applied Cryptography, section 22.1.
"""

from pqmp.field import Field


def split(secret:int, t:int, n:int, F:Field) -> list[tuple[int, int]]:
    """Split a secret into n shares, any t of which reconstruct it.

    Builds a random polynomial of degree t-1 with the secret as its
    constant term, and evaluates it at x = 1..n.
    """
        
    if n >= F.modulus:
        raise ValueError(f"n={n} must be less than modulus {F.modulus}")

    if t > n:
        raise ValueError(f"t={t} cannot exceed n={n}")
    
    secret = secret % F.modulus

    coeff = [secret]

    for _ in range(t-1):
        coeff.append(F.random_element())

    shares = []

    for i in range(1, n + 1):
        y = 0
        for k, c in enumerate(coeff):
            y = F.add(y, F.mul(c, F.power(i, k)))
        shares.append((i, y))

    return shares


def reconstruct(shares:list[tuple[int, int]], F:Field) -> int:
    """Recover the secret by Lagrange interpolation at x = 0.

    Share indices must be distinct and non-zero; x = 0 is the secret itself.
    """
        
    xs = [x for x, _ in shares]
    if len(set(xs)) != len(xs):
        raise ValueError("share indices must be distinct")
    if 0 in xs:
        raise ValueError("share index 0 is not a valid share: omega(0) is the secret itself")
    if not xs:
        raise ValueError("no shares provided") 

    secret = 0

    for x_j, _ in shares:
        lam = 1
        for x_m, y_m in shares:
            if x_m != x_j:
                lam = F.mul(lam, F.div(F.sub(0, x_m), F.sub(x_j, x_m))) # lambda_j = prod_{m != j} (0 - x_m) / (x_j - x_m)
            else:
                lam = F.mul(lam, y_m)
        secret = F.add(secret, lam)

    return secret
