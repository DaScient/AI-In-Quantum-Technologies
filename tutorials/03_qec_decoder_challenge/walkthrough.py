"""Tutorial 3 — Quantum Error Correction Decoder Challenge.

Benchmark the built-in minimum-weight decoder on a repetition-code corpus and
provide a baseline logical-error-rate score to beat with a learned decoder.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the top-level ``datasets`` package importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from aiquantum.quantum import decode_repetition_code  # noqa: E402
from datasets import synthetic_syndrome_dataset  # noqa: E402


def logical_error_rate(n_samples: int, n_data: int, error_rate: float, seed: int) -> float:
    """Fraction of shots where the decoder fails to recover the logical bit."""
    batch = synthetic_syndrome_dataset(
        n_samples=n_samples, n_data=n_data, error_rate=error_rate, seed=seed
    )
    failures = 0
    for error, syndrome in zip(batch["errors"], batch["syndromes"], strict=True):
        recovery = decode_repetition_code(syndrome, n_data)
        residual = (error + recovery) % 2
        # Logical failure: the residual flips a majority of data qubits.
        if residual.sum() > n_data // 2:
            failures += 1
    return failures / n_samples


def main() -> None:
    print("Quantum Error Correction Decoder Challenge")
    print("------------------------------------------")
    print(f"{'physical error rate':>22} | {'logical error rate':>18}")
    for p in (0.02, 0.05, 0.10, 0.20):
        ler = logical_error_rate(2000, n_data=3, error_rate=p, seed=0)
        print(f"{p:>22.2f} | {ler:>18.4f}")
    print("\nBaseline: minimum-weight matching decoder.")
    print("Challenge: train a decoder on the (errors, syndromes) arrays and "
          "lower the logical error rate.")


if __name__ == "__main__":
    main()
