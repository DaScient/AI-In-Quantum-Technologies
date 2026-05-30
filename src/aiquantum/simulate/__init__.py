"""Learning device noise models from calibration data (Part II).

Backs ``/api/v1/simulate/noise_model``. A single-qubit Pauli channel is fully
specified by its Pauli error probabilities ``(p_I, p_X, p_Y, p_Z)``. These are
recovered from the measured Pauli fidelities (the diagonal of the Pauli transfer
matrix) by the Walsh-Hadamard relation, the workhorse of randomised
benchmarking and gate-set tomography.
"""

from __future__ import annotations

from collections.abc import Mapping


def learn_pauli_channel(pauli_fidelities: Mapping[str, float]) -> dict[str, float]:
    """Recover single-qubit Pauli error probabilities from fidelities.

    Parameters
    ----------
    pauli_fidelities:
        Mapping with keys ``"X"``, ``"Y"``, ``"Z"`` giving the measured Pauli
        fidelities :math:`f_P = \\operatorname{Tr}[P\\,\\mathcal{E}(P)]/2` in
        ``[-1, 1]``.

    Returns
    -------
    dict
        Mapping with keys ``"I"``, ``"X"``, ``"Y"``, ``"Z"`` giving the Pauli
        error probabilities, clipped to be non-negative and renormalised.
    """
    f_x = float(pauli_fidelities.get("X", 1.0))
    f_y = float(pauli_fidelities.get("Y", 1.0))
    f_z = float(pauli_fidelities.get("Z", 1.0))
    for name, value in (("X", f_x), ("Y", f_y), ("Z", f_z)):
        if not -1.0 <= value <= 1.0:
            raise ValueError(f"fidelity {name} must lie in [-1, 1]; got {value}")

    probs = {
        "I": (1.0 + f_x + f_y + f_z) / 4.0,
        "X": (1.0 + f_x - f_y - f_z) / 4.0,
        "Y": (1.0 - f_x + f_y - f_z) / 4.0,
        "Z": (1.0 - f_x - f_y + f_z) / 4.0,
    }
    clipped = {k: max(v, 0.0) for k, v in probs.items()}
    total = sum(clipped.values())
    if total <= 0:
        return {k: 0.25 for k in clipped}
    return {k: v / total for k, v in clipped.items()}


def average_gate_infidelity(pauli_error_probabilities: Mapping[str, float]) -> float:
    """Average gate infidelity ``1 - F_avg`` of a single-qubit Pauli channel."""
    p_error = sum(v for k, v in pauli_error_probabilities.items() if k != "I")
    # For a single qubit, F_avg = 1 - (d/(d+1)) * p_error with d = 2.
    return float((2.0 / 3.0) * p_error)
