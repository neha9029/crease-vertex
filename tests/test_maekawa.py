"""Tests for Maekawa’s theorem diagnostics."""

from __future__ import annotations

import pytest

from crease_vertex import (
    Assignment,
    Crease,
    CreaseVertex,
    MaekawaResult,
    check_maekawa,
)


M = Assignment.MOUNTAIN
V = Assignment.VALLEY


class TestMaekawaValid:
    def test_three_mountain_one_valley(self, flat_cross_angles: list[float]) -> None:
        result = CreaseVertex(
            flat_cross_angles, assignments=[M, M, M, V]
        ).check_maekawa()
        assert isinstance(result, MaekawaResult)
        assert result.applicable is True
        assert result.mountain_count == 3
        assert result.valley_count == 1
        assert result.difference == 2
        assert result.expected_difference == 2
        assert result.satisfied is True

    def test_three_valley_one_mountain(self, flat_cross_angles: list[float]) -> None:
        result = CreaseVertex(
            flat_cross_angles, assignments=[V, V, V, M]
        ).check_maekawa()
        assert result.mountain_count == 1
        assert result.valley_count == 3
        assert result.difference == 2
        assert result.satisfied is True

    def test_degree_six_valid_counts(self) -> None:
        angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
        # |4-2| = 2
        assignments = [M, M, M, M, V, V]
        result = CreaseVertex(angles, assignments=assignments).check_maekawa()
        assert result.satisfied is True
        assert result.difference == 2


class TestMaekawaInvalid:
    def test_equal_mountain_valley_fails(self, flat_cross_angles: list[float]) -> None:
        result = CreaseVertex(
            flat_cross_angles, assignments=[M, V, M, V]
        ).check_maekawa()
        assert result.applicable is True
        assert result.mountain_count == 2
        assert result.valley_count == 2
        assert result.difference == 0
        assert result.satisfied is False

    def test_all_mountain_fails(self, flat_cross_angles: list[float]) -> None:
        result = CreaseVertex(
            flat_cross_angles, assignments=[M, M, M, M]
        ).check_maekawa()
        assert result.difference == 4
        assert result.satisfied is False

    def test_difference_of_one_impossible_for_even_degree_but_reported(
        self,
    ) -> None:
        # Odd crease count can yield |M-V|=1; Maekawa still requires == 2.
        angles = [0.0, 120.0, 240.0]
        result = CreaseVertex(angles, assignments=[M, M, V]).check_maekawa()
        assert result.difference == 1
        assert result.satisfied is False


class TestMaekawaApplicability:
    def test_missing_assignments_not_applicable(
        self, flat_cross_angles: list[float]
    ) -> None:
        result = CreaseVertex(flat_cross_angles).check_maekawa()
        assert result.applicable is False
        assert result.satisfied is False
        assert "assign" in result.detail.lower()

    def test_partial_assignments_via_crease_objects_not_applicable(self) -> None:
        result = CreaseVertex(
            [
                Crease(0.0, M),
                Crease(90.0, V),
                Crease(180.0, None),
                Crease(270.0, M),
            ]
        ).check_maekawa()
        assert result.applicable is False
        assert result.satisfied is False


class TestMaekawaStandaloneHelper:
    def test_helper_valid(self) -> None:
        result = check_maekawa([M, M, M, V])
        assert result.satisfied is True
        assert result.difference == 2

    def test_helper_invalid(self) -> None:
        result = check_maekawa([M, V, M, V])
        assert result.satisfied is False

    def test_helper_preserves_assignment_tuple(self) -> None:
        assignments = (M, V, M, M)
        result = check_maekawa(assignments)
        assert result.assignments == assignments

    def test_analyze_includes_maekawa(
        self,
        flat_cross_angles: list[float],
        flat_cross_assignments_mv: list[Assignment],
    ) -> None:
        report = CreaseVertex(
            flat_cross_angles, assignments=flat_cross_assignments_mv
        ).analyze()
        assert report.maekawa.satisfied is True
        assert report.maekawa.difference == 2
