# Capstones & Workshops — Classroom-Based Interactive Learning

> Back Matter: From reading to building

The twenty-four chapters of *AI in Quantum Technologies* develop a single,
repeated idea — replace an intractable quantum object with a learned, structured
surrogate trained on its measurable consequences — across eight domains. This
back-matter section turns that idea into practice. It collects **workshops**
(single-session, in-class activities) and **capstone projects** (multi-week,
team-based investigations) designed for the classroom, the laboratory section,
and the flipped lecture. Every activity is anchored to specific chapters, runs
against the dependency-light [`aiquantum`](../api.md) core library so it executes
offline, and is paired with an explicit assessment rubric.

## Learning objectives

After completing the activities in this section, students and instructors will be
able to:

- Translate a chapter's theory into a reproducible, version-controlled
  experiment with a baseline and a measured outcome.
- Design and defend an evaluation protocol in which any claimed quantum or
  learning advantage is quantified against a classical baseline.
- Run a collaborative, milestone-driven project that mirrors the workflow of a
  research group: hypothesis, implementation, ablation, write-up, and review.
- Apply the ethical, provenance, and reproducibility standards of Part VII to
  their own deliverables.

## How to use this section

The material is organised for two cadences:

1. **Workshops** are scoped to a single 75–120 minute session and require only
   the core library and a laptop. They suit recitation sections, lab days, and
   the active portion of a flipped lecture. Each lists prerequisites, a timed
   run-of-show, a concrete deliverable, and discussion prompts.
2. **Capstones** are scoped to 3–6 weeks of team work and culminate in a
   short paper, a reproducible repository, and an oral defence. Each lists
   milestones, deliverables, extension paths, and a grading rubric.

!!! note "Reproducibility contract"
    Every deliverable in this section must satisfy the same contract the
    repository itself enforces: fixed random seeds, a pinned environment, a
    runnable entry point, and a baseline against which results are reported.
    A result without a baseline is treated as incomplete, not merely unpolished.

