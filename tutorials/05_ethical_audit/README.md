# Tutorial 5 — Ethical Audit of a Quantum-Enhanced Model

**Chapters:** 19 (Ethical Dimensions of Quantum AI) · 20 (Governance and Standards)

A model can be accurate in aggregate yet fail specific groups. This path audits a
quantum-kernel classifier for *performance disparity* across two cohorts, turning
the ethical principles of Chapters 19–20 into a concrete, reproducible measurement.

## What you will learn

- How to measure subgroup accuracy disparity, a basic fairness diagnostic.
- Why aggregate accuracy can hide group-level failures.
- How to make an audit reproducible and reportable (Chapters 19–20).

## Run it

```bash
python tutorials/05_ethical_audit/walkthrough.py
```

The script trains a `HybridKernelClassifier`, evaluates it separately on two
cohorts, and reports per-cohort accuracy plus the disparity gap. Treat a large gap
as a flag to investigate data representativeness before deployment.
