# pq-mental-poker

Educational implementations of cryptographic primitives for a post-quantum
mental poker protocol. 

**Not constant-time, not audited, not for production use.**

## What's here

- `pqmp/field.py` — modular arithmetic over a prime field: addition,
  multiplication, inversion, exponentiation, uniform random sampling.
- `pqmp/shamir.py` — Shamir's t-out-of-n secret sharing: polynomial
  share generation and Lagrange reconstruction at x = 0.

## Running the tests

```bash
pip install -r requirements.txt
pytest -v
```

## Design notes

Randomness is generated in exactly one place (`Field.random_element`,
backed by `secrets`) so that no other module can reach for a weak
generator by accident.

`reconstruct` rejects duplicate share indices explicitly rather than
letting them fail inside modular inversion — duplicates otherwise
produce a silently incorrect secret rather than an error.

## Roadmap

ElGamal and threshold decryption, Pedersen commitments and Sigma
protocols, verifiable re-encryption shuffles, and lattice-based
(LWE) constructions.

## References

- A. Shamir. How to Share a Secret. CACM 22(11), 1979.
- D. Boneh, V. Shoup. A Graduate Course in Applied Cryptography, §22.1.