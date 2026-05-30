"""Hybrid quantum-classical training with a kernel-ridge classifier.

The classifier solves a regularised least-squares problem in the quantum-kernel
feature space and thresholds the decision function for binary labels. It mirrors
the support-vector workflow of the textbook while remaining dependency-light.
"""

from __future__ import annotations

import numpy as np

from .kernel import quantum_kernel_matrix


class HybridKernelClassifier:
    """Binary classifier built on a precomputed quantum kernel."""

    def __init__(self, regularization: float = 1e-3) -> None:
        self.regularization = float(regularization)
        self._x_train: np.ndarray | None = None
        self._dual: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> HybridKernelClassifier:
        """Fit on samples ``x`` with labels ``y`` in ``{-1, +1}`` or ``{0, 1}``."""
        x = np.atleast_2d(np.asarray(x, dtype=float))
        y = np.asarray(y, dtype=float)
        y = np.where(y <= 0, -1.0, 1.0)
        kernel = quantum_kernel_matrix(x)
        kernel += self.regularization * np.eye(kernel.shape[0])
        self._dual = np.linalg.solve(kernel, y)
        self._x_train = x
        return self

    def decision_function(self, x: np.ndarray) -> np.ndarray:
        """Return the real-valued decision score for each sample."""
        if self._x_train is None or self._dual is None:
            raise RuntimeError("Classifier must be fitted before prediction.")
        x = np.atleast_2d(np.asarray(x, dtype=float))
        kernel = quantum_kernel_matrix(x, self._x_train)
        return kernel @ self._dual

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Return predicted labels in ``{-1, +1}``."""
        return np.sign(self.decision_function(x))

    def score(self, x: np.ndarray, y: np.ndarray) -> float:
        """Return classification accuracy in ``[0, 1]``."""
        y = np.where(np.asarray(y, dtype=float) <= 0, -1.0, 1.0)
        return float(np.mean(self.predict(x) == y))


def train_hybrid_model(
    x: np.ndarray,
    y: np.ndarray,
    regularization: float = 1e-3,
) -> dict[str, object]:
    """Train a :class:`HybridKernelClassifier` and report training metrics.

    Returns a JSON-serialisable summary suitable for the ``/qml/train`` endpoint.
    """
    model = HybridKernelClassifier(regularization=regularization).fit(x, y)
    accuracy = model.score(x, y)
    return {
        "n_samples": int(np.atleast_2d(x).shape[0]),
        "n_features": int(np.atleast_2d(x).shape[1]),
        "regularization": regularization,
        "train_accuracy": accuracy,
        "model": model,
    }
