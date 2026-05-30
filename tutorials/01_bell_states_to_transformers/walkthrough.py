"""Tutorial 1 — From Bell States to Transformers.

Classify single-qubit states by encoding their Bloch-vector features with a
quantum kernel. Runs offline using only the core ``aiquantum`` library.
"""

from __future__ import annotations

import numpy as np

from aiquantum.qml import HybridKernelClassifier
from aiquantum.quantum import linear_inversion_tomography


def bloch_feature(expectations: dict[str, float]) -> np.ndarray:
    """Reconstruct a single-qubit state and return its Bloch vector."""
    rho = linear_inversion_tomography(expectations, n_qubits=1, project=True)
    x = 2.0 * rho[0, 1].real
    y = -2.0 * rho[0, 1].imag
    z = (rho[0, 0] - rho[1, 1]).real
    return np.array([x, y, z])


def main() -> None:
    rng = np.random.default_rng(0)

    # Two classes of states: clustered near +Z and near -Z, with noise.
    samples, labels = [], []
    for _ in range(30):
        z = 0.8 + 0.1 * rng.standard_normal()
        samples.append(bloch_feature({"Z": float(np.clip(z, -1, 1))}))
        labels.append(1)
        z = -0.8 + 0.1 * rng.standard_normal()
        samples.append(bloch_feature({"Z": float(np.clip(z, -1, 1))}))
        labels.append(0)

    x = np.array(samples)
    y = np.array(labels)

    # Encode the polar angle as a single feature for the quantum kernel.
    angles = np.arccos(np.clip(x[:, 2], -1.0, 1.0)).reshape(-1, 1) / 2.0
    model = HybridKernelClassifier(regularization=1e-3).fit(angles, y)
    accuracy = model.score(angles, y)

    print("From Bell States to Transformers")
    print("--------------------------------")
    print(f"samples: {len(y)}  features: {angles.shape[1]}")
    print(f"quantum-kernel training accuracy: {accuracy:.2f}")
    print("The two state families are separable in the quantum feature space.")


if __name__ == "__main__":
    main()
