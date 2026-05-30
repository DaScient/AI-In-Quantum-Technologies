"""Tutorial 2 — Designing a Superconducting Qubit with AI.

Screen candidate superconductors by critical temperature, then synthesise a
high-fidelity gate pulse for the chosen qubit with GRAPE.
"""

from __future__ import annotations

from aiquantum.linalg import X
from aiquantum.materials import allen_dynes_tc
from aiquantum.quantum import grape_pulse


def main() -> None:
    # Candidate electron-phonon parameter sets (lambda, omega_log [K], mu*).
    candidates = {
        "candidate-A": (0.6, 350.0, 0.10),
        "candidate-B": (0.9, 420.0, 0.10),
        "candidate-C": (1.2, 500.0, 0.13),
    }

    print("Designing a Superconducting Qubit with AI")
    print("-----------------------------------------")
    ranked = sorted(
        candidates.items(),
        key=lambda kv: allen_dynes_tc(*kv[1]),
        reverse=True,
    )
    for name, params in ranked:
        tc = allen_dynes_tc(*params)
        print(f"  {name}: T_c = {tc:6.1f} K")

    best_name = ranked[0][0]
    print(f"\nSelected host material: {best_name}")

    # Synthesise an X gate for the selected qubit.
    result = grape_pulse(X, n_steps=20, dt=0.2, iterations=400, seed=1)
    print(f"GRAPE X-gate fidelity: {result.fidelity:.4f}")
    print(f"Pulse shape: {result.controls.shape[0]} steps x "
          f"{result.controls.shape[1]} controls")


if __name__ == "__main__":
    main()
