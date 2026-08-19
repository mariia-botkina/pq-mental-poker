import secrets
from sympy import isprime

class Field:
    """Modular arithmetic over a prime field.

    Educational implementation. Not constant-time, not audited.
    """

    def __init__(self, modulus:int, name=None, check=True):
        if check and not isprime(modulus):
            raise ValueError(f"modulus {modulus} is not prime")
        self.modulus = modulus
        self.name = name or f"F_{modulus}"

    def add(self, a:int, b:int) -> int: 
        return (a + b) % self.modulus

    def sub(self, a:int, b:int) -> int:
        return (a - b) % self.modulus

    def mul(self, a:int, b:int) -> int:
        return (a * b) % self.modulus

    def inv(self, a:int) -> int:
        a %= self.modulus
        if a == 0:
            raise ZeroDivisionError(f"no inverse of 0 modulo {self.modulus}")
        return pow(a, -1, self.modulus)

    def div(self, a:int, b:int) -> int:
        return self.mul(a, self.inv(b))

    def power(self, a:int, exponent:int) -> int:
        if exponent < 0:
            return self.inv(self.power(a, -exponent))
        return pow(a, exponent, self.modulus)

    def random_element(self) -> int:
        return secrets.randbelow(self.modulus)

    def random_nonzero(self) -> int:
        return secrets.randbelow(self.modulus - 1) + 1

    def __repr__(self) -> str:
        return f"<Field {self.name}, {self.modulus.bit_length()} bits>"

    def __eq__(self, other:Field) -> bool:
        return isinstance(other, Field) and self.modulus == other.modulus





    