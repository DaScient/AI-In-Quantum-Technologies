"""Quantum kernels via exact state-vector simulation.

We use a product-state *angle-encoding* feature map: feature ``x_j`` rotates
qubit ``j`` by ``R_y(2 x_j)`` applied to ``|0>``. The resulting feature state is
a tensor product of single-qubit states, and the quantum kernel is the squared
state overlap

.. math::

    k(x, y) = \\lvert \\langle \\phi(x) \\mid \\phi(y) \\rangle \\rvert^2,

which factorises across qubits and is therefore exact and inexpensive to
compute for the small examples in the textbook.
"""

from __future__ import annotations

import numpy as np


def angle_feature_map(x: np.ndarray) -> np.ndarray:
    """Return the product feature state for a single sample.

    Each feature is encoded as a single-qubit state
    ``[cos(x_j), sin(x_j)]`` and the full state is their tensor product.
    """
    x = np.asarray(x, dtype=float).ravel()
    state = np.array([1.0], dtype=complex)
    for value in x:
        qubit = np.array([np.cos(value), np.sin(value)], dtype=complex)
        state = np.kron(state, qubit)
    return state


def quantum_kernel_matrix(
    x_a: np.ndarray,
    x_b: np.ndarray | None = None,
) -> np.ndarray:
    """Compute the quantum kernel (Gram) matrix between two datasets.

    Parameters
    ----------
    x_a:
        ``(n_a, n_features)`` array of samples.
    x_b:
        ``(n_b, n_features)`` array; defaults to ``x_a`` for a symmetric Gram
        matrix.

    Returns
    -------
    numpy.ndarray
        ``(n_a, n_b)`` matrix of kernel values in ``[0, 1]``.
    """
    x_a = np.atleast_2d(np.asarray(x_a, dtype=float))
    symmetric = x_b is None
    x_b = x_a if symmetric else np.atleast_2d(np.asarray(x_b, dtype=float))
    if x_a.shape[1] != x_b.shape[1]:
        raise ValueError("x_a and x_b must have the same number of features")

    states_a = np.stack([angle_feature_map(row) for row in x_a])
    states_b = states_a if symmetric else np.stack([angle_feature_map(row) for row in x_b])
    overlaps = states_a.conj() @ states_b.T
    return np.abs(overlaps) ** 2
