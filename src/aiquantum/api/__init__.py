"""HTTP API for the AI-in-Quantum library (FastAPI)."""

from __future__ import annotations

__all__ = ["app", "run"]


def __getattr__(name: str):  # lazy import so the package imports without FastAPI
    if name in {"app", "run"}:
        from .app import app, run

        return {"app": app, "run": run}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
