from pqmp.field import Field

class Group:
    """Prime-order subgroup of Z_p^* for discrete-log based schemes.

    The group is the order-q subgroup of Z_p^* where p = 2q + 1 (safe prime).
    Group elements live mod p (Fp); exponents live mod q (Fq).

    Educational implementation. Not constant-time, not audited.
    """

    identity = 1

    def __init__(self, p:int, q:int, g:int, check=True):
        self.p = p
        self.q = q
        self.g = g

        self.Fp = Field(p, check=check)
        self.Fq = Field(q, check=check)

        if 2 * q + 1 != p:
            raise ValueError(f"p={p} not equal to 2 * q + 1 for q={q}")
        if g == 1:
            raise ValueError('g must not equal 1')
        if pow(g, q, p) != 1: # g^q = 1 iff g is in the order-q subgroup
            raise ValueError(f"g={g} does not generate the subgroup of order {q}")

    def mul(self, a:int, b:int) -> int:
        return self.Fp.mul(a, b)

    def div(self, a:int, b:int) -> int:
        return self.Fp.div(a, b)

    def power(self, base, exponent) -> int:
        return self.Fp.power(base, exponent)

    def inv(self, a) -> int:
        return self.Fp.inv(a)

    def random_exponent(self) -> int:
        """Uniform non-zero exponent from Z_q."""
        return self.Fq.random_nonzero()

    def random_subgroup_element(self) -> int:
        return self.power(self.g, self.random_exponent())

    def is_element(self, x:int) -> bool:
        """x is a valid element of Z_p^* (but not necessarily of the subgroup)."""
        return 1 <= x < self.p

    def in_subgroup(self, x:int) -> bool:
        """x lies in the order-q subgroup: true iff x^q = 1."""
        return self.is_element(x) and self.power(x, self.q) == 1

    def __repr__(self) -> str:
        if self.p.bit_length() <= 32:
            return f"<Group p={self.p}, q={self.q}, g={self.g}>"
        return f"<Group p={self.p.bit_length()} bits, q={self.q.bit_length()} bits>"

    def __eq__(self, other) -> bool:
        return isinstance(other, Group) and (self.p, self.q, self.g) == (other.p, other.q, other.g)

    def __hash__(self) -> int:
        return hash((self.p, self.q, self.g))
    