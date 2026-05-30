"""Tutorial 4 — Certified Quantum Randomness.

Use the BB84 secret-key-rate analysis as a proxy for device-independent
randomness certification: sweep the quantum bit-error rate and locate the abort
threshold beyond which no randomness can be certified.
"""

from __future__ import annotations

from aiquantum.crypto import bb84_key_rate


def main() -> None:
    print("Certified Quantum Randomness")
    print("----------------------------")
    print(f"{'QBER':>6} | {'certified bits/use':>18}")

    threshold = None
    for i in range(0, 21):
        qber = i / 100.0
        rate = bb84_key_rate(qber)
        print(f"{qber:>6.2f} | {rate:>18.4f}")
        if threshold is None and rate <= 0.0 and qber > 0.0:
            threshold = qber

    if threshold is not None:
        print(f"\nAbort threshold: certified randomness vanishes at QBER >= {threshold:.2f}.")
    print("Below threshold, each channel use yields the printed certified-random bits.")


if __name__ == "__main__":
    main()
