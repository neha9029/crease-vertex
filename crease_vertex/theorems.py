"""Kawasaki and Maekawa theorem checks."""

from __future__ import annotations

from collections.abc import Sequence

from .crease import Assignment
from .results import KawasakiResult, MaekawaResult

_EXPECTED_ALTERNATING_SUM = 180.0
_EXPECTED_MAEKAWA_DIFFERENCE = 2


def check_kawasaki(
    sector_angles: Sequence[float],
    *,
    tolerance: float,
) -> KawasakiResult:
    """Check Kawasaki’s theorem on sector angles around a vertex.

    For an even number of creases (hence an even number of sectors), the
    two alternating sector sums must each equal 180° within ``tolerance``.

    Alternating sums use even indices first, then odd indices.
    """
    sectors = tuple(float(s) for s in sector_angles)
    crease_count = len(sectors)

    if crease_count < 2 or crease_count % 2 != 0:
        return KawasakiResult(
            applicable=False,
            crease_count=crease_count,
            alternating_sums=None,
            expected=_EXPECTED_ALTERNATING_SUM,
            residuals=None,
            tolerance=tolerance,
            satisfied=False,
            detail=(
                f"Kawasaki’s theorem requires an even number of creases; "
                f"got {crease_count} (odd or too few)."
            ),
        )

    even_sum = sum(sectors[i] for i in range(0, crease_count, 2))
    odd_sum = sum(sectors[i] for i in range(1, crease_count, 2))
    residuals = (
        even_sum - _EXPECTED_ALTERNATING_SUM,
        odd_sum - _EXPECTED_ALTERNATING_SUM,
    )
    satisfied = (
        abs(residuals[0]) <= tolerance and abs(residuals[1]) <= tolerance
    )

    if satisfied:
        detail = (
            f"Alternating sector sums equal {_EXPECTED_ALTERNATING_SUM}° "
            f"within {tolerance}°."
        )
    else:
        detail = (
            f"Alternating sector sums are {even_sum}° and {odd_sum}°; "
            f"expected {_EXPECTED_ALTERNATING_SUM}° ± {tolerance}°."
        )

    return KawasakiResult(
        applicable=True,
        crease_count=crease_count,
        alternating_sums=(even_sum, odd_sum),
        expected=_EXPECTED_ALTERNATING_SUM,
        residuals=residuals,
        tolerance=tolerance,
        satisfied=satisfied,
        detail=detail,
    )


def check_maekawa(
    assignments: Sequence[Assignment],
) -> MaekawaResult:
    """Check Maekawa’s theorem on mountain/valley assignments.

    Requires ``abs(mountain_count - valley_count) == 2``.
    """
    assigned = tuple(assignments)
    mountain_count = sum(1 for a in assigned if a is Assignment.MOUNTAIN)
    valley_count = sum(1 for a in assigned if a is Assignment.VALLEY)
    difference = abs(mountain_count - valley_count)
    satisfied = difference == _EXPECTED_MAEKAWA_DIFFERENCE

    if satisfied:
        detail = (
            f"Maekawa satisfied: |{mountain_count}M - {valley_count}V| = "
            f"{difference}."
        )
    else:
        detail = (
            f"Maekawa failed: |{mountain_count}M - {valley_count}V| = "
            f"{difference}; expected {_EXPECTED_MAEKAWA_DIFFERENCE}."
        )

    return MaekawaResult(
        applicable=True,
        mountain_count=mountain_count,
        valley_count=valley_count,
        difference=difference,
        expected_difference=_EXPECTED_MAEKAWA_DIFFERENCE,
        satisfied=satisfied,
        detail=detail,
        assignments=assigned,
    )
