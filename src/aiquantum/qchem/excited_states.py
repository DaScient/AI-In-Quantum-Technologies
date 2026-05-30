"""Excited-state (optical spectrum) prediction utilities.

The companion API returns a broadened absorption spectrum given a set of
excitation energies and oscillator strengths. The broadening models the finite
linewidth observed experimentally and produces the smooth spectra plotted in the
quantum-chemistry notebook.
"""

from __future__ import annotations

import numpy as np


def predict_excitation_spectrum(
    excitation_energies: np.ndarray,
    oscillator_strengths: np.ndarray,
    grid: np.ndarray | None = None,
    broadening: float = 0.1,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a Gaussian-broadened absorption spectrum.

    Parameters
    ----------
    excitation_energies:
        Vertical excitation energies (eV).
    oscillator_strengths:
        Dimensionless oscillator strengths, one per excitation.
    grid:
        Energy grid (eV) on which to evaluate the spectrum. If ``None``, a grid
        spanning the excitations with margin is generated.
    broadening:
        Gaussian standard deviation (eV).

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        ``(grid, intensity)`` arrays.
    """
    energies = np.asarray(excitation_energies, dtype=float)
    strengths = np.asarray(oscillator_strengths, dtype=float)
    if energies.shape != strengths.shape:
        raise ValueError("excitation_energies and oscillator_strengths must match")
    if broadening <= 0:
        raise ValueError("broadening must be positive")

    if grid is None:
        lo = float(energies.min()) - 5.0 * broadening
        hi = float(energies.max()) + 5.0 * broadening
        grid = np.linspace(lo, hi, 512)
    grid = np.asarray(grid, dtype=float)

    norm = 1.0 / (broadening * np.sqrt(2.0 * np.pi))
    intensity = np.zeros_like(grid)
    for energy, strength in zip(energies, strengths, strict=False):
        intensity += strength * norm * np.exp(-0.5 * ((grid - energy) / broadening) ** 2)
    return grid, intensity
