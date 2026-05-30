"""Phase-estimation sensitivity limits for quantum sensing.

For ``N`` probes and ``mu`` independent repetitions, the phase uncertainty of an
unentangled (coherent) strategy is bounded by the standard quantum limit
:math:`\\Delta\\phi_{\\text{SQL}} = 1/\\sqrt{\\mu N}`, while a maximally entangled
(GHZ/NOON) strategy reaches the Heisenberg limit
:math:`\\Delta\\phi_{\\text{HL}} = 1/(N\\sqrt{\\mu})`. The achievable sensitivity for
a given quantum Fisher information ``F_Q`` follows the quantum Cramér-Rao bound
:math:`\\Delta\\phi \\ge 1/\\sqrt{\\mu F_Q}`.
"""

from __future__ import annotations

import numpy as np


def standard_quantum_limit(n_probes: int, repetitions: int = 1) -> float:
    """Standard quantum limit on phase uncertainty."""
    _validate(n_probes, repetitions)
    return float(1.0 / np.sqrt(repetitions * n_probes))


def heisenberg_limit(n_probes: int, repetitions: int = 1) -> float:
    """Heisenberg limit on phase uncertainty."""
    _validate(n_probes, repetitions)
    return float(1.0 / (n_probes * np.sqrt(repetitions)))


def optimal_phase_sensitivity(quantum_fisher_information: float, repetitions: int = 1) -> float:
    """Quantum Cramér-Rao bound on phase uncertainty for a given QFI."""
    if quantum_fisher_information <= 0:
        raise ValueError("quantum_fisher_information must be positive")
    if repetitions < 1:
        raise ValueError("repetitions must be >= 1")
    return float(1.0 / np.sqrt(repetitions * quantum_fisher_information))


def _validate(n_probes: int, repetitions: int) -> None:
    if n_probes < 1:
        raise ValueError("n_probes must be >= 1")
    if repetitions < 1:
        raise ValueError("repetitions must be >= 1")
