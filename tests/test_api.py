"""End-to-end tests for the FastAPI service."""

from __future__ import annotations


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_banner(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


def test_state_tomography_endpoint(client):
    response = client.post(
        "/api/v1/quantum/state_tomography",
        json={"n_qubits": 1, "expectations": {"Z": 1.0}},
    )
    assert response.status_code == 200
    body = response.json()
    assert abs(body["density_matrix_real"][0][0] - 1.0) < 1e-6
    assert abs(body["purity"] - 1.0) < 1e-6


def test_state_tomography_validation(client):
    response = client.post(
        "/api/v1/quantum/state_tomography",
        json={"n_qubits": 1, "expectations": {"Z": 5.0}},
    )
    assert response.status_code == 422


def test_optimal_control_endpoint(client):
    response = client.post(
        "/api/v1/quantum/optimal_control",
        json={
            "target_real": [[0.0, 1.0], [1.0, 0.0]],
            "target_imag": [[0.0, 0.0], [0.0, 0.0]],
            "n_steps": 20,
            "dt": 0.2,
            "iterations": 300,
        },
    )
    assert response.status_code == 200
    assert response.json()["fidelity"] > 0.95


def test_error_decode_endpoint(client):
    response = client.post(
        "/api/v1/quantum/error_decode",
        json={"syndrome": [1, 1], "n_data": 3},
    )
    assert response.status_code == 200
    assert response.json()["weight"] == 1


def test_circuit_optimize_endpoint(client):
    response = client.post(
        "/api/v1/quantum/circuit_optimize",
        json={"circuit": [{"gate": "H", "qubits": [0]}, {"gate": "H", "qubits": [0]}]},
    )
    assert response.status_code == 200
    assert response.json()["optimized_gate_count"] == 0


def test_superconductor_endpoint(client):
    response = client.post(
        "/api/v1/materials/superconductor",
        json={"lambda_ep": 0.8, "omega_log": 400.0, "mu_star": 0.1},
    )
    assert response.status_code == 200
    assert response.json()["critical_temperature_kelvin"] > 0


def test_crystal_generation_endpoint(client):
    response = client.post(
        "/api/v1/materials/crystal_generation",
        json={"species": ["Cu"], "target_density": 8.96},
    )
    assert response.status_code == 200
    assert abs(response.json()["density"] - 8.96) < 0.1


def test_qml_kernel_endpoint(client):
    response = client.post(
        "/api/v1/qml/kernel",
        json={"x_a": [[0.0], [0.0]]},
    )
    assert response.status_code == 200
    assert abs(response.json()["kernel_matrix"][0][1] - 1.0) < 1e-9


def test_qml_train_endpoint(client):
    response = client.post(
        "/api/v1/qml/train",
        json={"x": [[0.0], [0.1], [1.5], [1.6]], "y": [0, 0, 1, 1]},
    )
    assert response.status_code == 200
    assert response.json()["train_accuracy"] >= 0.5


def test_key_rate_endpoint(client):
    response = client.post("/api/v1/crypto/key_rate", json={"qber": 0.02})
    assert response.status_code == 200
    body = response.json()
    assert body["secure"] is True
    assert body["secret_key_rate"] > 0


def test_sensitivity_endpoint(client):
    response = client.post(
        "/api/v1/metrology/sensitivity",
        json={"n_probes": 16, "repetitions": 1, "quantum_fisher_information": 256.0},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["heisenberg_limit"] < body["standard_quantum_limit"]
    assert body["achievable_sensitivity"] is not None


def test_noise_model_endpoint(client):
    response = client.post(
        "/api/v1/simulate/noise_model",
        json={"pauli_fidelities": {"X": 0.98, "Y": 0.98, "Z": 0.99}},
    )
    assert response.status_code == 200
    probs = response.json()["pauli_error_probabilities"]
    assert abs(sum(probs.values()) - 1.0) < 1e-9


def test_ground_state_endpoint(client):
    response = client.post(
        "/api/v1/qchem/ground_state",
        json={
            "charges": [1.0, 1.0],
            "coordinates": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.74]],
            "descriptor_size": 4,
        },
    )
    assert response.status_code == 200
    assert len(response.json()["descriptor"]) == 4


def test_excited_states_endpoint(client):
    response = client.post(
        "/api/v1/qchem/excited_states",
        json={"excitation_energies": [2.0, 4.0], "oscillator_strengths": [1.0, 0.5]},
    )
    assert response.status_code == 200
    assert len(response.json()["energy_grid"]) == 256


def test_process_tomography_endpoint(client):
    response = client.post(
        "/api/v1/quantum/process_tomography",
        json={"n_qubits": 1, "transfer_data": {"X": {"X": 1.0}}},
    )
    assert response.status_code == 200
    assert response.json()["labels"][0] == "I"
