"""Shamir's t-out-of-n secret sharing over a prime field.

Reference: Boneh & Shoup, A Graduate Course in Applied Cryptography, section 22.1.
"""

from pqmp.field import Field


def split(secret: int, t: int, n: int, F: Field) -> list[tuple[int, int]]:
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

    for _ in range(t - 1):
        coeff.append(F.random_element())

    # Coefficients are sampled uniformly, so the leading one may be zero
    # with probability 1/q, formally lowering the degree. Negligible for
    # cryptographic q; noted here because the threshold is then t-1.

    shares = []

    for i in range(1, n + 1):
        y = 0
        for k, c in enumerate(coeff):
            y = F.add(y, F.mul(c, F.power(i, k)))
        shares.append((i, y))

    return shares


def lagrange_coefficients(xs: list[int], F: Field) -> dict[int, int]:
    """Lagrange coefficients for interpolation at x = 0.

    Depends only on the evaluation points, not on the values at them —
    which is what makes interpolation in the exponent possible.
    """

    if not xs:
        raise ValueError("no evaluation points provided")
    if len(set(xs)) != len(xs):
        raise ValueError("evaluation points must be distinct")
    if 0 in xs:
        raise ValueError("x = 0 is the interpolation target, not an evaluation point")

    coeffs = {}

    for x_j in xs:
        lam_j = 1
        for x_m in xs:
            if x_j != x_m:
                lam_j = F.mul(
                    lam_j, F.div(F.sub(0, x_m), F.sub(x_j, x_m))
                )  # lambda_j = prod_{m != j} (0 - x_m) / (x_j - x_m)
        coeffs[x_j] = lam_j

    return coeffs


def reconstruct(shares: list[tuple[int, int]], F: Field) -> int:
    """Recover the secret by Lagrange interpolation at x = 0.

    Share indices must be distinct and non-zero; x = 0 is the secret itself.
    """
    secret = 0

    lams = lagrange_coefficients([x for x, _ in shares], F)
    for x_j, y_j in shares:
        secret = F.add(secret, F.mul(lams[x_j], y_j))

    return secret
