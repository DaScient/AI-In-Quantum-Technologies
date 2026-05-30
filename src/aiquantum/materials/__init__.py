"""AI for quantum matter: crystal generation and superconductor screening.

Corresponds to **Part IV** of the textbook and the ``/api/v1/materials/*``
endpoints. Property prediction uses transparent physics-based surrogates so the
results are interpretable and reproducible without proprietary models.
"""

from __future__ import annotations

from .crystal import CrystalStructure, generate_crystal
from .superconductor import allen_dynes_tc, mcmillan_tc

__all__ = [
    "CrystalStructure",
    "generate_crystal",
    "allen_dynes_tc",
    "mcmillan_tc",
]
