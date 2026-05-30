# Interactive Learning Paths

Beyond the per-chapter notebooks, the `tutorials/` directory contains thematic
learning paths that cut across multiple chapters. Each tutorial is a
self-contained, reproducible study that combines prose, code against the
`aiquantum` library, and exercises.

| # | Tutorial | Chapters | Folder |
| --- | --- | --- | --- |
| 1 | From Bell States to Transformers | 4, 16 | [`tutorials/01_bell_states_to_transformers/`](https://github.com/DaScient/AI-In-Quantum-Technologies/tree/main/tutorials/01_bell_states_to_transformers) |
| 2 | Designing a Superconducting Qubit with AI | 7, 11 | [`tutorials/02_designing_a_superconducting_qubit/`](https://github.com/DaScient/AI-In-Quantum-Technologies/tree/main/tutorials/02_designing_a_superconducting_qubit) |
| 3 | Quantum Error Correction Decoder Challenge | 8 | [`tutorials/03_qec_decoder_challenge/`](https://github.com/DaScient/AI-In-Quantum-Technologies/tree/main/tutorials/03_qec_decoder_challenge) |
| 4 | Certified Quantum Randomness | 13, 15 | [`tutorials/04_certified_quantum_randomness/`](https://github.com/DaScient/AI-In-Quantum-Technologies/tree/main/tutorials/04_certified_quantum_randomness) |
| 5 | Ethical Audit of a Quantum AI System | 19, 20 | [`tutorials/05_ethical_audit/`](https://github.com/DaScient/AI-In-Quantum-Technologies/tree/main/tutorials/05_ethical_audit) |

## Running a tutorial

Each tutorial folder contains a `README.md` describing the path and a runnable
`walkthrough.py` that uses only the core library, so it executes offline:

```bash
python tutorials/03_qec_decoder_challenge/walkthrough.py
```
