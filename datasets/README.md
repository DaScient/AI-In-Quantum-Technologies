# Benchmark Datasets

This directory provides programmatic access to the benchmark datasets used
throughout *AI in Quantum Technologies*. To keep the repository lightweight and
fully reproducible offline, large external archives are **not** vendored here.
Instead, `datasets/__init__.py` offers two complementary facilities:

1. **A registry** (`REGISTRY`) describing each benchmark — its scientific
   domain, a short description, the upstream source URL, and its licence.
2. **Synthetic generators** that emit data in the exact schema of the
   corresponding benchmark, so every notebook, test, and tutorial runs with no
   network access.

## Usage

```python
from datasets import list_datasets, describe, synthetic_syndrome_dataset

print(list_datasets())
print(describe("qm9").source_url)

batch = synthetic_syndrome_dataset(n_samples=1000, n_data=3, error_rate=0.1)
print(batch["syndromes"].shape)  # (1000, 2)
```

## Using the real archives

Download an upstream archive (see each dataset's `source_url`) and unpack it
into `datasets/raw/<name>/`. The directory is git-ignored so large files are
never committed. Loaders that consume the real data look in this location and
fall back to the synthetic generator when it is absent.

## Registered datasets

| Domain | Datasets |
| --- | --- |
| Circuit & compilation | QASMBench, Feynman, QUEKO |
| Quantum chemistry | QM9, ANI-1, MD17, PubChemQC |
| Materials | Materials Project, OQMD, JARVIS-DFT, SuperCon |
| Error correction | Stim-generated syndromes, hardware decoding traces |
| Cryptography | QKD experimental traces, QuNetSim simulations |

Each dataset is redistributed under its own licence; consult the upstream
source before using it in derivative work.
