# Tutorial 4 — Certified Quantum Randomness

**Chapter:** 13 (Quantum Cryptography and Security)

Randomness you can *trust* must be certified by physics, not asserted by a vendor.
This path uses the BB84 secret-key-rate analysis as a proxy for device-independent
certification: it estimates how certified-random bits per channel use survive
a given quantum bit-error rate, and where the protocol aborts.

## What you will learn

- How the BB84 asymptotic key rate depends on the quantum bit-error rate (QBER).
- Why there is a threshold QBER above which no secret randomness can be certified.
- How certification budgets shrink as channel noise grows (Chapter 13).

## Run it

```bash
python tutorials/04_certified_quantum_randomness/walkthrough.py
```

The script sweeps the QBER, prints the certified secret-key rate, and reports the
abort threshold beyond which the certified-randomness rate falls to zero.
