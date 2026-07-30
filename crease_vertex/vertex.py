"""CreaseVertex: analyze a single origami crease vertex."""

from __future__ import annotations

import math
from collections.abc import Sequence

from .crease import Assignment, Crease
from .exceptions import (
    AssignmentCountError,
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

_FULL_TURN = 360.0


def _normalize_angle(angle: float) -> float:
    """Map an angle in degrees to the half-open interval [0, 360)."""
    return angle % _FULL_TURN


def _circular_separation(a: float, b: float) -> float:
    """Smallest arc distance in degrees between two angles on the circle."""
    diff = abs(a - b) % _FULL_TURN
    return min(diff, _FULL_TURN - diff)


class CreaseVertex:
    """A single origami crease vertex defined by outgoing crease directions.

    Construction
    ------------
    1. Accept angles in degrees (bare floats or :class:`Crease` objects).
    2. Optionally accept parallel ``assignments`` when angles are bare floats.
    3. Normalize every angle to ``[0, 360)``.
    4. Reject duplicate directions within ``tolerance`` (closed; circular).
    5. Sort creases counterclockwise (increasing angle).
    6. Precompute sector angles between consecutive creases, including the
       wraparound sector from the last crease back to the first.

    Parameters
    ----------
    creases:
        Either a sequence of angles in degrees, or a sequence of
        :class:`Crease` objects.
    assignments:
        Optional mountain/valley labels aligned with ``creases`` when
        ``creases`` is a sequence of floats. Ignored when ``creases`` is a
        sequence of :class:`Crease` objects. Must match length when provided.
    tolerance:
        Absolute angular tolerance in degrees used for duplicate detection
        and for theorem residual comparisons.
    """

    def __init__(
        self,
        creases: Sequence[float] | Sequence[Crease],
        *,
        assignments: Sequence[Assignment] | None = None,
        tolerance: float = 1e-6,
    ) -> None:
        if tolerance < 0:
            raise ValueError("tolerance must be non-negative")

        angles, assigns = self._coerce_inputs(creases, assignments)
        if len(angles) < 2:
            raise EmptyCreaseError(
                "A crease vertex requires at least two crease directions."
            )

        normalized = [_normalize_angle(a) for a in angles]
        paired = sorted(
            zip(normalized, assigns, strict=True),
            key=lambda item: item[0],
        )
        self._reject_duplicates(paired, tolerance)

        self._tolerance = float(tolerance)
        self._angles = tuple(angle for angle, _ in paired)
        self._assignments = tuple(assignment for _, assignment in paired)
        self._sector_angles = self._compute_sectors(self._angles)

    @staticmethod
    def _coerce_inputs(
        creases: Sequence[float] | Sequence[Crease],
        assignments: Sequence[Assignment] | None,
    ) -> tuple[list[float], list[Assignment | None]]:
        if not creases:
            return [], []

        if all(isinstance(c, Crease) for c in creases):
            crease_objs = [c for c in creases if isinstance(c, Crease)]
            angles = [float(c.angle) for c in crease_objs]
            assigns: list[Assignment | None] = [c.assignment for c in crease_objs]
            return angles, assigns

        if any(isinstance(c, Crease) for c in creases):
            raise TypeError(
                "creases must be all angles (float) or all Crease objects, not mixed."
            )

        angles = [float(a) for a in creases]  # type: ignore[arg-type]
        if assignments is None:
            return angles, [None] * len(angles)

        if len(assignments) != len(angles):
            raise AssignmentCountError(
                f"Expected {len(angles)} assignments, got {len(assignments)}."
            )
        return angles, list(assignments)

    @staticmethod
    def _reject_duplicates(
        paired: list[tuple[float, Assignment | None]],
        tolerance: float,
    ) -> None:
        n = len(paired)
        if n < 2:
            return

        for i in range(n - 1):
            a = paired[i][0]
            b = paired[i + 1][0]
            if _circular_separation(a, b) <= tolerance:
                raise DuplicateCreaseError(
                    f"Duplicate crease directions within {tolerance}°: "
                    f"{a}° and {b}°."
                )

        first = paired[0][0]
        last = paired[-1][0]
        if _circular_separation(first, last) <= tolerance:
            raise DuplicateCreaseError(
                f"Duplicate crease directions within {tolerance}° "
                f"(wraparound): {last}° and {first}°."
            )

    @staticmethod
    def _compute_sectors(angles: tuple[float, ...]) -> tuple[float, ...]:
        sectors = [angles[i + 1] - angles[i] for i in range(len(angles) - 1)]
        sectors.append((angles[0] + _FULL_TURN) - angles[-1])
        return tuple(sectors)

    @property
    def tolerance(self) -> float:
        """Absolute angular tolerance in degrees."""
        return self._tolerance

    @property
    def angles(self) -> tuple[float, ...]:
        """Normalized, unique, counterclockwise-sorted crease angles."""
        return self._angles

    @property
    def assignments(self) -> tuple[Assignment | None, ...]:
        """Assignments aligned with :attr:`angles` (`None` if unset)."""
        return self._assignments

    @property
    def sector_angles(self) -> tuple[float, ...]:
        """Sector angles between consecutive creases, including wraparound."""
        return self._sector_angles

    def check_sector_sum(self) -> SectorSumResult:
        """Verify that sector angles sum to 360° within tolerance."""
        total = math.fsum(self._sector_angles)
        residual = total - _FULL_TURN
        satisfied = abs(residual) <= self._tolerance
        if satisfied:
            detail = f"Sector angles sum to {total}° (expected {_FULL_TURN}°)."
        else:
            detail = (
                f"Sector angles sum to {total}°; expected {_FULL_TURN}° "
                f"± {self._tolerance}°."
            )
        return SectorSumResult(
            sector_angles=self._sector_angles,
            total=total,
            expected=_FULL_TURN,
            residual=residual,
            tolerance=self._tolerance,
            satisfied=satisfied,
            detail=detail,
        )

    def check_kawasaki(self) -> KawasakiResult:
        """Apply Kawasaki’s theorem to this vertex’s sector angles."""
        return check_kawasaki(self._sector_angles, tolerance=self._tolerance)

    def check_maekawa(self) -> MaekawaResult:
        """Apply Maekawa’s theorem to this vertex’s assignments."""
        if any(a is None for a in self._assignments):
            present = tuple(a for a in self._assignments if a is not None)
            mountain_count = sum(1 for a in present if a is Assignment.MOUNTAIN)
            valley_count = sum(1 for a in present if a is Assignment.VALLEY)
            return MaekawaResult(
                applicable=False,
                mountain_count=mountain_count,
                valley_count=valley_count,
                difference=abs(mountain_count - valley_count),
                expected_difference=2,
                satisfied=False,
                detail=(
                    "Maekawa’s theorem requires a mountain/valley assignment "
                    "on every crease."
                ),
                assignments=present,
            )

        complete: tuple[Assignment, ...] = tuple(
            a for a in self._assignments if a is not None
        )
        return check_maekawa(complete)

    def analyze(self) -> VertexAnalysisResult:
        """Run sector-sum, Kawasaki, and Maekawa checks together."""
        return VertexAnalysisResult(
            angles=self._angles,
            sector_sum=self.check_sector_sum(),
            kawasaki=self.check_kawasaki(),
            maekawa=self.check_maekawa(),
        )
