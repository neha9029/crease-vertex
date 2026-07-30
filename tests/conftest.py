"""Shared fixtures for crease-vertex tests."""

from __future__ import annotations

import pytest

from crease_vertex import Assignment


@pytest.fixture
def flat_cross_angles() -> list[float]:
    """Canonical flat degree-4 vertex at 0°/90°/180°/270°."""
    return [0.0, 90.0, 180.0, 270.0]


@pytest.fixture
def flat_cross_assignments_mv() -> list[Assignment]:
    """Valid Maekawa assignment for a degree-4 vertex: |M-V| = 2."""
    return [
        Assignment.MOUNTAIN,
        Assignment.VALLEY,
        Assignment.MOUNTAIN,
        Assignment.MOUNTAIN,
    ]
