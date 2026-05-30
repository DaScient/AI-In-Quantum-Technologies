"""Ground-state energy prediction with descriptor-based kernel ridge regression.

The Coulomb matrix of Rupp et al. (*Phys. Rev. Lett.* **108**, 058301, 2012) is
a classic permutation-sensitive molecular descriptor. Sorting its eigenvalues
yields a fixed-length, rotation- and permutation-invariant fingerprint that maps
well onto atomisation energies with a Gaussian-kernel ridge regressor — the
baseline against which the textbook benchmarks ``MolQNet``.
"""

from __future__ import annotations

import numpy as np


def coulomb_matrix(charges: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    """Return the Coulomb matrix for a molecule.

    Parameters
    ----------
    charges:
        Length-``n`` array of nuclear charges ``Z_i``.
    coordinates:
        ``n x 3`` array of atomic coordinates (in angstrom).
    """
    charges = np.asarray(charges, dtype=float)
    coordinates = np.asarray(coordinates, dtype=float)
    n = len(charges)
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i, j] = 0.5 * charges[i] ** 2.4
            else:
                distance = np.linalg.norm(coordinates[i] - coordinates[j])
                matrix[i, j] = charges[i] * charges[j] / distance
    return matrix


def sorted_eigenvalue_descriptor(charges: np.ndarray, coordinates: np.ndarray, size: int) -> np.ndarray:
    """Return a fixed-length sorted-eigenvalue Coulomb descriptor."""
    eigvals = np.linalg.eigvalsh(coulomb_matrix(charges, coordinates))
    eigvals = np.sort(eigvals)[::-1]
    descriptor = np.zeros(size, dtype=float)
    descriptor[: min(size, len(eigvals))] = eigvals[:size]
    return descriptor


class GroundStateRegressor:
    """Gaussian-kernel ridge regressor for molecular ground-state energies."""

    def __init__(self, gamma: float = 1e-3, alpha: float = 1e-6) -> None:
        self.gamma = float(gamma)
        self.alpha = float(alpha)
        self._x_train: np.ndarray | None = None
        self._weights: np.ndarray | None = None

    def _kernel(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        sq = (
            np.sum(a ** 2, axis=1)[:, None]
            + np.sum(b ** 2, axis=1)[None, :]
            - 2.0 * a @ b.T
        )
        return np.exp(-self.gamma * np.maximum(sq, 0.0))

    def fit(self, descriptors: np.ndarray, energies: np.ndarray) -> GroundStateRegressor:
        """Fit the regressor to descriptor/energy pairs."""
        x = np.atleast_2d(np.asarray(descriptors, dtype=float))
        y = np.asarray(energies, dtype=float)
        kernel = self._kernel(x, x)
        kernel += self.alpha * np.eye(kernel.shape[0])
        self._weights = np.linalg.solve(kernel, y)
        self._x_train = x
        return self

    def predict(self, descriptors: np.ndarray) -> np.ndarray:
        """Predict energies for new descriptors."""
        if self._x_train is None or self._weights is None:
            raise RuntimeError("Regressor must be fitted before prediction.")
        x = np.atleast_2d(np.asarray(descriptors, dtype=float))
        return self._kernel(x, self._x_train) @ self._weights


def h2_dissociation_curve(bond_lengths: np.ndarray) -> np.ndarray:
    """Return a Morse-potential model of the H2 dissociation curve (Hartree).

    Parameters approximate the full-configuration-interaction curve in a
    minimal basis and are used by the textbook to illustrate variational
    quantum eigensolvers. Energies are reported relative to two free hydrogen
    atoms.
    """
    r = np.asarray(bond_lengths, dtype=float)
    depth = 0.1745       # well depth (Hartree)
    width = 1.04         # Morse width parameter (1/angstrom)
    r_eq = 0.741         # equilibrium bond length (angstrom)
    exp_term = np.exp(-width * (r - r_eq))
    return depth * (exp_term ** 2 - 2.0 * exp_term)
