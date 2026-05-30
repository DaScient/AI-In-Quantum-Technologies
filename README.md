# AI in Quantum Technologies

<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg"></a>
<a href="https://dascient.github.io/ai-in-quantum-technologies"><img src="https://img.shields.io/badge/docs-mkdocs-blue"></a>
<a href="https://github.com/DaScient/ai-in-quantum/actions/workflows/tests.yml"><img src="https://github.com/DaScient/ai-in-quantum/actions/workflows/tests.yml/badge.svg"></a>
<a href="https://api.quantumai.dascient.com/docs"><img src="https://img.shields.io/website?url=https%3A%2F%2Fapi.quantumai.dascient.com%2Fhealth"></a>

> *"Do you really believe the moon is only there when you look at it?"* — Albert Einstein

## About This Repository

This repository is the living digital companion to the textbook **"AI in Quantum Technologies: Theory, Applications, Practice, and Society"** (DaScient Press Ltd., 2026). It provides a hands‑on, code‑first journey through the rapidly evolving intersection of artificial intelligence and quantum science. Inside you will find:

- **Interactive Jupyter Notebooks** for all 24 chapters
- **RESTful API** exposing AI‑driven quantum tools
- **Pre‑trained models** for quantum control, error correction, material discovery, and more
- **Curated benchmark datasets** and evaluation suites
- **Docker containers** guaranteeing reproducible research environments
- **Cloud deployment templates** for AWS, GCP, and Azure
- **Tutorials** that bridge quantum computing frameworks (Qiskit, PennyLane, Cirq) with modern deep learning (PyTorch, JAX, TensorFlow)

## Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/DaScient/ai-in-quantum.git
cd ai-in-quantum

# Create and activate conda environment
conda create -n ai-quantum python=3.11
conda activate ai-quantum

# Install the package with all quantum and ML dependencies
pip install -e .[all]

# Launch Jupyter Lab
jupyter lab
```

### Docker Quick Start

```bash
docker-compose up -d
# API available at http://localhost:8000
# Jupyter at http://localhost:8888 (token: quantum)
# MLflow tracking server at http://localhost:5000
```

## Textbook Chapters

The textbook is structured into eight parts, each building the conceptual and practical machinery required to apply AI across the quantum technology landscape. Every chapter includes a fully executable notebook that can be run locally or opened directly in Google Colab.

| Part | Chapter | Notebook |
| --- | --- | --- |
| **I: Foundations** | 1. Quantum Mechanics as Information Science | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 2. Artificial Intelligence: Paradigms for Quantum Discovery | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 3. Mathematical and Computational Toolbox | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **II: Quantum Data Across Scales** | 4. Representing Quantum States and Processes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 5. Datasets from Quantum Experiments | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 6. Noise, Decoherence, and Real‑World Imperfections | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **III: AI for Quantum Devices** | 7. Quantum Optimal Control | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 8. Quantum Error Correction & Mitigation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 9. Quantum Metrology & Sensing | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **IV: AI for Quantum Matter** | 10. Quantum Chemistry & Molecular Design | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 11. Quantum Materials Discovery | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 12. Many‑Body Physics & Tensor Networks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **V: Quantum Information & Communication** | 13. Quantum Cryptography & Security | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 14. Quantum Networks & Repeaters | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 15. Quantum Algorithms & Complexity | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **VI: Quantum Machine Learning & Hybrid Systems** | 16. Quantum Machine Learning Fundamentals | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 17. Variational Quantum Algorithms | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 18. Quantum‑Classical Hybrid Computing | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **VII: Ethics, Policy, and Societal Impact** | 19. Ethical Dimensions of Quantum AI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 20. Governance & Standards for Quantum Technologies | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 21. Workforce, Equity, and Geopolitics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| **VIII: Horizons** | 22. Co‑Evolution of AI and Quantum Hardware | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 23. Open Questions and Fundamental Limits | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |
| | 24. Toward a Quantum‑Native Intelligence | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/) |

> All chapters are then exported to a single `.docx` file for manuscript processing by DaScient Press, Ltd.

## API Endpoints

A production‑ready FastAPI service exposes state‑of‑the‑art AI models tailored to quantum science. The interactive documentation is available at `/docs` once the server is running.

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/quantum/state_tomography` | POST | Reconstruct quantum state from measurement outcomes |
| `/api/v1/quantum/process_tomography` | POST | Characterise unknown quantum processes |
| `/api/v1/quantum/optimal_control` | POST | Generate optimal pulse sequences for gate operations |
| `/api/v1/quantum/error_decode` | POST | Decode syndrome measurements for error correction |
| `/api/v1/quantum/circuit_optimize` | POST | Compress and optimise quantum circuit depth |
| `/api/v1/qchem/ground_state` | POST | Predict molecular ground state energies |
| `/api/v1/qchem/excited_states` | POST | Compute optical spectra using ML‑enhanced methods |
| `/api/v1/materials/crystal_generation` | POST | Inverse design of crystal structures with desired properties |
| `/api/v1/materials/superconductor` | POST | Predict superconducting critical temperatures |
| `/api/v1/qml/kernel` | POST | Compute quantum kernel matrices for classification |
| `/api/v1/qml/train` | POST | Train a hybrid quantum‑classical model |
| `/api/v1/crypto/key_rate` | POST | Estimate secret key rate for QKD protocols |
| `/api/v1/metrology/sensitivity` | POST | Optimise probe states for quantum sensing |
| `/api/v1/simulate/noise_model` | POST | Learn a device noise model from calibration data |

