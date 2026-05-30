# API Reference

The `aiquantum` package is organised into domain sub-packages that mirror the
parts of the textbook and the public REST endpoints.

## REST endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/quantum/state_tomography` | POST | Reconstruct a quantum state from measurement outcomes |
| `/api/v1/quantum/process_tomography` | POST | Characterise an unknown quantum process |
| `/api/v1/quantum/optimal_control` | POST | Generate optimal pulse sequences for gate operations |
| `/api/v1/quantum/error_decode` | POST | Decode syndrome measurements for error correction |
| `/api/v1/quantum/circuit_optimize` | POST | Compress and optimise quantum circuit depth |
| `/api/v1/qchem/ground_state` | POST | Featurise a molecule for ground-state energy prediction |
| `/api/v1/qchem/excited_states` | POST | Compute a broadened optical spectrum |
| `/api/v1/materials/crystal_generation` | POST | Inverse-design a crystal with target density |
| `/api/v1/materials/superconductor` | POST | Predict superconducting critical temperatures |
| `/api/v1/qml/kernel` | POST | Compute quantum kernel matrices |
| `/api/v1/qml/train` | POST | Train a hybrid quantum-classical model |
| `/api/v1/crypto/key_rate` | POST | Estimate the secret key rate for QKD |
| `/api/v1/metrology/sensitivity` | POST | Phase-estimation sensitivity limits |
| `/api/v1/simulate/noise_model` | POST | Learn a device noise model from calibration data |

## Library reference

::: aiquantum.linalg

::: aiquantum.quantum

::: aiquantum.qchem

::: aiquantum.materials

::: aiquantum.qml

::: aiquantum.crypto

::: aiquantum.metrology

::: aiquantum.simulate
