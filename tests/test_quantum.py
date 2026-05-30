"""Tests for the quantum-device modules."""

from __future__ import annotations

import numpy as np

from aiquantum.linalg import X, is_density_matrix
from aiquantum.quantum import (
    decode_repetition_code,
    grape_pulse,
    linear_inversion_process_tomography,
    linear_inversion_tomography,
    optimize_circuit,
)
from aiquantum.quantum.circuit_optimize import circuit_depth


def test_state_tomography_recovers_plus_state():
    # |+> has <X>=1, <Y>=0, <Z>=0.
    rho = linear_inversion_tomography({"X": 1.0}, 1)
    assert is_density_matrix(rho)
    expected = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
    assert np.allclose(rho, expected, atol=1e-6)


def test_state_tomography_rejects_out_of_range():
    import pytest

    with pytest.raises(ValueError):
        linear_inversion_tomography({"Z": 2.0}, 1)


def test_process_tomography_identity():
    ptm = linear_inversion_process_tomography({}, 1)
    assert ptm.shape == (4, 4)
    assert ptm[0, 0] == 1.0


def test_grape_learns_x_gate():
    result = grape_pulse(X, n_steps=20, dt=0.2, iterations=400, seed=1)
    assert result.fidelity > 0.99


def test_repetition_decoder_no_error():
    recovery = decode_repetition_code([0, 0], n_data=3)
    assert recovery.sum() == 0


def test_repetition_decoder_single_error():
    # A single middle-qubit flip produces syndrome (1, 1).
    recovery = decode_repetition_code([1, 1], n_data=3)
    assert recovery.sum() == 1


def test_circuit_optimize_cancels_and_fuses():
    circuit = [
        {"gate": "H", "qubits": [0]},
        {"gate": "H", "qubits": [0]},
        {"gate": "RZ", "qubits": [1], "param": 0.1},
        {"gate": "RZ", "qubits": [1], "param": 0.2},
    ]
    optimized = optimize_circuit(circuit)
    assert len(optimized) == 1
    assert optimized[0]["gate"] == "RZ"
    assert np.isclose(optimized[0]["param"], 0.3)


def test_circuit_depth_parallelism():
    circuit = [
        {"gate": "H", "qubits": [0]},
        {"gate": "H", "qubits": [1]},
        {"gate": "CNOT", "qubits": [0, 1]},
    ]
    assert circuit_depth(circuit) == 2
