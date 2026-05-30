"""Quantum cryptography analysis (Part V).

Backs ``/api/v1/crypto/key_rate``. The implementation computes asymptotic secret
key rates for the BB84 protocol, the canonical example used in the textbook's
quantum-security chapter.
"""

from __future__ import annotations

from .qkd import bb84_key_rate, binary_entropy

__all__ = ["bb84_key_rate", "binary_entropy"]
