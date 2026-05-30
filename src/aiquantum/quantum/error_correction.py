"""Classical decoders for quantum error correction.

Two complementary decoders are provided:

* :func:`decode_repetition_code` — majority-vote decoding for the bit-flip
  repetition code, the simplest illustration of stabiliser decoding.
* :func:`syndrome_lookup_decoder` — a maximum-likelihood lookup-table decoder
  that maps each syndrome to its most probable recovery operation. This is the
  classical baseline against which the learned ``ErrorFormer`` decoder described
  in the textbook is benchmarked.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def decode_repetition_code(syndrome: Sequence[int], n_data: int) -> np.ndarray:
    """Decode a bit-flip repetition-code syndrome by minimum-weight matching.

    Parameters
    ----------
    syndrome:
        Length ``n_data - 1`` sequence of parity checks ``Z_i Z_{i+1}`` with
        entries in ``{0, 1}``.
    n_data:
        Number of physical data qubits.

    Returns
    -------
    numpy.ndarray
        A length-``n_data`` binary recovery (1 = apply X correction).
    """
    syndrome = np.asarray(syndrome, dtype=int)
    if syndrome.shape[0] != n_data - 1:
        raise ValueError("syndrome length must equal n_data - 1")

    # Detection events are the positions where the parity differs from the
    # boundary. Minimum-weight matching on a 1-D chain pairs consecutive
    # defects; the correction is the parity prefix-sum of the syndrome.
    correction = np.zeros(n_data, dtype=int)
    flip = 0
    for i in range(n_data - 1):
        flip ^= int(syndrome[i])
        correction[i + 1] = flip

    # Choose the lower-weight of the recovery and its logical complement.
    if correction.sum() > n_data - correction.sum():
        correction = 1 - correction
    return correction


def build_syndrome_table(
    error_probabilities: dict[tuple[int, ...], float],
    parity_check_matrix: np.ndarray,
) -> dict[tuple[int, ...], tuple[int, ...]]:
    """Build a maximum-likelihood syndrome -> recovery lookup table.

    Parameters
    ----------
    error_probabilities:
        Mapping from an error pattern (tuple of 0/1) to its prior probability.
    parity_check_matrix:
        Binary parity-check matrix ``H`` of shape ``(n_checks, n_qubits)``.

    Returns
    -------
    dict
        Mapping from syndrome tuple to the most probable error pattern.
    """
    h = np.asarray(parity_check_matrix, dtype=int) % 2
    table: dict[tuple[int, ...], tuple[float, tuple[int, ...]]] = {}
    for error, prob in error_probabilities.items():
        vec = np.asarray(error, dtype=int) % 2
        syndrome = tuple((h @ vec) % 2)
        if syndrome not in table or prob > table[syndrome][0]:
            table[syndrome] = (prob, tuple(int(b) for b in vec))
    return {syndrome: recovery for syndrome, (_, recovery) in table.items()}


def syndrome_lookup_decoder(
    syndrome: Sequence[int],
    table: dict[tuple[int, ...], tuple[int, ...]],
    n_qubits: int,
) -> np.ndarray:
    """Decode a syndrome using a precomputed lookup table.

    Unknown syndromes fall back to the all-identity recovery.
    """
    key = tuple(int(b) % 2 for b in syndrome)
    recovery = table.get(key)
    if recovery is None:
        return np.zeros(n_qubits, dtype=int)
    return np.asarray(recovery, dtype=int)
