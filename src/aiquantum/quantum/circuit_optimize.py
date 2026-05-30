"""Lightweight peephole optimisation of quantum circuits.

Circuits are represented as ordered lists of gate dictionaries::

    {"gate": "H", "qubits": [0]}
    {"gate": "RZ", "qubits": [1], "param": 0.3}

The optimiser applies local rewrite rules that preserve the unitary while
reducing depth: cancellation of adjacent self-inverse gates (``H H``, ``X X``,
``CNOT CNOT`` on the same qubits), fusion of consecutive rotations about the
same axis, and removal of zero-angle rotations. It is the classical baseline for
the learned ``Q-GPT`` compiler discussed in the textbook.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

_SELF_INVERSE = {"H", "X", "Y", "Z", "CNOT", "CX", "CZ", "SWAP"}
_ROTATIONS = {"RX", "RY", "RZ"}


def _same_target(a: dict, b: dict) -> bool:
    return a.get("gate") == b.get("gate") and a.get("qubits") == b.get("qubits")


def optimize_circuit(circuit: Sequence[dict], atol: float = 1e-9) -> list[dict]:
    """Return a logically equivalent circuit with reduced gate count.

    Parameters
    ----------
    circuit:
        Sequence of gate dictionaries (see module docstring).
    atol:
        Angle tolerance below which a rotation is treated as identity.

    Returns
    -------
    list[dict]
        The optimised circuit.
    """
    gates = [dict(g) for g in circuit]
    changed = True
    while changed:
        changed = False
        output: list[dict] = []
        i = 0
        while i < len(gates):
            current = gates[i]
            name = current.get("gate")

            # Drop near-zero rotations.
            if name in _ROTATIONS and abs(_wrap_angle(current.get("param", 0.0))) < atol:
                changed = True
                i += 1
                continue

            if i + 1 < len(gates):
                nxt = gates[i + 1]
                # Cancel adjacent self-inverse gates on identical targets.
                if name in _SELF_INVERSE and _same_target(current, nxt):
                    changed = True
                    i += 2
                    continue
                # Fuse consecutive rotations about the same axis and qubit.
                if (
                    name in _ROTATIONS
                    and nxt.get("gate") == name
                    and current.get("qubits") == nxt.get("qubits")
                ):
                    fused = _wrap_angle(current.get("param", 0.0) + nxt.get("param", 0.0))
                    changed = True
                    if abs(fused) >= atol:
                        output.append({"gate": name, "qubits": current["qubits"], "param": fused})
                    i += 2
                    continue

            output.append(current)
            i += 1
        gates = output
    return gates


def circuit_depth(circuit: Sequence[dict]) -> int:
    """Return the circuit depth accounting for parallelism across qubits."""
    layer_for_qubit: dict[int, int] = {}
    depth = 0
    for gate in circuit:
        qubits = gate.get("qubits", [])
        start = max((layer_for_qubit.get(q, 0) for q in qubits), default=0)
        for q in qubits:
            layer_for_qubit[q] = start + 1
        depth = max(depth, start + 1)
    return depth


def _wrap_angle(theta: float) -> float:
    """Wrap an angle into ``(-pi, pi]``."""
    wrapped = (float(theta) + math.pi) % (2 * math.pi) - math.pi
    if wrapped <= -math.pi:
        wrapped += 2 * math.pi
    return wrapped
