"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aiquantum.api.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
