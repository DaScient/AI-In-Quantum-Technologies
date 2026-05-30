# syntax=docker/dockerfile:1
#
# Reproducible runtime for the AI-in-Quantum-Technologies API and notebooks.
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# System libraries required by the scientific Python stack.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install the package first (better layer caching).
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --upgrade pip && pip install ".[api]"

# Copy the remaining project assets.
COPY datasets ./datasets
COPY tutorials ./tutorials
COPY docs ./docs

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status == 200 else 1)"

CMD ["uvicorn", "aiquantum.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
