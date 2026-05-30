"""Tutorial 5 — Ethical Audit of a Quantum-Enhanced Model.

Audit a quantum-kernel classifier for performance disparity across two cohorts,
operationalising the fairness principles of Chapter 24 as a reproducible metric.
"""

from __future__ import annotations

import numpy as np

from aiquantum.qml import HybridKernelClassifier


def make_cohort(n: int, separation: float, noise: float, rng: np.random.Generator):
    """Return angle features and labels for one cohort.

    ``separation`` controls how distinguishable the two classes are; smaller
    separation models a cohort the training data represents poorly.
    """
    half = n // 2
    pos = separation + noise * rng.standard_normal(half)
    neg = -separation + noise * rng.standard_normal(half)
    x = np.concatenate([pos, neg]).reshape(-1, 1)
    y = np.concatenate([np.ones(half), np.zeros(half)]).astype(int)
    return x, y


def main() -> None:
    rng = np.random.default_rng(0)

    # Train on the well-represented cohort A.
    xa, ya = make_cohort(80, separation=0.8, noise=0.15, rng=rng)
    model = HybridKernelClassifier(regularization=1e-3).fit(xa, ya)

    # Cohort B is under-represented: same task, weaker class separation.
    xb, yb = make_cohort(80, separation=0.3, noise=0.15, rng=rng)

    acc_a = model.score(xa, ya)
    acc_b = model.score(xb, yb)
    gap = abs(acc_a - acc_b)

    print("Ethical Audit of a Quantum-Enhanced Model")
    print("-----------------------------------------")
    print(f"cohort A accuracy: {acc_a:.2f}")
    print(f"cohort B accuracy: {acc_b:.2f}")
    print(f"disparity gap:     {gap:.2f}")
    verdict = "PASS" if gap <= 0.10 else "REVIEW"
    print(f"audit verdict (gap <= 0.10): {verdict}")
    if verdict == "REVIEW":
        print("Large disparity: investigate data representativeness before deployment.")


if __name__ == "__main__":
    main()
