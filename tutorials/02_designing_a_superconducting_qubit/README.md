# Tutorial 2 — Designing a Superconducting Qubit with AI

**Chapters:** 7 (Quantum Optimal Control) · 11 (Quantum Materials Discovery)

Designing a qubit spans two scales: the *material* that hosts it and the *control*
that operates it. This path treats both — screening a superconductor by its
predicted critical temperature, then synthesising a high-fidelity gate pulse for
the resulting qubit with GRAPE.

## What you will learn

- How the Allen–Dynes formula screens candidate superconductors (Chapter 11).
- How GRAPE optimises a control pulse to realise a target gate (Chapter 7).
- How materials and control decisions compose into a single design workflow.

## Run it

```bash
python tutorials/02_designing_a_superconducting_qubit/walkthrough.py
```

The script ranks a small set of electron–phonon parameter sets by critical
temperature, then runs GRAPE to synthesise an X gate for the chosen qubit,
reporting the achieved fidelity. Extend it with the `CrysDiff` generative model
to propose the candidate structures.
