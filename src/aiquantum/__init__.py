"""AI in Quantum Technologies — code-first companion library.

This package implements the reference algorithms, models, and services that
accompany the textbook *AI in Quantum Technologies: Theory, Applications,
Practice, and Society* (DaScient Press Ltd., 2026).

The library is organised into domain sub-packages that mirror the parts of the
textbook and the public API surface:

- :mod:`aiquantum.quantum`    — tomography, optimal control, error correction,
  and circuit optimisation for quantum *devices*.
- :mod:`aiquantum.qchem`      — ML-accelerated quantum chemistry.
- :mod:`aiquantum.materials`  — inverse design and property prediction for
  quantum *matter*.
- :mod:`aiquantum.qml`         — quantum machine learning kernels and trainers.
- :mod:`aiquantum.crypto`      — quantum key distribution analysis.
- :mod:`aiquantum.metrology`   — quantum sensing and metrology.
- :mod:`aiquantum.simulate`    — device noise-model learning.

All implementations depend only on :mod:`numpy` and :mod:`scipy` so that the
core science remains runnable in any environment. Heavy quantum and deep
learning back-ends (Qiskit, PennyLane, Cirq, PyTorch, JAX) are declared as
optional extras and consumed by the notebooks and tutorials.
"""

from __future__ import annotations

__all__ = [
    "__version__",
    "linalg",
    "quantum",
    "qchem",
    "materials",
    "qml",
    "crypto",
    "metrology",
    "simulate",
]

__version__ = "0.1.0"
