"""Exceptions raised by crease-vertex during construction and validation."""

from __future__ import annotations


class CreaseVertexError(Exception):
    """Base error for crease-vertex."""


class DuplicateCreaseError(CreaseVertexError):
    """Raised when two crease directions coincide within tolerance."""


class AssignmentCountError(CreaseVertexError):
    """Raised when mountain/valley assignments do not match crease count."""


class EmptyCreaseError(CreaseVertexError):
    """Raised when fewer than two crease directions are provided."""
