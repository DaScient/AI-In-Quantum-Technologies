# Getting Started

## Installation

The reference library `aiquantum` targets Python 3.11+ and keeps its core
dependencies light (`numpy`, `scipy`, `pydantic`) so the science runs anywhere.

```bash
git clone https://github.com/DaScient/AI-In-Quantum-Technologies.git
cd AI-In-Quantum-Technologies

python -m venv .venv && source .venv/bin/activate
pip install -e ".[api,dev]"      # core + web API + test tooling
```

To pull in the full quantum and deep-learning back-ends used by the notebooks
(Qiskit, PennyLane, Cirq, PyTorch), install the `all` extra:

```bash
pip install -e ".[all]"
```

## Running the API

```bash
aiquantum-api                    # console script
# or
uvicorn aiquantum.api.app:app --reload
```

Interactive OpenAPI documentation is then served at
[http://localhost:8000/docs](http://localhost:8000/docs), and a liveness probe
at `/health`.

## Docker

A reproducible stack (API + Jupyter Lab + MLflow) is provided:

```bash
docker compose up -d
# API     -> http://localhost:8000
# Jupyter -> http://localhost:8888  (token: quantum)
# MLflow  -> http://localhost:5000
```

## A first computation

```python
from aiquantum.quantum import linear_inversion_tomography

# Reconstruct |+> from its Pauli expectation values <X>=1, <Y>=<Z>=0.
rho = linear_inversion_tomography({"X": 1.0}, n_qubits=1)
print(rho.round(3))
```

## Running the tests

```bash
ruff check src tests datasets
pytest
```
