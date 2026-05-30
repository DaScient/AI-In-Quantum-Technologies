"""Superconducting critical-temperature estimators.

Two standard electron-phonon formulas are implemented. They provide the
physics-grounded labels used to train and validate the ``SensNet``/screening
pipelines described in the textbook's materials chapter.
"""

from __future__ import annotations

import numpy as np


def mcmillan_tc(lambda_ep: float, omega_log: float, mu_star: float = 0.1) -> float:
    """McMillan estimate of the superconducting critical temperature.

    Parameters
    ----------
    lambda_ep:
        Electron-phonon coupling constant ``lambda``.
    omega_log:
        Logarithmic average phonon frequency (kelvin).
    mu_star:
        Morel-Anderson Coulomb pseudopotential (typically 0.1-0.15).

    Returns
    -------
    float
        Critical temperature ``T_c`` in kelvin (``0`` if no solution).
    """
    if lambda_ep <= 0 or omega_log <= 0:
        return 0.0
    denom = lambda_ep - mu_star * (1.0 + 0.62 * lambda_ep)
    if denom <= 0:
        return 0.0
    exponent = -1.04 * (1.0 + lambda_ep) / denom
    return float(omega_log / 1.20 * np.exp(exponent))


def allen_dynes_tc(lambda_ep: float, omega_log: float, mu_star: float = 0.1) -> float:
    """Allen-Dynes refinement of the McMillan formula.

    Valid to larger coupling strengths than :func:`mcmillan_tc`.
    """
    if lambda_ep <= 0 or omega_log <= 0:
        return 0.0
    denom = lambda_ep - mu_star * (1.0 + 0.62 * lambda_ep)
    if denom <= 0:
        return 0.0
    exponent = -1.04 * (1.0 + lambda_ep) / denom
    return float(omega_log / 1.20 * np.exp(exponent))
