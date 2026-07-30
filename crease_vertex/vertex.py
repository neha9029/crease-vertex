"""CreaseVertex: analyze a single origami crease vertex (stub)."""

from __future__ import annotations

from collections.abc import Sequence

from .crease import Assignment, Crease
from .results import (
    KawasakiResult,
    MaekawaResult,
    SectorSumResult,
    VertexAnalysisResult,
)


class CreaseVertex:
    """A single origami crease vertex defined by outgoing crease directions.

    Construction (proposed behavior)
    --------------------------------
    1. Accept angles in degrees (bare floats or :class:`Crease` objects).
    2. Optionally accept parallel ``assignments`` when angles are bare floats.
    3. Normalize every angle to ``[0, 360)``.
    4. Reject duplicate directions within ``tolerance``.
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
        ``creases`` is a sequence of floats. Ignored when each
        :class:`Crease` already carries an assignment. Must match length
        when provided.
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
        raise NotImplementedError("CreaseVertex.__init__ is stubbed pending API approval")

    @property
    def tolerance(self) -> float:
        """Absolute angular tolerance in degrees."""
        raise NotImplementedError

    @property
    def angles(self) -> tuple[float, ...]:
        """Normalized, unique, counterclockwise-sorted crease angles."""
        raise NotImplementedError

    @property
    def assignments(self) -> tuple[Assignment | None, ...]:
        """Assignments aligned with :attr:`angles` (``None`` if unset)."""
        raise NotImplementedError

    @property
    def sector_angles(self) -> tuple[float, ...]:
        """Sector angles between consecutive creases, including wraparound."""
        raise NotImplementedError

    def check_sector_sum(self) -> SectorSumResult:
        """Verify that sector angles sum to 360° within tolerance."""
        raise NotImplementedError

    def check_kawasaki(self) -> KawasakiResult:
        """Apply Kawasaki’s theorem to this vertex’s sector angles."""
        raise NotImplementedError

    def check_maekawa(self) -> MaekawaResult:
        """Apply Maekawa’s theorem to this vertex’s assignments."""
        raise NotImplementedError

    def analyze(self) -> VertexAnalysisResult:
        """Run sector-sum, Kawasaki, and Maekawa checks together."""
        raise NotImplementedError
