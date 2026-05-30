"""AI for quantum devices: tomography, control, error correction, compilation.

This sub-package corresponds to **Part III** of the textbook and underpins the
``/api/v1/quantum/*`` endpoints of the companion service.
"""

from __future__ import annotations

from .circuit_optimize import optimize_circuit
from .error_correction import decode_repetition_code, syndrome_lookup_decoder
from .optimal_control import grape_pulse, simulate_pulse
from .process_tomography import linear_inversion_process_tomography
from .state_tomography import linear_inversion_tomography, pauli_measurement_operators

__all__ = [
    "linear_inversion_tomography",
    "pauli_measurement_operators",
    "linear_inversion_process_tomography",
    "grape_pulse",
    "simulate_pulse",
    "decode_repetition_code",
    "syndrome_lookup_decoder",
    "optimize_circuit",
]
