"""Conditional crystal-structure generation.

The textbook's ``CrysDiff`` diffusion model performs inverse design: it samples
crystal structures conditioned on a desired property. Here we provide a compact,
fully reproducible stand-in that samples a random but physically plausible
structure whose unit-cell volume is steered toward a target mass density. It
serves as the deterministic baseline and reference data format for the learned
generator.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Approximate atomic masses (g/mol) for a handful of common elements.
_ATOMIC_MASS = {
    "H": 1.008, "Li": 6.94, "C": 12.011, "N": 14.007, "O": 15.999,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "Ti": 47.867,
    "Fe": 55.845, "Cu": 63.546, "Ga": 69.723, "As": 74.922, "Y": 88.906,
    "Ba": 137.327, "La": 138.905,
}

_AVOGADRO = 6.02214076e23


@dataclass
class CrystalStructure:
    """A crystal structure in fractional coordinates."""

    lattice: np.ndarray            # 3x3 lattice vectors (angstrom)
    species: list[str]             # length-n element symbols
    frac_coords: np.ndarray        # n x 3 fractional coordinates

    @property
    def volume(self) -> float:
        """Unit-cell volume in cubic angstrom."""
        return float(abs(np.linalg.det(self.lattice)))

    @property
    def density(self) -> float:
        """Mass density in g/cm^3."""
        mass = sum(_ATOMIC_MASS.get(s, 0.0) for s in self.species)  # g/mol
        volume_cm3 = self.volume * 1e-24
        return mass / _AVOGADRO / volume_cm3


def generate_crystal(
    species: list[str],
    target_density: float | None = None,
    seed: int | None = 0,
    max_iter: int = 64,
) -> CrystalStructure:
    """Sample a cubic crystal whose density approaches ``target_density``.

    Parameters
    ----------
    species:
        Element symbols populating the unit cell.
    target_density:
        Desired mass density (g/cm^3). If ``None``, a random cell is returned.
    seed:
        Random seed for reproducibility.
    max_iter:
        Maximum bisection steps used to match the target density.

    Returns
    -------
    CrystalStructure
        The sampled structure.
    """
    if not species:
        raise ValueError("species must be non-empty")
    rng = np.random.default_rng(seed)
    n = len(species)
    frac_coords = rng.random((n, 3))

    def make(a: float) -> CrystalStructure:
        return CrystalStructure(lattice=a * np.eye(3), species=list(species), frac_coords=frac_coords)

    if target_density is None or target_density <= 0:
        return make(3.0 + 2.0 * rng.random())

    mass = sum(_ATOMIC_MASS.get(s, 0.0) for s in species)
    # Analytic cell edge for the target density: rho = mass / (N_A * (a^3 * 1e-24)).
    volume_cm3 = mass / _AVOGADRO / target_density
    edge = (volume_cm3 * 1e24) ** (1.0 / 3.0)

    structure = make(edge)
    # Small reproducible jitter then bisection refinement to honour max_iter.
    lo, hi = 0.5 * edge, 1.5 * edge
    for _ in range(max_iter):
        if abs(structure.density - target_density) < 1e-6:
            break
        if structure.density > target_density:
            lo = structure.lattice[0, 0]
        else:
            hi = structure.lattice[0, 0]
        structure = make(0.5 * (lo + hi))
    return structure