A shared rubric (see [Assessment](#assessment-and-rubrics)) underlies both
cadences so that instructors can grade consistently across topics.

## Workshops

Each workshop is self-contained and maps onto the thematic
[learning paths](../tutorials.md) in the `tutorials/` directory, which provide a
ready-made `walkthrough.py` starting point.

### Workshop A — Reading a Density Matrix

| Field | Value |
| --- | --- |
| **Chapters** | 1, 4 |
| **Duration** | 75 min |
| **Prerequisites** | `aiquantum.linalg`; basic NumPy |
| **Format** | Pairs at the keyboard, instructor-led checkpoints |

**Goal.** Build intuition for the density matrix $\rho$ as the universal
description of real hardware, and for the estimators that recover it from data.

**Run-of-show.**

1. *(10 min)* Warm-up: each pair constructs a pure state, a classically mixed
   state, and an entangled state, and computes purity $\operatorname{Tr}(\rho^2)$
   and von Neumann entropy $S(\rho) = -\operatorname{Tr}(\rho\log\rho)$.
2. *(25 min)* Generate a synthetic tomography dataset and reconstruct $\rho$ from
   noisy expectation values, comparing the estimate to ground truth via fidelity.
3. *(25 min)* Vary the shot budget and plot reconstruction fidelity versus shots;
   relate the trend to the $1/\sqrt{N}$ scaling introduced in Chapter 4.
4. *(15 min)* Discussion and deliverable hand-in.

```python
import numpy as np
from datasets import synthetic_tomography_dataset
from aiquantum.linalg import purity, von_neumann_entropy

data = synthetic_tomography_dataset(n_samples=128, shots=1024, seed=0)
# `bloch` holds the true Bloch vectors; `expectations` the shot-noisy estimates.
print("loaded", len(data["expectations"]), "noisy single-qubit measurements")
```

**Deliverable.** A one-figure report: fidelity-versus-shots, with a two-sentence
explanation of the observed scaling.

**Discussion prompts.** Why does the maximally mixed state carry one bit of
entropy? What breaks if you reconstruct from too few shots, and how would you
detect that failure automatically?

### Workshop B — From Bell States to Learned Representations

| Field | Value |
| --- | --- |
| **Chapters** | 4, 16 |
| **Duration** | 90 min |
| **Prerequisites** | `aiquantum.qml`; Workshop A |
| **Format** | Pairs, with a closing baseline comparison |

**Goal.** Encode quantum measurement data as features and train a small classical
model to classify states, making the chapter's "surrogate" pattern concrete.

**Run-of-show.** Load a labelled set of single-qubit measurement records; build a
feature map; fit a kernel model from `aiquantum.qml`; and—critically—compare it
to a trivial classical baseline so the *added value* of the representation is
measured, not assumed.

**Deliverable.** A confusion matrix plus a one-paragraph statement of whether the
learned representation beats the baseline and by how much.

**Discussion prompts.** Where does the quantum data enter, and where is the model
purely classical? Under what conditions would this pipeline fail to generalise?

### Workshop C — Decoder Bake-Off

| Field | Value |
| --- | --- |
| **Chapters** | 6, 8 |
| **Duration** | 90 min |
| **Prerequisites** | `aiquantum.quantum.error_correction` |
| **Format** | Small teams competing on a held-out test set |

**Goal.** Train and compare syndrome decoders under a fixed noise model, framing
quantum error correction as a supervised learning problem.

**Run-of-show.** Generate a syndrome dataset at a chosen physical error rate;
implement a lookup-table baseline decoder; train a learned decoder; and rank
teams by logical error rate on an unseen test split.

```python
from datasets import synthetic_syndrome_dataset

train = synthetic_syndrome_dataset(n_samples=2000, error_rate=0.10, seed=1)
test = synthetic_syndrome_dataset(n_samples=500, error_rate=0.10, seed=2)
print(train["syndromes"].shape, "->", train["errors"].shape)
```

**Deliverable.** A leaderboard entry: logical error rate versus the lookup-table
baseline, with the decoder code committed and seeded.

**Discussion prompts.** Why is the *logical* error rate, not raw accuracy, the
correct figure of merit? What happens to each decoder as the physical error rate
approaches the code's threshold (Chapter 8)?

### Workshop D — Auditing a Quantum AI System

| Field | Value |
| --- | --- |
| **Chapters** | 19, 20 |
| **Duration** | 75 min |
| **Prerequisites** | None beyond Part VII reading |
| **Format** | Structured role-play and written audit |

**Goal.** Apply the governance and ethics frameworks of Part VII to a concrete
pipeline, producing a reproducibility-and-impact audit.

**Run-of-show.** Teams receive a model card and dataset card for a hypothetical
quantum-AI deployment, identify provenance gaps and misuse vectors, and draft
remediation steps using the [ethical audit tutorial](../tutorials.md) as a
template.

**Deliverable.** A completed one-page audit naming at least three concrete risks
and a mitigation for each.

**Discussion prompts.** Which risks are technical, which are social, and which are
both? What would *provenance* mean for a dataset generated on shared cloud
hardware?

## Capstone projects

Capstones are team efforts (3–4 students) that run across several weeks. Each
follows the same milestone structure so that progress is legible and comparable.

!!! tip "Milestone scaffold"
    **M1 — Proposal (Week 1).** Problem statement, chosen baseline, success
    metric, and a runnable "hello world" against the relevant `aiquantum` module.
    **M2 — Working pipeline (Week 2–3).** End-to-end run on small data with the
    baseline reproduced.
    **M3 — Investigation (Week 3–5).** Ablations, error bars, and at least one
    falsifiable claim tested.
    **M4 — Defence (Final week).** Short paper, reproducible repository, and a
    10-minute oral defence with live re-execution.

### Capstone 1 — Sample-Efficient State Tomography

- **Part / chapters.** II / 4, with techniques from 16.
- **Question.** Can a learned prior reduce the number of shots required to
  reconstruct an unknown single-qubit state to a target fidelity $F \ge 0.99$?
- **Approach.** Treat tomography as estimation under a shot budget; compare a
  maximum-likelihood baseline to a learned estimator trained on
  `synthetic_tomography_dataset`. Report fidelity as a function of shots with
  confidence intervals.
- **Baseline.** Linear inversion / least-squares reconstruction.
- **Deliverables.** Fidelity-versus-shots curves with error bars; an ablation
  over training-set size; a discussion of where the learned prior helps and where
  it injects bias.
- **Extensions.** Two-qubit states; active selection of the next measurement
  basis; robustness to a mismatched noise model (Chapter 6).

### Capstone 2 — Learned Decoders Near Threshold

- **Part / chapters.** III / 8, with noise models from 6.
- **Question.** How does a learned syndrome decoder's logical error rate compare
  to a lookup-table decoder as the physical error rate sweeps toward threshold?
- **Approach.** Sweep `error_rate` in `synthetic_syndrome_dataset`; train decoders
  at each point; plot logical-versus-physical error curves for both methods.
- **Baseline.** Minimum-weight / lookup-table decoding.
- **Deliverables.** A threshold plot, a statement of the crossover (if any) where
  learning helps, and a runtime comparison.
- **Extensions.** Larger codes; correlated noise; decoder transfer across error
  rates.

### Capstone 3 — Variational Ground States with Honest Baselines

- **Part / chapters.** IV / 10, 12, 17.
- **Question.** For a small spin Hamiltonian, how close does a variational/neural
  surrogate come to the exact ground-state energy, and at what optimisation cost?
- **Approach.** Construct $H$, obtain the exact ground energy by diagonalisation
  for reference, then minimise the energy with a parameterised model from
  `aiquantum.qchem` / `aiquantum.qml`; report the energy gap $\Delta E = E_{\text{var}} - E_0$ versus iterations.
- **Baseline.** Exact diagonalisation (small system) and a mean-field estimate.
- **Deliverables.** Convergence curves; a barren-plateau diagnostic; a sensitivity
  study over initialisation seeds.
- **Extensions.** Excited states; larger lattices via tensor-network surrogates
  (Chapter 12); noise-aware training.

### Capstone 4 — Certified Randomness and Its Audit

- **Part / chapters.** V / 13, 15, bridged to VII / 19.
- **Question.** Can a team build, *and then audit*, a certified-randomness
  pipeline end to end?
- **Approach.** Implement the protocol from the [certified randomness
  tutorial](../tutorials.md) using `aiquantum.crypto`; quantify extracted entropy;
  then apply Workshop D's audit lens to the resulting system.
- **Baseline.** A non-certified pseudo-random source, contrasted on the
  guarantees each can and cannot make.
- **Deliverables.** A working extractor, an entropy accounting, and a one-page
  ethics-and-provenance audit of the deployment.
- **Extensions.** Device-independence assumptions; failure-mode analysis;
  threat modelling for misuse.

## Assessment and rubrics

Both workshops and capstones are graded on the same five dimensions, so students
internalise a single standard of rigour. Weights below are a suggested default
for capstones; workshops typically collapse to *Correctness*, *Baseline*, and
*Communication*.

| Dimension | What it measures | Weight |
| --- | --- | --- |
| **Correctness** | Code runs from a clean checkout; results match claims. | 25% |
| **Baseline & evaluation** | A fair classical/control baseline is implemented and beaten *or* honestly reported as not beaten. | 25% |
| **Rigour** | Error bars, seeds, ablations; claims are falsifiable and tested. | 20% |
| **Reproducibility** | Pinned environment, fixed seeds, documented entry point, committed artefacts. | 15% |
| **Communication & ethics** | Clear write-up; provenance, limitations, and societal impact addressed (Part VII). | 15% |

!!! warning "The cardinal rule"
    A claimed advantage with no baseline earns no credit for *Baseline &
    evaluation*, regardless of how impressive the result appears. This mirrors the
    discipline argued throughout the book (Chapters 16, 18, 23): advantage is
    conditional and must be measured, baseline by baseline.

## Facilitation notes for instructors

- **Group quantum data live.** Generate datasets in class with a fixed seed so
  every team starts from identical data, then change one seed to surface
  variance — a fast, visceral lesson in why error bars matter.
- **Front-load the baseline.** Require the baseline before the "interesting"
  model. Teams that build the baseline first design better experiments.
- **Run the defence as re-execution.** Ask each team to re-run their pipeline
  from a clean checkout during the defence; reproducibility becomes a graded
  performance, not an afterthought.
- **Close the loop to Part VII.** Reserve the final discussion of every activity
  for impact and provenance, reinforcing that ethics is woven through the science
  rather than appended to it.

## Summary

This section operationalises the book: workshops convert single chapters into
90-minute, hands-on encounters, and capstones convert whole parts into
milestone-driven research experiences. A shared reproducibility contract and a
single rubric — anchored on the non-negotiable demand for an honest baseline —
hold the activities to the same standard the repository itself enforces. The aim
is not merely to teach what AI for quantum technologies *is*, but to give
students the habits to build, measure, and defend it.

## Further reading

- The thematic [tutorials](../tutorials.md) and [API reference](../api.md), which
  provide runnable starting points for every activity above.
- The [contributing guide](../contributing.md), whose review checklist doubles as
  a capstone acceptance criterion.
- Part VII (Chapters 19–21) for the ethics, governance, and equity standards that
  every deliverable must meet.
