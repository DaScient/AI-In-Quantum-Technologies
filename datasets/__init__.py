"""Benchmark dataset loaders for *AI in Quantum Technologies*.

The textbook references a number of external corpora (QM9, Materials Project,
Stim-generated syndromes, and so on). To keep the repository lightweight and
fully reproducible, this package does **not** vendor those multi-gigabyte
archives. Instead it provides:

1. A :data:`REGISTRY` describing each benchmark dataset and where to obtain it.
2. Synthetic *generators* that emit data in the exact schema of each benchmark,
   so that every notebook, test, and tutorial runs offline with no downloads.

Real archives can be dropped into ``datasets/raw/<name>/`` and loaded with the
same interface once the corresponding ``download`` URL has been fetched.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DatasetSpec:
    """Metadata describing a benchmark dataset."""

    name: str
    domain: str
    description: str
    source_url: str
    license: str


REGISTRY: dict[str, DatasetSpec] = {
    "qasmbench": DatasetSpec(
        "qasmbench",
        "circuits",
        "Benchmark suite of OpenQASM circuits spanning small, medium, and large scales.",
        "https://github.com/pnnl/QASMBench",
        "BSD-2-Clause",
    ),
    "qm9": DatasetSpec(
        "qm9",
        "chemistry",
        "134k small organic molecules with DFT-computed properties.",
        "http://quantum-machine.org/datasets/",
        "CC0-1.0",
    ),
    "materials_project": DatasetSpec(
        "materials_project",
        "materials",
        "Computed properties of inorganic crystals.",
        "https://materialsproject.org",
        "CC-BY-4.0",
    ),
    "supercon": DatasetSpec(
        "supercon",
        "materials",
        "Superconductor critical temperatures with composition descriptors.",
        "https://supercon.nims.go.jp",
        "Custom (NIMS)",
    ),
    "stim_syndromes": DatasetSpec(
        "stim_syndromes",
        "error_correction",
        "Surface-code syndrome/error pairs generated with Stim.",
        "https://github.com/quantumlib/Stim",
        "Apache-2.0",
    ),
    "qkd_traces": DatasetSpec(
        "qkd_traces",
        "cryptography",
        "Experimental QKD traces (gain and QBER vs. distance).",
        "https://github.com/tqsd/QuNetSim",
        "MIT",
    ),
}


def list_datasets() -> list[str]:
    """Return the names of all registered benchmark datasets."""
    return sorted(REGISTRY)


def describe(name: str) -> DatasetSpec:
    """Return the :class:`DatasetSpec` for ``name``."""
    if name not in REGISTRY:
        raise KeyError(f"Unknown dataset {name!r}. Available: {list_datasets()}")
    return REGISTRY[name]


def synthetic_tomography_dataset(
    n_samples: int = 256,
    n_qubits: int = 1,
    shots: int = 1024,
    seed: int = 0,
) -> dict[str, np.ndarray]:
    """Generate noisy Pauli-expectation samples for random pure states.

    Returns a dict with ``expectations`` (``n_samples x 3**? `` Pauli values) and
    the underlying ``bloch`` vectors, in the schema consumed by the state
    tomography notebook.
    """
    if n_qubits != 1:
        raise NotImplementedError("synthetic tomography generator supports 1 qubit")
    rng = np.random.default_rng(seed)
    # Random pure single-qubit states as Bloch vectors on the sphere.
    vectors = rng.normal(size=(n_samples, 3))
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    # Simulate finite-shot estimation noise (binomial standard error).
    noise = rng.normal(scale=1.0 / np.sqrt(shots), size=vectors.shape)
    measured = np.clip(vectors + noise, -1.0, 1.0)
    return {"bloch": vectors, "expectations": measured}


def synthetic_syndrome_dataset(
    n_samples: int = 1000,
    n_data: int = 3,
    error_rate: float = 0.1,
    seed: int = 0,
) -> dict[str, np.ndarray]:
    """Generate bit-flip repetition-code syndrome/error pairs.

    Returns a dict with ``errors`` (``n_samples x n_data``) and ``syndromes``
    (``n_samples x (n_data - 1)``) suitable for training and benchmarking
    decoders.
    """
    rng = np.random.default_rng(seed)
    errors = (rng.random((n_samples, n_data)) < error_rate).astype(int)
    # Z_i Z_{i+1} parity checks.
    syndromes = (errors[:, :-1] ^ errors[:, 1:]).astype(int)
    return {"errors": errors, "syndromes": syndromes}


__all__ = [
    "DatasetSpec",
    "REGISTRY",
    "list_datasets",
    "describe",
    "synthetic_tomography_dataset",
    "synthetic_syndrome_dataset",
]
