"""FastAPI application exposing AI-driven quantum tools.

Run locally with::

    aiquantum-api            # console script
    uvicorn aiquantum.api.app:app --reload

Interactive documentation is served at ``/docs``. Each route is a thin,
validated wrapper around the corresponding :mod:`aiquantum` library function so
that the science is testable independently of the web layer.
"""

from __future__ import annotations

import numpy as np
from fastapi import FastAPI, HTTPException

from .. import __version__
from ..crypto import bb84_key_rate
from ..linalg import purity, von_neumann_entropy
from ..materials import allen_dynes_tc, generate_crystal, mcmillan_tc
from ..metrology import heisenberg_limit, optimal_phase_sensitivity, standard_quantum_limit
from ..qchem import coulomb_matrix, predict_excitation_spectrum
from ..qchem.ground_state import sorted_eigenvalue_descriptor
from ..qml import quantum_kernel_matrix, train_hybrid_model
from ..quantum import (
    decode_repetition_code,
    grape_pulse,
    linear_inversion_process_tomography,
    linear_inversion_tomography,
    optimize_circuit,
)
from ..quantum.circuit_optimize import circuit_depth
from ..quantum.state_tomography import n_qubit_paulis
from ..simulate import average_gate_infidelity, learn_pauli_channel
from . import schemas

