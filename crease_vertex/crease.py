"""Crease direction and mountain/valley assignment types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Assignment(Enum):
    """Fold assignment for a single crease."""

    MOUNTAIN = "mountain"
    VALLEY = "valley"


@dataclass(frozen=True, slots=True)
class Crease:
    """A crease leaving a vertex, given as a direction angle in degrees.

    Angles are stored as provided; :class:`CreaseVertex` is responsible for
    normalizing to ``[0, 360)`` and sorting.
    """

    angle: float
    assignment: Assignment | None = None
