"""Shared fixtures for all tests."""

import pytest
from datetime import datetime


@pytest.fixture
def fixed_datetime():
    """A fixed datetime for deterministic tests."""
    return datetime(2026, 1, 1, 12, 0, 0)