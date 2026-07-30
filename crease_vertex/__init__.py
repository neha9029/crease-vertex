"""crease-vertex: analyze a single origami crease vertex.

Public API
----------
Construction
    ``CreaseVertex(creases, *, assignments=None, tolerance=1e-6)``
    Accepts ``Sequence[float]`` or ``Sequence[Crease]``. Normalizes angles
    to ``[0, 360)``, rejects duplicates within ``tolerance``, sorts
    counterclockwise, and computes sector angles including wraparound.

Inspection
    ``angles``, ``assignments``, ``sector_angles``, ``tolerance``

Checks (structured diagnostics, not bare booleans)
    ``check_sector_sum()`` -> ``SectorSumResult``
    ``check_kawasaki()`` -> ``KawasakiResult``
    ``check_maekawa()`` -> ``MaekawaResult``
    ``analyze()`` -> ``VertexAnalysisResult``

Standalone theorem helpers
    ``check_kawasaki(sector_angles, *, tolerance)``
    ``check_maekawa(assignments)``

Exceptions
    ``CreaseVertexError``, ``DuplicateCreaseError``,
    ``AssignmentCountError``, ``EmptyCreaseError``
"""

from __future__ import annotations

from .crease import Assignment, Crease
from .exceptions import (
    AssignmentCountError,
    CreaseVertexError,
    DuplicateCreaseError,
    EmptyCreaseError,
)
from .results import (
    KawasakiResult,
    MaekawaResult,
    SectorSumResult,
    VertexAnalysisResult,
)
from .theorems import check_kawasaki, check_maekawa
from .vertex import CreaseVertex

__all__ = [
    "Assignment",
    "AssignmentCountError",
    "Crease",
    "CreaseVertex",
    "CreaseVertexError",
    "DuplicateCreaseError",
    "EmptyCreaseError",
    "KawasakiResult",
    "MaekawaResult",
    "SectorSumResult",
    "VertexAnalysisResult",
    "check_kawasaki",
    "check_maekawa",
]

__version__ = "0.1.0"
