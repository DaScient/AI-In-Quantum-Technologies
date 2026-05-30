"""Pydantic request/response schemas for the AI-in-Quantum API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StateTomographyRequest(BaseModel):
    n_qubits: int = Field(..., ge=1, le=4, description="Number of qubits.")
    expectations: dict[str, float] = Field(
        ..., description="Pauli-string expectation values in [-1, 1]."
    )
    project: bool = Field(True, description="Project onto physical density matrices.")


class StateTomographyResponse(BaseModel):
    density_matrix_real: list[list[float]]
    density_matrix_imag: list[list[float]]
    purity: float
    von_neumann_entropy: float


class ProcessTomographyRequest(BaseModel):
    n_qubits: int = Field(..., ge=1, le=3)
    transfer_data: dict[str, dict[str, float]] = Field(
        ..., description="transfer_data[input_pauli][output_pauli] = value."
    )


class ProcessTomographyResponse(BaseModel):
    pauli_transfer_matrix: list[list[float]]
    labels: list[str]


class OptimalControlRequest(BaseModel):
    target_real: list[list[float]] = Field(..., description="Real part of target unitary.")
    target_imag: list[list[float]] = Field(..., description="Imaginary part of target unitary.")
    n_steps: int = Field(20, ge=1, le=200)
    dt: float = Field(0.1, gt=0)
    iterations: int = Field(200, ge=1, le=2000)
    learning_rate: float = Field(1.0, gt=0)


class OptimalControlResponse(BaseModel):
    controls: list[list[float]]
    fidelity: float
    iterations_run: int


class ErrorDecodeRequest(BaseModel):
    syndrome: list[int] = Field(..., description="Binary syndrome bits.")
    n_data: int = Field(..., ge=2, description="Number of data qubits.")


class ErrorDecodeResponse(BaseModel):
    recovery: list[int]
    weight: int


class CircuitOptimizeRequest(BaseModel):
    circuit: list[dict] = Field(..., description="Ordered list of gate dictionaries.")


class CircuitOptimizeResponse(BaseModel):
    optimized_circuit: list[dict]
    original_gate_count: int
    optimized_gate_count: int
    original_depth: int
    optimized_depth: int


class GroundStateRequest(BaseModel):
    charges: list[float] = Field(..., description="Nuclear charges Z_i.")
    coordinates: list[list[float]] = Field(..., description="n x 3 coordinates (angstrom).")
    descriptor_size: int = Field(8, ge=1, le=64)


class GroundStateResponse(BaseModel):
    descriptor: list[float]
    coulomb_matrix: list[list[float]]


class ExcitedStatesRequest(BaseModel):
    excitation_energies: list[float]
    oscillator_strengths: list[float]
    broadening: float = Field(0.1, gt=0)
    n_points: int = Field(256, ge=16, le=4096)


class ExcitedStatesResponse(BaseModel):
    energy_grid: list[float]
    intensity: list[float]


class CrystalGenerationRequest(BaseModel):
    species: list[str] = Field(..., min_length=1)
    target_density: float | None = Field(None, gt=0)
    seed: int | None = 0


class CrystalGenerationResponse(BaseModel):
    lattice: list[list[float]]
    species: list[str]
    frac_coords: list[list[float]]
    volume: float
    density: float


class SuperconductorRequest(BaseModel):
    lambda_ep: float = Field(..., gt=0, description="Electron-phonon coupling.")
    omega_log: float = Field(..., gt=0, description="Log-average phonon frequency (K).")
    mu_star: float = Field(0.1, ge=0, le=0.3)
    method: str = Field("allen_dynes", pattern="^(allen_dynes|mcmillan)$")


class SuperconductorResponse(BaseModel):
    critical_temperature_kelvin: float
    method: str


class KernelRequest(BaseModel):
    x_a: list[list[float]]
    x_b: list[list[float]] | None = None


class KernelResponse(BaseModel):
    kernel_matrix: list[list[float]]


class QMLTrainRequest(BaseModel):
    x: list[list[float]]
    y: list[float]
    regularization: float = Field(1e-3, gt=0)


class QMLTrainResponse(BaseModel):
    n_samples: int
    n_features: int
    regularization: float
    train_accuracy: float


class KeyRateRequest(BaseModel):
    qber: float = Field(..., ge=0, le=0.5)
    phase_error: float | None = Field(None, ge=0, le=0.5)
    sifting_efficiency: float = Field(0.5, gt=0, le=1)
    reconciliation_efficiency: float = Field(1.0, ge=1)


class KeyRateResponse(BaseModel):
    secret_key_rate: float
    secure: bool


class SensitivityRequest(BaseModel):
    n_probes: int = Field(..., ge=1)
    repetitions: int = Field(1, ge=1)
    quantum_fisher_information: float | None = Field(None, gt=0)


class SensitivityResponse(BaseModel):
    standard_quantum_limit: float
    heisenberg_limit: float
    achievable_sensitivity: float | None = None


class NoiseModelRequest(BaseModel):
    pauli_fidelities: dict[str, float] = Field(
        ..., description="Measured Pauli fidelities with keys X, Y, Z."
    )


class NoiseModelResponse(BaseModel):
    pauli_error_probabilities: dict[str, float]
    average_gate_infidelity: float
