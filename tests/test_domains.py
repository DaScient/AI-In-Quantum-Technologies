"""Tests for chemistry, materials, QML, crypto, metrology, simulation."""

from __future__ import annotations

import numpy as np

from aiquantum.crypto import bb84_key_rate, binary_entropy
from aiquantum.materials import allen_dynes_tc, generate_crystal, mcmillan_tc
from aiquantum.metrology import (
    heisenberg_limit,
    optimal_phase_sensitivity,
    standard_quantum_limit,
)
from aiquantum.qchem import (
    GroundStateRegressor,
    coulomb_matrix,
    h2_dissociation_curve,
    predict_excitation_spectrum,
)
from aiquantum.qml import quantum_kernel_matrix, train_hybrid_model
from aiquantum.simulate import average_gate_infidelity, learn_pauli_channel


def test_coulomb_matrix_symmetry():
    charges = np.array([1.0, 1.0])
    coords = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.74]])
    cm = coulomb_matrix(charges, coords)
    assert np.allclose(cm, cm.T)
    assert cm[0, 1] > 0


def test_ground_state_regressor_fits_linear_signal():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(20, 4))
    y = x[:, 0] * 2.0 - x[:, 1]
    model = GroundStateRegressor(gamma=0.5, alpha=1e-8).fit(x, y)
    pred = model.predict(x)
    assert np.corrcoef(pred, y)[0, 1] > 0.9


def test_h2_curve_minimum_near_equilibrium():
    r = np.linspace(0.4, 3.0, 400)
    energy = h2_dissociation_curve(r)
    r_min = r[np.argmin(energy)]
    assert abs(r_min - 0.741) < 0.05
    assert energy.min() < 0


def test_excitation_spectrum_peaks():
    grid, intensity = predict_excitation_spectrum([2.0, 4.0], [1.0, 0.5], broadening=0.05)
    assert intensity.max() > 0
    assert len(grid) == len(intensity)


def test_superconductor_formulas_positive():
    tc_md = mcmillan_tc(0.8, 400.0, 0.1)
    tc_ad = allen_dynes_tc(0.8, 400.0, 0.1)
    assert tc_md > 0
    assert tc_ad > 0


def test_generate_crystal_matches_density():
    structure = generate_crystal(["Cu"], target_density=8.96, seed=0)
    assert abs(structure.density - 8.96) < 0.1


def test_quantum_kernel_properties():
    x = np.array([[0.0], [0.0], [np.pi / 2]])
    k = quantum_kernel_matrix(x)
    assert np.allclose(np.diag(k), 1.0)
    assert np.isclose(k[0, 1], 1.0)
    assert k[0, 2] < 1e-9


def test_hybrid_training_separable():
    x = np.array([[0.0], [0.1], [1.5], [1.6]])
    y = np.array([0, 0, 1, 1])
    summary = train_hybrid_model(x, y)
    assert summary["train_accuracy"] >= 0.75


def test_bb84_key_rate_monotonic():
    assert binary_entropy(0.0) == 0.0
    low = bb84_key_rate(0.01)
    high = bb84_key_rate(0.10)
    assert low > high >= 0
    assert bb84_key_rate(0.5) == 0.0


def test_metrology_limits_ordering():
    n = 16
    sql = standard_quantum_limit(n)
    hl = heisenberg_limit(n)
    assert hl < sql
    assert optimal_phase_sensitivity(float(n)) > 0


def test_learn_pauli_channel_normalised():
    probs = learn_pauli_channel({"X": 0.98, "Y": 0.98, "Z": 0.99})
    assert abs(sum(probs.values()) - 1.0) < 1e-9
    assert all(v >= 0 for v in probs.values())
    assert 0.0 <= average_gate_infidelity(probs) <= 1.0