app = FastAPI(
    title="AI in Quantum Technologies API",
    version=__version__,
    description=(
        "Production-ready AI models for quantum science, the companion service "
        "to the DaScient Press textbook *AI in Quantum Technologies*."
    ),
)


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    """Service banner."""
    return {
        "name": "AI in Quantum Technologies API",
        "version": __version__,
        "docs": "/docs",
    }


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Liveness probe used by deployment health checks."""
    return {"status": "ok"}


# --- Quantum devices ---------------------------------------------------------


@app.post(
    "/api/v1/quantum/state_tomography",
    response_model=schemas.StateTomographyResponse,
    tags=["quantum"],
)
def state_tomography(req: schemas.StateTomographyRequest) -> schemas.StateTomographyResponse:
    """Reconstruct a quantum state from Pauli expectation values."""
    try:
        rho = linear_inversion_tomography(req.expectations, req.n_qubits, project=req.project)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.StateTomographyResponse(
        density_matrix_real=rho.real.tolist(),
        density_matrix_imag=rho.imag.tolist(),
        purity=purity(rho),
        von_neumann_entropy=von_neumann_entropy(rho),
    )


@app.post(
    "/api/v1/quantum/process_tomography",
    response_model=schemas.ProcessTomographyResponse,
    tags=["quantum"],
)
def process_tomography(req: schemas.ProcessTomographyRequest) -> schemas.ProcessTomographyResponse:
    """Characterise an unknown quantum process via its Pauli transfer matrix."""
    try:
        ptm = linear_inversion_process_tomography(req.transfer_data, req.n_qubits)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    labels = list(n_qubit_paulis(req.n_qubits).keys())
    return schemas.ProcessTomographyResponse(
        pauli_transfer_matrix=ptm.tolist(), labels=labels
    )


@app.post(
    "/api/v1/quantum/optimal_control",
    response_model=schemas.OptimalControlResponse,
    tags=["quantum"],
)
def optimal_control(req: schemas.OptimalControlRequest) -> schemas.OptimalControlResponse:
    """Generate an optimal control pulse approximating a target unitary."""
    target = np.asarray(req.target_real, dtype=float) + 1j * np.asarray(req.target_imag, dtype=float)
    if target.ndim != 2 or target.shape[0] != target.shape[1]:
        raise HTTPException(status_code=422, detail="target must be a square matrix")
    result = grape_pulse(
        target,
        n_steps=req.n_steps,
        dt=req.dt,
        iterations=req.iterations,
        learning_rate=req.learning_rate,
    )
    return schemas.OptimalControlResponse(
        controls=result.controls.tolist(),
        fidelity=result.fidelity,
        iterations_run=len(result.history),
    )


@app.post(
    "/api/v1/quantum/error_decode",
    response_model=schemas.ErrorDecodeResponse,
    tags=["quantum"],
)
def error_decode(req: schemas.ErrorDecodeRequest) -> schemas.ErrorDecodeResponse:
    """Decode a repetition-code syndrome into a recovery operation."""
    try:
        recovery = decode_repetition_code(req.syndrome, req.n_data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.ErrorDecodeResponse(
        recovery=recovery.tolist(), weight=int(recovery.sum())
    )


@app.post(
    "/api/v1/quantum/circuit_optimize",
    response_model=schemas.CircuitOptimizeResponse,
    tags=["quantum"],
)
def circuit_optimize(req: schemas.CircuitOptimizeRequest) -> schemas.CircuitOptimizeResponse:
    """Compress and optimise quantum circuit depth."""
    optimized = optimize_circuit(req.circuit)
    return schemas.CircuitOptimizeResponse(
        optimized_circuit=optimized,
        original_gate_count=len(req.circuit),
        optimized_gate_count=len(optimized),
        original_depth=circuit_depth(req.circuit),
        optimized_depth=circuit_depth(optimized),
    )


# --- Quantum chemistry -------------------------------------------------------


@app.post(
    "/api/v1/qchem/ground_state",
    response_model=schemas.GroundStateResponse,
    tags=["qchem"],
)
def ground_state(req: schemas.GroundStateRequest) -> schemas.GroundStateResponse:
    """Featurise a molecule for ground-state energy prediction."""
    charges = np.asarray(req.charges, dtype=float)
    coords = np.asarray(req.coordinates, dtype=float)
    if coords.shape != (len(charges), 3):
        raise HTTPException(status_code=422, detail="coordinates must be n x 3 matching charges")
    descriptor = sorted_eigenvalue_descriptor(charges, coords, req.descriptor_size)
    return schemas.GroundStateResponse(
        descriptor=descriptor.tolist(),
        coulomb_matrix=coulomb_matrix(charges, coords).tolist(),
    )


@app.post(
    "/api/v1/qchem/excited_states",
    response_model=schemas.ExcitedStatesResponse,
    tags=["qchem"],
)
def excited_states(req: schemas.ExcitedStatesRequest) -> schemas.ExcitedStatesResponse:
    """Compute a broadened optical absorption spectrum."""
    try:
        grid, intensity = predict_excitation_spectrum(
            np.asarray(req.excitation_energies),
            np.asarray(req.oscillator_strengths),
            grid=np.linspace(
                min(req.excitation_energies) - 1.0,
                max(req.excitation_energies) + 1.0,
                req.n_points,
            ),
            broadening=req.broadening,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.ExcitedStatesResponse(
        energy_grid=grid.tolist(), intensity=intensity.tolist()
    )


# --- Materials ---------------------------------------------------------------


@app.post(
    "/api/v1/materials/crystal_generation",
    response_model=schemas.CrystalGenerationResponse,
    tags=["materials"],
)
def crystal_generation(req: schemas.CrystalGenerationRequest) -> schemas.CrystalGenerationResponse:
    """Inverse-design a crystal structure with a target density."""
    structure = generate_crystal(req.species, target_density=req.target_density, seed=req.seed)
    return schemas.CrystalGenerationResponse(
        lattice=structure.lattice.tolist(),
        species=structure.species,
        frac_coords=structure.frac_coords.tolist(),
        volume=structure.volume,
        density=structure.density,
    )


@app.post(
    "/api/v1/materials/superconductor",
    response_model=schemas.SuperconductorResponse,
    tags=["materials"],
)
def superconductor(req: schemas.SuperconductorRequest) -> schemas.SuperconductorResponse:
    """Predict a superconducting critical temperature."""
    estimator = allen_dynes_tc if req.method == "allen_dynes" else mcmillan_tc
    tc = estimator(req.lambda_ep, req.omega_log, req.mu_star)
    return schemas.SuperconductorResponse(critical_temperature_kelvin=tc, method=req.method)


# --- Quantum machine learning ------------------------------------------------


@app.post("/api/v1/qml/kernel", response_model=schemas.KernelResponse, tags=["qml"])
def qml_kernel(req: schemas.KernelRequest) -> schemas.KernelResponse:
    """Compute a quantum kernel (Gram) matrix."""
    try:
        kernel = quantum_kernel_matrix(
            np.asarray(req.x_a, dtype=float),
            None if req.x_b is None else np.asarray(req.x_b, dtype=float),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.KernelResponse(kernel_matrix=kernel.tolist())


@app.post("/api/v1/qml/train", response_model=schemas.QMLTrainResponse, tags=["qml"])
def qml_train(req: schemas.QMLTrainRequest) -> schemas.QMLTrainResponse:
    """Train a hybrid quantum-classical kernel classifier."""
    summary = train_hybrid_model(
        np.asarray(req.x, dtype=float),
        np.asarray(req.y, dtype=float),
        regularization=req.regularization,
    )
    return schemas.QMLTrainResponse(
        n_samples=summary["n_samples"],
        n_features=summary["n_features"],
        regularization=summary["regularization"],
        train_accuracy=summary["train_accuracy"],
    )


# --- Cryptography, metrology, simulation ------------------------------------


@app.post("/api/v1/crypto/key_rate", response_model=schemas.KeyRateResponse, tags=["crypto"])
def key_rate(req: schemas.KeyRateRequest) -> schemas.KeyRateResponse:
    """Estimate the secret key rate for the BB84 QKD protocol."""
    try:
        rate = bb84_key_rate(
            req.qber,
            phase_error=req.phase_error,
            sifting_efficiency=req.sifting_efficiency,
            reconciliation_efficiency=req.reconciliation_efficiency,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.KeyRateResponse(secret_key_rate=rate, secure=rate > 0.0)


@app.post(
    "/api/v1/metrology/sensitivity",
    response_model=schemas.SensitivityResponse,
    tags=["metrology"],
)
def sensitivity(req: schemas.SensitivityRequest) -> schemas.SensitivityResponse:
    """Report phase-estimation sensitivity limits for quantum sensing."""
    achievable = None
    if req.quantum_fisher_information is not None:
        achievable = optimal_phase_sensitivity(req.quantum_fisher_information, req.repetitions)
    return schemas.SensitivityResponse(
        standard_quantum_limit=standard_quantum_limit(req.n_probes, req.repetitions),
        heisenberg_limit=heisenberg_limit(req.n_probes, req.repetitions),
        achievable_sensitivity=achievable,
    )


@app.post(
    "/api/v1/simulate/noise_model",
    response_model=schemas.NoiseModelResponse,
    tags=["simulate"],
)
def noise_model(req: schemas.NoiseModelRequest) -> schemas.NoiseModelResponse:
    """Learn a single-qubit Pauli noise model from calibration data."""
    try:
        probs = learn_pauli_channel(req.pauli_fidelities)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return schemas.NoiseModelResponse(
        pauli_error_probabilities=probs,
        average_gate_infidelity=average_gate_infidelity(probs),
    )


def run() -> None:  # pragma: no cover - thin CLI wrapper
    """Console-script entry point: launch the API with uvicorn."""
    import uvicorn

    uvicorn.run("aiquantum.api.app:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":  # pragma: no cover
    run()
