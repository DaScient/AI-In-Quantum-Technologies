"""Quantum machine learning: kernels and hybrid training (Part VI).

Backs the ``/api/v1/qml/*`` endpoints. The quantum kernel is evaluated exactly by
state-vector simulation of an angle-encoding feature map, providing the
ground-truth values the textbook compares against hardware estimates.
"""

from __future__ import annotations

from .kernel import angle_feature_map, quantum_kernel_matrix
from .train import HybridKernelClassifier, train_hybrid_model

__all__ = [
    "angle_feature_map",
    "quantum_kernel_matrix",
    "HybridKernelClassifier",
    "train_hybrid_model",
]
