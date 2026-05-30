"""Quantum state tomography by linear inversion with physicality projection.

Given expectation values of an informationally complete set of Pauli
observables, the density matrix of an ``n``-qubit state can be reconstructed as

.. math::

    \\rho = \\frac{1}{2^n} \\sum_{P} \\langle P \\rangle \\, P,

where the sum runs over all :math:`4^n` tensor-product Pauli operators. Finite
sampling produces an estimate that may be slightly unphysical; we therefore
project the raw estimate back onto the set of valid density matrices.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from ..linalg import n_qubit_paulis, project_to_density_matrix


def pauli_measurement_operators(n_qubits: int) -> dict[str, np.ndarray]:
    """Return the informationally complete Pauli operator basis."""
    return n_qubit_paulis(n_qubits)


def linear_inversion_tomography(
    expectations: Mapping[str, float],
    n_qubits: int,
    project: bool = True,
) -> np.ndarray:
    """Reconstruct a density matrix from Pauli expectation values.

    Parameters
    ----------
    expectations:
        Mapping from Pauli strings (e.g. ``"XZ"``) to measured expectation
        values in ``[-1, 1]``. The identity term ``"II...I"`` is optional and
        defaults to ``1``. Missing Pauli terms are assumed to be ``0``.
    n_qubits:
        Number of qubits.
    project:
        If ``True`` (default), project the linear-inversion estimate onto the
        set of physical density matrices.

    Returns
    -------
    numpy.ndarray
        A ``2**n x 2**n`` density matrix.
    """
    if n_qubits < 1:
        raise ValueError("n_qubits must be >= 1")
    basis = n_qubit_paulis(n_qubits)
    dim = 2 ** n_qubits
    identity_label = "I" * n_qubits

    rho = np.zeros((dim, dim), dtype=complex)
    for label, operator in basis.items():
        if label == identity_label:
            coeff = float(expectations.get(label, 1.0))
        else:
            coeff = float(expectations.get(label, 0.0))
        if not -1.0 - 1e-9 <= coeff <= 1.0 + 1e-9:
            raise ValueError(f"Expectation for {label} must lie in [-1, 1]; got {coeff}")
        rho += coeff * operator
    rho /= dim

    if project:
        rho = project_to_density_matrix(rho)
    return rho
