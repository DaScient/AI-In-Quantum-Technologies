"""Quantum process tomography via the Pauli-transfer-matrix representation.

A completely positive, trace-preserving (CPTP) map :math:`\\mathcal{E}` acting on
``n`` qubits is fully characterised by its Pauli transfer matrix (PTM)

.. math::

    R_{ij} = \\frac{1}{2^n} \\operatorname{Tr}\\!\\left[ P_i\\, \\mathcal{E}(P_j) \\right],

whose entries are real numbers in ``[-1, 1]``. Given input Pauli operators and
the measured Pauli expectation values of the corresponding outputs, the PTM is
recovered by linear inversion.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from ..linalg import n_qubit_paulis


def linear_inversion_process_tomography(
    transfer_data: Mapping[str, Mapping[str, float]],
    n_qubits: int,
) -> np.ndarray:
    """Reconstruct the Pauli transfer matrix of an unknown process.

    Parameters
    ----------
    transfer_data:
        Nested mapping ``transfer_data[input_pauli][output_pauli] = value`` where
        ``value`` approximates :math:`\\operatorname{Tr}[P_{out}\\,
        \\mathcal{E}(P_{in})] / 2^n`. Missing entries default to ``0`` except the
        identity-to-identity entry which defaults to ``1`` (trace preservation).
    n_qubits:
        Number of qubits.

    Returns
    -------
    numpy.ndarray
        A ``4**n x 4**n`` real Pauli transfer matrix. Rows and columns are
        ordered consistently with :func:`aiquantum.linalg.n_qubit_paulis`.
    """
    if n_qubits < 1:
        raise ValueError("n_qubits must be >= 1")
    labels = list(n_qubit_paulis(n_qubits).keys())
    index = {label: i for i, label in enumerate(labels)}
    size = len(labels)  # 4**n
    identity_label = "I" * n_qubits

    ptm = np.zeros((size, size), dtype=float)
    ptm[index[identity_label], index[identity_label]] = 1.0

    for in_label, outputs in transfer_data.items():
        if in_label not in index:
            raise ValueError(f"Unknown input Pauli label: {in_label}")
        j = index[in_label]
        for out_label, value in outputs.items():
            if out_label not in index:
                raise ValueError(f"Unknown output Pauli label: {out_label}")
            ptm[index[out_label], j] = float(value)
    return ptm
