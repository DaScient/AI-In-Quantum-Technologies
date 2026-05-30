"""Tests for the benchmark dataset registry and synthetic generators."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make the top-level ``datasets`` package importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import datasets  # noqa: E402


def test_registry_and_describe():
    names = datasets.list_datasets()
    assert "qm9" in names
    assert datasets.describe("qm9").domain == "chemistry"
    with pytest.raises(KeyError):
        datasets.describe("does_not_exist")


def test_synthetic_tomography_dataset_shapes():
    batch = datasets.synthetic_tomography_dataset(n_samples=64, shots=512, seed=1)
    assert batch["expectations"].shape == (64, 3)
    assert batch["bloch"].shape == (64, 3)
    assert batch["expectations"].max() <= 1.0
    assert batch["expectations"].min() >= -1.0


def test_synthetic_syndrome_dataset_parity():
    batch = datasets.synthetic_syndrome_dataset(n_samples=128, n_data=4, seed=2)
    errors = batch["errors"]
    syndromes = batch["syndromes"]
    assert syndromes.shape == (128, 3)
    # Syndrome must equal the parity of adjacent error bits.
    expected = (errors[:, :-1] ^ errors[:, 1:])
    assert (syndromes == expected).all()
