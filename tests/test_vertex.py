"""Tests for CreaseVertex construction, normalization, sectors, and diagnostics."""

from __future__ import annotations

import math

import pytest

from crease_vertex import (
    Assignment,
    AssignmentCountError,
    Crease,
    CreaseVertex,
    DuplicateCreaseError,
    EmptyCreaseError,
    SectorSumResult,
    VertexAnalysisResult,
)


class TestNormalizationAndSorting:
    def test_normalizes_negative_and_large_angles(self) -> None:
        # -45 -> 315, 450 -> 90; canonical order is sorted in [0, 360)
        vertex = CreaseVertex([-45.0, 450.0, 180.0, 270.0])
        assert vertex.angles == (90.0, 180.0, 270.0, 315.0)

    def test_normalizes_exact_360_to_zero(self) -> None:
        vertex = CreaseVertex([90.0, 180.0, 270.0, 360.0])
        assert vertex.angles == (0.0, 90.0, 180.0, 270.0)

    def test_sorts_counterclockwise_from_arbitrary_input_order(
        self, flat_cross_angles: list[float]
    ) -> None:
        shuffled = [270.0, 0.0, 180.0, 90.0]
        vertex = CreaseVertex(shuffled)
        assert vertex.angles == tuple(sorted(a % 360.0 for a in flat_cross_angles))

    def test_accepts_crease_objects(self) -> None:
        vertex = CreaseVertex(
            [
                Crease(270.0, Assignment.MOUNTAIN),
                Crease(0.0, Assignment.VALLEY),
                Crease(180.0, Assignment.MOUNTAIN),
                Crease(90.0, Assignment.MOUNTAIN),
            ]
        )
        assert vertex.angles == (0.0, 90.0, 180.0, 270.0)
        assert vertex.assignments == (
            Assignment.VALLEY,
            Assignment.MOUNTAIN,
            Assignment.MOUNTAIN,
            Assignment.MOUNTAIN,
        )


class TestDuplicateRejection:
    def test_rejects_exact_duplicate_angles(self) -> None:
        with pytest.raises(DuplicateCreaseError):
            CreaseVertex([0.0, 90.0, 90.0, 180.0])

    def test_rejects_360_and_0_as_duplicates(self) -> None:
        with pytest.raises(DuplicateCreaseError):
            CreaseVertex([0.0, 90.0, 180.0, 360.0])

    def test_rejects_near_duplicates_within_tolerance(self) -> None:
        with pytest.raises(DuplicateCreaseError):
            CreaseVertex([0.0, 90.0, 180.0, 270.0, 0.0 + 1e-9], tolerance=1e-6)

    def test_allows_near_angles_outside_tolerance(self) -> None:
        vertex = CreaseVertex([0.0, 1.0, 180.0, 181.0], tolerance=1e-6)
        assert len(vertex.angles) == 4

    def test_rejects_wraparound_near_duplicates(self) -> None:
        """Wraparound duplicates: 0.1° and 359.9° are 0.2° apart on the circle."""
        with pytest.raises(DuplicateCreaseError):
            CreaseVertex([0.1, 90.0, 180.0, 359.9], tolerance=0.25)

    def test_configurable_tolerance_boundary(self) -> None:
        # Separation is exactly 0.5°; strict < or <= is implementation-defined,
        # but equal-to-tolerance must be treated as a duplicate (closed tolerance).
        with pytest.raises(DuplicateCreaseError):
            CreaseVertex([0.0, 0.5, 180.0, 180.5], tolerance=0.5)


class TestSectorAngles:
    def test_equal_sectors_for_flat_cross(self, flat_cross_angles: list[float]) -> None:
        vertex = CreaseVertex(flat_cross_angles)
        assert vertex.sector_angles == (90.0, 90.0, 90.0, 90.0)

    def test_includes_wraparound_sector(self) -> None:
        vertex = CreaseVertex([10.0, 100.0, 200.0])
        # Sectors: 90, 100, and wraparound 170 (from 200 -> 370/10)
        assert len(vertex.sector_angles) == 3
        assert vertex.sector_angles[0] == pytest.approx(90.0)
        assert vertex.sector_angles[1] == pytest.approx(100.0)
        assert vertex.sector_angles[2] == pytest.approx(170.0)

    def test_uneven_sectors(self) -> None:
        vertex = CreaseVertex([0.0, 60.0, 180.0, 270.0])
        assert vertex.sector_angles == pytest.approx((60.0, 120.0, 90.0, 90.0))

    def test_sector_count_matches_crease_count(self) -> None:
        angles = [0.0, 40.0, 100.0, 200.0, 300.0]
        vertex = CreaseVertex(angles)
        assert len(vertex.sector_angles) == len(vertex.angles)


