# Tutorial 1 — From Bell States to Transformers

**Chapters:** 4 (Representing Quantum States) · 16 (Quantum ML Fundamentals)

This learning path connects the representation of quantum states to their
classification with machine learning. We start from the four Bell states, encode
single-qubit measurement statistics as classical features, and use a quantum
kernel to separate two state families — a complete, miniature walk-through of
quantum state classification.

## What you will learn

- How an informationally complete set of Pauli expectations identifies a state
  (Chapter 4).
- How a quantum feature map turns those features into a kernel (Chapter 16).
- Why the geometry of the feature space, not its mere size, determines
  separability.

## Run it

```bash
python tutorials/01_bell_states_to_transformers/walkthrough.py
```

The script reconstructs states by linear inversion, builds a quantum kernel over
their Bloch features, and reports the kernel structure that makes the classes
linearly separable in feature space. Extend it by replacing the kernel classifier
with a transformer trained on longer measurement records.
