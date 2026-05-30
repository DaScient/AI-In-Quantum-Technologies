"""ML-accelerated quantum chemistry (Part IV of the textbook).

These reference implementations expose the workflow used by the ``MolQNet``
model: molecules are turned into permutation-invariant descriptors and mapped to
energies by a regressor. The :class:`GroundStateRegressor` here is a transparent
kernel-ridge baseline that the notebooks compare against the SE(3)-equivariant
neural network.
"""

from __future__ import annotations

from .excited_states import predict_excitation_spectrum
from .ground_state import GroundStateRegressor, coulomb_matrix, h2_dissociation_curve

__all__ = [
    "GroundStateRegressor",
    "coulomb_matrix",
    "h2_dissociation_curve",
    "predict_excitation_spectrum",
]
