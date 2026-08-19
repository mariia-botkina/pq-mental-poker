from pqmp.field import Field

def split(secret:int, t:int, n:int, F:Field) -> list[tuple[int, int]]:
    if n >= F.modulus:
        raise ValueError(f"n={n} must be less than modulus {F.modulus}")

    if t > n:
        raise ValueError("t={t} cannot exceed n={n}")
    
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
    secret = 0

    for x_j, _ in shares:
        lam = 1
        for x_m, y_m in shares:
            if x_m != x_j:
                lam = F.mul(lam, F.div(F.sub(0, x_m), F.sub(x_j, x_m)))
            else:
                lam = F.mul(lam, y_m)
        secret = F.add(secret, lam)

    return secret