## Pre-trained Models Available

All models are hosted on Hugging Face under the `dascient` organisation. They can be loaded with a few lines of code using the `transformers`, `pennylane`, or `torch` ecosystems.

| Model | Description | Parameters | Download |
| --- | --- | --- | --- |
| Q‑BERT | Quantum‑adapted BERT for gate sequence tokenisation | 110M | [Link](https://huggingface.co/dascient) |
| ErrorFormer | Transformer for surface code error decoding | 230M | [Link](https://huggingface.co/dascient) |
| MolQNet | Molecular ground state prediction with SE(3) equivariance | 340M | [Link](https://huggingface.co/dascient) |
| CrysDiff | Diffusion model for crystal structure generation | 450M | [Link](https://huggingface.co/dascient) |
| Q‑GPT | Generative pre‑trained transformer for quantum circuit synthesis | 1.2B | [Link](https://huggingface.co/dascient) |
| SensNet | Graph neural network for quantum sensor placement | 85M | [Link](https://huggingface.co/dascient) |
| QKD‑Flow | Normalising flow for quantum channel parameter estimation | 175M | [Link](https://huggingface.co/dascient) |

## Benchmark Datasets

The repository includes ready‑to‑use dataloaders for the following curated datasets. All are pre‑processed and documented in the `/datasets` directory.

- **Circuit & Compilation:** QASMBench, Feynman, QUEKO, IBM Qiskit runtime workloads
- **Quantum Control & Calibration:** QDataSet (gate calibration), Q-CTRL Boulder Opal benchmarks
- **Quantum Chemistry:** QM9, ANI‑1, MD17, PubChemQC
- **Materials:** Materials Project, OQMD, JARVIS‑DFT, SuperCon
- **Error Correction:** Stim‑generated syndrome datasets, IBM hardware decoding traces
- **Quantum Key Distribution:** Waks‑Group QKD experimental traces, Qunetsim simulations
- **Quantum Optics:** Photonic Boson Sampling benchmarks, Perceval‑generated photon counts

## Interactive Learning Paths

In addition to the chapter notebooks, the `/tutorials` folder contains thematic learning paths that cut across multiple chapters:

1. **"From Bell States to Transformers"** – A complete walk‑through of quantum state classification with deep learning.
2. **"Designing a Superconducting Qubit with AI"** – Inverse design tutorial using a pre‑trained diffusion model.
3. **"Quantum Error Correction Decoder Challenge"** – Build and submit your own ML decoder; leaderboard included.
4. **"Certified Quantum Randomness"** – Verify quantum advantage with AI‑powered statistical tests.
5. **"Ethical Audit of a Quantum AI System"** – Apply the textbook's ethics framework to a real API model.

## Contributing

We welcome contributions from the global quantum and AI communities. Please see `CONTRIBUTING.md` for detailed guidelines.

- **Report bugs:** Open a GitHub issue with a minimal reproducible example.
- **Suggest features:** Use the feature request template.
- **Submit code:** Fork → branch → pull request. All code must include tests and pass CI.
- **Improve documentation:** Edit files in `/docs/source/` and submit a PR.
- **Add a dataset or model:** Follow the `integration_guide.md` in the `/contrib` folder.

We are especially interested in contributions that:

- Add support for new quantum backends (IonQ, Rigetti, QuEra, etc.)
- Provide multi‑lingual notebook translations
- Expand the ethical auditing framework

## Citation

```bibtex
@book{tadaya2026aiquantum,
    title     = {AI in Quantum Technologies: Theory, Applications, Practice, and Society},
    author    = {Tadaya, Don D.M.},
    year      = {2026},
    publisher = {DaScient Press},
    series    = {DaScient Intelligence Academy Textbook Series},
    library_no = {178847474773666374859402992856},
    isbn      = {TBD}
}
```

## License

This work is licensed under a Creative Commons Attribution‑NonCommercial‑ShareAlike 4.0 International License. You are free to share and adapt the material under the same terms, provided you give appropriate credit. Commercial licensing (e.g., for corporate training, proprietary product integration) is available — please contact commercial@dascient.com.

## Acknowledgments

- DaScient Intelligence Academy for conceiving the textbook and open‑source initiative.
- IBM Quantum, Google Quantum AI, Xanadu, and QuEra for providing hardware access and simulators used in the notebooks.
- Qiskit, PennyLane, and Cirq communities for outstanding software ecosystems.
- Hugging Face for hosting all pre‑trained models.
- Contributors: Over 30 quantum physicists, ML engineers, and educators who refined the manuscripts and code.

## Contact

- **Technical Support:** support@dascient.com
- **API Access:** quantumapi@dascient.com
- **Textbook & Academic Inquiries:** press@dascient.com
- **LinkedIn:** https://linkedin.com/company/DaScient
