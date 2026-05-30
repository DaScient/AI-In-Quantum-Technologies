# Contributing to AI in Quantum Technologies

Thank you for your interest in improving the code-first companion to
*AI in Quantum Technologies: Theory, Applications, Practice, and Society*. We
welcome contributions from the global quantum and AI communities.

## Ways to contribute

- **Report bugs** — Open a GitHub issue with a minimal reproducible example.
- **Suggest features** — Use the feature request template.
- **Submit code** — Fork → branch → pull request. All code must include tests
  and pass CI.
- **Improve documentation** — Edit files under `docs/` and submit a PR.
- **Add a dataset or model** — Follow the integration guide in `contrib/`.

We are especially interested in contributions that:

- Add support for new quantum backends (IonQ, Rigetti, QuEra, etc.).
- Provide multi-lingual notebook translations.
- Expand the ethical auditing framework.

## Development setup

```bash
git clone https://github.com/DaScient/AI-In-Quantum-Technologies.git
cd AI-In-Quantum-Technologies
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,api]"
```

## Quality gates

Every pull request must pass the following locally and in CI:

```bash
ruff check src tests datasets      # lint
ruff format --check src tests      # formatting
pytest                             # unit and API tests
```

### Coding conventions

- Target Python 3.11+. Use type hints throughout.
- Keep the core library dependency-light (`numpy`/`scipy` only); heavier
  back-ends (Qiskit, PennyLane, Cirq, PyTorch, JAX) belong in optional extras,
  notebooks, and tutorials.
- Every public function needs a docstring and at least one test.
- Web routes in `aiquantum.api` must remain thin wrappers over tested library
  functions.

## Commit and PR guidelines

- Write clear, imperative commit messages ("Add surface-code decoder").
- Reference related issues in the PR description.
- Describe the scientific motivation for non-trivial changes and cite sources.

## Code of conduct

By participating you agree to uphold a respectful, inclusive, and harassment-free
environment. Be kind, assume good faith, and credit prior work.

## Licensing of contributions

Unless stated otherwise, contributions are accepted under the repository's
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license.
