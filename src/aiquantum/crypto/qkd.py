"""BB84 secret-key-rate estimation.

The asymptotic secret key rate of the BB84 protocol with one-way error
reconciliation is, following Shor and Preskill,

.. math::

    r = q\\,\\big[\\, 1 - H_2(e_b) - H_2(e_p) \\,\\big],

where :math:`H_2` is the binary entropy, :math:`e_b` and :math:`e_p` are the bit
and phase error rates, and :math:`q` is the sifting/basis-reconciliation
efficiency (``1/2`` for the standard protocol, approaching ``1`` for the
efficient variant). For depolarising channels :math:`e_b = e_p = Q`.
"""

from __future__ import annotations

import numpy as np


def binary_entropy(p: float) -> float:
    """Binary Shannon entropy ``H_2(p)`` in bits."""
    p = float(p)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return float(-p * np.log2(p) - (1.0 - p) * np.log2(1.0 - p))


def bb84_key_rate(
    qber: float,
    phase_error: float | None = None,
    sifting_efficiency: float = 0.5,
    reconciliation_efficiency: float = 1.0,
) -> float:
    """Return the asymptotic BB84 secret key rate (bits per signal).

    Parameters
    ----------
    qber:
        Quantum bit error rate ``e_b`` in ``[0, 0.5]``.
    phase_error:
        Phase error rate ``e_p``; defaults to ``qber`` (symmetric channel).
    sifting_efficiency:
        Fraction of signals retained after basis sifting (``q``).
    reconciliation_efficiency:
        Error-correction efficiency ``f >= 1``; ``1`` is the Shannon limit.

    Returns
    -------
    float
        Secret key rate, clamped at ``0`` when no positive rate is achievable.
    """
    if not 0.0 <= qber <= 0.5:
        raise ValueError("qber must lie in [0, 0.5]")
    if reconciliation_efficiency < 1.0:
        raise ValueError("reconciliation_efficiency must be >= 1")
    e_p = qber if phase_error is None else float(phase_error)
    if not 0.0 <= e_p <= 0.5:
        raise ValueError("phase_error must lie in [0, 0.5]")

    rate = sifting_efficiency * (
        1.0
        - reconciliation_efficiency * binary_entropy(qber)
        - binary_entropy(e_p)
    )
    return float(max(rate, 0.0))