class TestSectorSum:
    def test_sector_sum_satisfied_for_valid_vertex(
        self, flat_cross_angles: list[float]
    ) -> None:
        vertex = CreaseVertex(flat_cross_angles)
        result = vertex.check_sector_sum()
        assert isinstance(result, SectorSumResult)
        assert result.expected == 360.0
        assert result.total == pytest.approx(360.0)
        assert result.residual == pytest.approx(0.0)
        assert result.satisfied is True

    def test_sector_sum_always_360_for_constructed_vertex(self) -> None:
        """Any well-formed circular partition of the plane sums to 360°."""
        vertex = CreaseVertex([0.0, 1.0, 2.0, 179.0, 181.0, 359.0])
        result = vertex.check_sector_sum()
        assert result.total == pytest.approx(360.0, abs=vertex.tolerance)
        assert result.satisfied is True

    def test_floating_point_near_360(self) -> None:
        # Angles that can accumulate float error in naive summation.
        angles = [0.0, 120.0000000001, 240.0000000002]
        vertex = CreaseVertex(angles, tolerance=1e-6)
        result = vertex.check_sector_sum()
        assert result.satisfied is True
        assert abs(result.residual) <= vertex.tolerance


class TestConstructionErrors:
    def test_rejects_empty_input(self) -> None:
        with pytest.raises(EmptyCreaseError):
            CreaseVertex([])

    def test_rejects_single_crease(self) -> None:
        with pytest.raises(EmptyCreaseError):
            CreaseVertex([0.0])

    def test_assignment_count_mismatch_raises(self) -> None:
        with pytest.raises(AssignmentCountError):
            CreaseVertex(
                [0.0, 90.0, 180.0, 270.0],
                assignments=[Assignment.MOUNTAIN, Assignment.VALLEY],
            )

    def test_assignments_reordered_with_angles(self) -> None:
        vertex = CreaseVertex(
            [270.0, 0.0, 180.0, 90.0],
            assignments=[
                Assignment.MOUNTAIN,  # 270
                Assignment.VALLEY,  # 0
                Assignment.MOUNTAIN,  # 180
                Assignment.VALLEY,  # 90
            ],
        )
        assert vertex.angles == (0.0, 90.0, 180.0, 270.0)
        assert vertex.assignments == (
            Assignment.VALLEY,
            Assignment.VALLEY,
            Assignment.MOUNTAIN,
            Assignment.MOUNTAIN,
        )


class TestAnalyze:
    def test_analyze_returns_aggregate_report(
        self,
        flat_cross_angles: list[float],
        flat_cross_assignments_mv: list[Assignment],
    ) -> None:
        vertex = CreaseVertex(
            flat_cross_angles, assignments=flat_cross_assignments_mv
        )
        report = vertex.analyze()
        assert isinstance(report, VertexAnalysisResult)
        assert report.angles == vertex.angles
        assert report.sector_sum.satisfied is True
        assert report.kawasaki.satisfied is True
        assert report.maekawa.satisfied is True

    def test_tolerance_is_exposed(self) -> None:
        vertex = CreaseVertex([0.0, 120.0, 240.0], tolerance=1e-4)
        assert vertex.tolerance == 1e-4


class TestFloatingPointBoundary:
    def test_angles_just_below_360(self) -> None:
        vertex = CreaseVertex([0.0, 120.0, 239.9999999999], tolerance=1e-6)
        assert all(0.0 <= a < 360.0 for a in vertex.angles)
        assert math.fsum(vertex.sector_angles) == pytest.approx(360.0, abs=1e-6)

    def test_very_small_positive_angle(self) -> None:
        vertex = CreaseVertex([1e-12, 120.0, 240.0], tolerance=1e-15)
        assert vertex.angles[0] == pytest.approx(1e-12)
