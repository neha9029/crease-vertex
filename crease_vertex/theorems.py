"""Kawasaki and Maekawa theorem checks (stubs until API approval)."""

from __future__ import annotations

from collections.abc import Sequence

from .crease import Assignment
from .results import KawasakiResult, MaekawaResult


def check_kawasaki(
    sector_angles: Sequence[float],
    *,
    tolerance: float,
) -> KawasakiResult:
    """Check Kawasaki’s theorem on sector angles around a vertex.

    For an even number of creases (hence an even number of sectors), the
    two alternating sector sums must each equal 180° within ``tolerance``.

    Parameters
    ----------
    sector_angles:
        Consecutive sector angles in counterclockwise order, including the
        wraparound sector. Length must equal the crease count.
    tolerance:
        Absolute angular tolerance in degrees.
    """
    raise NotImplementedError("check_kawasaki is stubbed pending API approval")


def check_maekawa(
    assignments: Sequence[Assignment],
) -> MaekawaResult:
    """Check Maekawa’s theorem on mountain/valley assignments.

    Requires ``abs(mountain_count - valley_count) == 2``.
    """
    raise NotImplementedError("check_maekawa is stubbed pending API approval")
