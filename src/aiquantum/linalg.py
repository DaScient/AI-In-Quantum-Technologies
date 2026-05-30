"""Linear-algebra primitives shared across the :mod:`aiquantum` domain modules.

The functions here form a small, dependency-light foundation for working with
quantum states and operators expressed as dense complex matrices. They are used
throughout the library and are deliberately written for clarity over raw
performance, mirroring the pedagogical goals of the accompanying textbook.
"""

from __future__ import annotations

import numpy as np

# --- Single-qubit Pauli basis -------------------------------------------------

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}


def is_unitary(matrix: np.ndarray, atol: float = 1e-8) -> bool:
    """Return ``True`` if ``matrix`` is unitary within ``atol``."""
    matrix = np.asarray(matrix, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return False
    identity = np.eye(matrix.shape[0], dtype=complex)
    return np.allclose(matrix.conj().T @ matrix, identity, atol=atol)


def is_density_matrix(rho: np.ndarray, atol: float = 1e-6) -> bool:
    """Return ``True`` if ``rho`` is a valid density matrix.

    A density matrix is Hermitian, positive semi-definite, and unit-trace.
    """
    rho = np.asarray(rho, dtype=complex)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        return False
    if not np.allclose(rho, rho.conj().T, atol=atol):
        return False
    if not np.isclose(np.trace(rho).real, 1.0, atol=atol):
        return False
    eigvals = np.linalg.eigvalsh(rho)
    return bool(np.all(eigvals >= -atol))


def project_to_density_matrix(matrix: np.ndarray) -> np.ndarray:
    """Project a Hermitian estimate onto the set of physical density matrices.

    Implements the fast trace-preserving projection of Smolin, Gambetta, and
    Smith (*Phys. Rev. Lett.* **108**, 070502, 2012): eigenvalues are clipped to
    be non-negative and renormalised so the trace equals one.
    """
    matrix = np.asarray(matrix, dtype=complex)
    hermitian = 0.5 * (matrix + matrix.conj().T)
    eigvals, eigvecs = np.linalg.eigh(hermitian)
    eigvals = _project_simplex(eigvals.real)
    return (eigvecs * eigvals) @ eigvecs.conj().T


def _project_simplex(eigvals: np.ndarray) -> np.ndarray:
    """Project a real vector onto the probability simplex (sum to 1, >= 0)."""
    sorted_vals = np.sort(eigvals)[::-1]
    cumulative = np.cumsum(sorted_vals)
    rho_index = np.nonzero(sorted_vals + (1.0 - cumulative) / (np.arange(len(eigvals)) + 1) > 0)[0]
    if len(rho_index) == 0:
        return np.full_like(eigvals, 1.0 / len(eigvals))
    k = rho_index[-1] + 1
    theta = (cumulative[k - 1] - 1.0) / k
    return np.maximum(eigvals - theta, 0.0)


def fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Uhlmann–Jozsa fidelity between two density matrices.

    Returns a value in ``[0, 1]`` using the convention
    ``F = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))**2``.
    """
    rho = np.asarray(rho, dtype=complex)
    sigma = np.asarray(sigma, dtype=complex)
    sqrt_rho = _matrix_sqrt(rho)
    inner = sqrt_rho @ sigma @ sqrt_rho
    eigvals = np.clip(np.linalg.eigvalsh(inner).real, 0.0, None)
    return float(np.sum(np.sqrt(eigvals)) ** 2)


def _matrix_sqrt(matrix: np.ndarray) -> np.ndarray:
    eigvals, eigvecs = np.linalg.eigh(0.5 * (matrix + matrix.conj().T))
    eigvals = np.clip(eigvals.real, 0.0, None)
    return (eigvecs * np.sqrt(eigvals)) @ eigvecs.conj().T


def purity(rho: np.ndarray) -> float:
    """Return ``Tr(rho^2)``, the purity of a quantum state."""
    rho = np.asarray(rho, dtype=complex)
    return float(np.trace(rho @ rho).real)


def von_neumann_entropy(rho: np.ndarray, base: float = 2.0) -> float:
    """Von Neumann entropy ``S(rho) = -Tr(rho log rho)`` in the given base."""
    eigvals = np.clip(np.linalg.eigvalsh(np.asarray(rho, dtype=complex)).real, 0.0, None)
    nonzero = eigvals[eigvals > 1e-12]
    return float(-np.sum(nonzero * np.log(nonzero)) / np.log(base))


def expectation(observable: np.ndarray, rho: np.ndarray) -> float:
    """Expectation value ``Tr(observable @ rho)`` of a Hermitian observable."""
    return float(np.trace(np.asarray(observable, dtype=complex) @ np.asarray(rho, dtype=complex)).real)


def n_qubit_paulis(n_qubits: int) -> dict[str, np.ndarray]:
    """Return the full tensor-product Pauli basis for ``n_qubits`` qubits.

    Keys are Pauli strings such as ``"XZ"`` and values are ``2**n x 2**n``
    matrices. The basis has ``4**n`` elements and is informationally complete.
    """
    if n_qubits < 1:
        raise ValueError("n_qubits must be >= 1")
    labels = ["I", "X", "Y", "Z"]
    basis: dict[str, np.ndarray] = {}

    def _build(prefix: str, matrix: np.ndarray, depth: int) -> None:
        if depth == n_qubits:
            basis[prefix] = matrix
            return
        for label in labels:
            _build(prefix + label, np.kron(matrix, PAULI[label]) if depth else PAULI[label], depth + 1)

    _build("", np.array([[1.0]], dtype=complex), 0)
    return basis
