# Datasets

The repository ships a lightweight dataset layer (`datasets/`) that combines a
**registry** of the external benchmarks referenced in the textbook with
**synthetic generators** that emit data in each benchmark's schema. This keeps
the repository small while guaranteeing that every notebook and test runs
offline.

```python
from datasets import list_datasets, describe, synthetic_syndrome_dataset

list_datasets()
# ['materials_project', 'qasmbench', 'qkd_traces', 'qm9', 'stim_syndromes', 'supercon']

describe("qm9").source_url
# 'http://quantum-machine.org/datasets/'

batch = synthetic_syndrome_dataset(n_samples=1000, n_data=3, error_rate=0.1)
batch["syndromes"].shape   # (1000, 2)
```

## Registered benchmarks

| Domain | Datasets |
| --- | --- |
| Circuit & compilation | QASMBench, Feynman, QUEKO, IBM Qiskit runtime workloads |
| Quantum control & calibration | QDataSet, Q-CTRL Boulder Opal benchmarks |
| Quantum chemistry | QM9, ANI-1, MD17, PubChemQC |
| Materials | Materials Project, OQMD, JARVIS-DFT, SuperCon |
| Error correction | Stim-generated syndromes, hardware decoding traces |
| Quantum key distribution | QKD experimental traces, QuNetSim simulations |
| Quantum optics | Boson-sampling benchmarks, Perceval photon counts |

## Using the real archives

Download an upstream archive (see each dataset's `source_url`) and unpack it into
`datasets/raw/<name>/`. That directory is git-ignored, so large files are never
committed. See [`datasets/README.md`](https://github.com/DaScient/AI-In-Quantum-Technologies/blob/main/datasets/README.md)
for details.
