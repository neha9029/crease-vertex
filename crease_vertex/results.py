"""Structured diagnostic results for vertex checks."""

from __future__ import annotations

from dataclasses import dataclass

from .crease import Assignment


@dataclass(frozen=True, slots=True)
class SectorSumResult:
    """Result of summing sector angles around the vertex."""

    sector_angles: tuple[float, ...]
    total: float
    expected: float
    residual: float
    tolerance: float
    satisfied: bool
    detail: str


@dataclass(frozen=True, slots=True)
class KawasakiResult:
    """Result of Kawasaki’s theorem check.

    Kawasaki applies only when the crease count is even and at least 2.
    When not applicable, ``alternating_sums`` / ``residuals`` are ``None``
    and ``satisfied`` is ``False``.
    """

    applicable: bool
    crease_count: int
    alternating_sums: tuple[float, float] | None
    expected: float
    residuals: tuple[float, float] | None
    tolerance: float
    satisfied: bool
    detail: str


@dataclass(frozen=True, slots=True)
class MaekawaResult:
    """Result of Maekawa’s theorem check.

    Maekawa requires a mountain/valley assignment on every crease.
    When not applicable, counts may still be reported and ``satisfied``
    is ``False``.
    """

    applicable: bool
    mountain_count: int
    valley_count: int
    difference: int
    expected_difference: int
    satisfied: bool
    detail: str
    assignments: tuple[Assignment, ...]


@dataclass(frozen=True, slots=True)
class VertexAnalysisResult:
    """Aggregate report for a single crease vertex."""

    angles: tuple[float, ...]
    sector_sum: SectorSumResult
    kawasaki: KawasakiResult
    maekawa: MaekawaResult
