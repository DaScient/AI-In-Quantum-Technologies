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


def allen_dynes_tc(
    lambda_ep: float,
    omega_log: float,
    mu_star: float = 0.1,
    omega2: float | None = None,
) -> float:
    """Allen-Dynes refinement of the McMillan formula.

    Adds the strong-coupling (:math:`f_1`) and spectral-shape (:math:`f_2`)
    correction factors that extend validity to larger coupling strengths than
    :func:`mcmillan_tc`.

    Parameters
    ----------
    lambda_ep:
        Electron-phonon coupling constant ``lambda``.
    omega_log:
        Logarithmic average phonon frequency (kelvin).
    mu_star:
        Morel-Anderson Coulomb pseudopotential (typically 0.1-0.15).
    omega2:
        Root-mean-square phonon frequency (kelvin) used by the :math:`f_2`
        factor. Defaults to ``omega_log`` (which yields :math:`f_2 = 1`).

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

    # Strong-coupling correction f1 (Allen & Dynes, Phys. Rev. B 12, 905).
    lambda1 = 2.46 * (1.0 + 3.8 * mu_star)
    f1 = (1.0 + (lambda_ep / lambda1) ** 1.5) ** (1.0 / 3.0)

    # Spectral-shape correction f2; reduces to 1 when omega2 == omega_log.
    omega2 = omega_log if omega2 is None else omega2
    ratio = omega2 / omega_log
    lambda2 = 1.82 * (1.0 + 6.3 * mu_star) * ratio
    f2 = 1.0 + (ratio - 1.0) * lambda_ep**2 / (lambda_ep**2 + lambda2**2)

    return float(f1 * f2 * omega_log / 1.20 * np.exp(exponent))
