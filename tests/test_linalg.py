"""Tests for the linear-algebra primitives."""

from __future__ import annotations

import numpy as np

from aiquantum.linalg import (
    fidelity,
    is_density_matrix,
    is_unitary,
    n_qubit_paulis,
    project_to_density_matrix,
    purity,
    von_neumann_entropy,
)


def test_pauli_basis_size_and_hermiticity():
    basis = n_qubit_paulis(2)
    assert len(basis) == 16
    for matrix in basis.values():
        assert matrix.shape == (4, 4)
        assert np.allclose(matrix, matrix.conj().T)


def test_is_unitary():
    assert is_unitary(np.array([[0, 1], [1, 0]], dtype=complex))
    assert not is_unitary(np.array([[1, 1], [0, 1]], dtype=complex))


def test_density_matrix_checks_and_projection():
    pure = np.array([[1, 0], [0, 0]], dtype=complex)
    assert is_density_matrix(pure)
    assert np.isclose(purity(pure), 1.0)
    assert np.isclose(von_neumann_entropy(pure), 0.0)

    unphysical = np.array([[1.2, 0], [0, -0.2]], dtype=complex)
    projected = project_to_density_matrix(unphysical)
    assert is_density_matrix(projected)


def test_fidelity_bounds():
    rho = np.array([[1, 0], [0, 0]], dtype=complex)
    sigma = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    assert np.isclose(fidelity(rho, rho), 1.0)
    assert 0.0 <= fidelity(rho, sigma) <= 1.0
    assert np.isclose(fidelity(rho, sigma), 0.5, atol=1e-6)
