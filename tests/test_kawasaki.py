"""Tests for Kawasaki’s theorem diagnostics."""

from __future__ import annotations

import pytest

from crease_vertex import CreaseVertex, KawasakiResult, check_kawasaki


class TestKawasakiValid:
    def test_flat_cross_satisfies_kawasaki(self, flat_cross_angles: list[float]) -> None:
        vertex = CreaseVertex(flat_cross_angles)
        result = vertex.check_kawasaki()
        assert isinstance(result, KawasakiResult)
        assert result.applicable is True
        assert result.crease_count == 4
        assert result.expected == 180.0
        assert result.alternating_sums is not None
        assert result.alternating_sums[0] == pytest.approx(180.0)
        assert result.alternating_sums[1] == pytest.approx(180.0)
        assert result.residuals is not None
        assert result.residuals[0] == pytest.approx(0.0)
        assert result.residuals[1] == pytest.approx(0.0)
        assert result.satisfied is True

    def test_degree_six_equal_sectors(self) -> None:
        angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
        result = CreaseVertex(angles).check_kawasaki()
        assert result.applicable is True
        assert result.satisfied is True
        assert result.alternating_sums == pytest.approx((180.0, 180.0))

    def test_uneven_but_valid_alternating_sums(self) -> None:
        # Sectors: 40, 140, 140, 40 -> alternating 40+140=180, 140+40=180
        angles = [0.0, 40.0, 180.0, 320.0]
        vertex = CreaseVertex(angles)
        assert vertex.sector_angles == pytest.approx((40.0, 140.0, 140.0, 40.0))
        result = vertex.check_kawasaki()
        assert result.satisfied is True
        assert result.alternating_sums == pytest.approx((180.0, 180.0))


class TestKawasakiInvalid:
    def test_alternating_sums_not_180(self) -> None:
        # Sectors: 60, 100, 60, 140 -> 60+60=120, 100+140=240
        angles = [0.0, 60.0, 160.0, 220.0]
        vertex = CreaseVertex(angles)
        assert vertex.sector_angles == pytest.approx((60.0, 100.0, 60.0, 140.0))
        result = vertex.check_kawasaki()
        assert result.applicable is True
        assert result.satisfied is False
        assert result.alternating_sums == pytest.approx((120.0, 240.0))
        assert result.residuals is not None
        assert result.residuals[0] == pytest.approx(-60.0)
        assert result.residuals[1] == pytest.approx(60.0)

    def test_near_miss_outside_tolerance(self) -> None:
        # Sectors ≈ 90.1, 89.9, 90.1, 89.9 -> alternating ≈ 180.2 / 179.8
        angles = [0.0, 90.1, 180.0, 270.1]
        result = CreaseVertex(angles, tolerance=1e-6).check_kawasaki()
        assert result.satisfied is False

    def test_near_miss_within_tolerance(self) -> None:
        angles = [0.0, 90.1, 180.0, 270.1]
        result = CreaseVertex(angles, tolerance=0.25).check_kawasaki()
        assert result.applicable is True
        assert result.satisfied is True


class TestKawasakiApplicability:
    def test_odd_crease_count_not_applicable(self) -> None:
        result = CreaseVertex([0.0, 120.0, 240.0]).check_kawasaki()
        assert result.applicable is False
        assert result.crease_count == 3
        assert result.alternating_sums is None
        assert result.residuals is None
        assert result.satisfied is False
        assert "even" in result.detail.lower() or "odd" in result.detail.lower()

    def test_degree_two_is_applicable(self) -> None:
        # Two opposite creases: sectors 180, 180
        result = CreaseVertex([0.0, 180.0]).check_kawasaki()
        assert result.applicable is True
        assert result.satisfied is True
        assert result.alternating_sums == pytest.approx((180.0, 180.0))


class TestKawasakiStandaloneHelper:
    def test_helper_matches_vertex_method(self, flat_cross_angles: list[float]) -> None:
        vertex = CreaseVertex(flat_cross_angles)
        via_vertex = vertex.check_kawasaki()
        via_helper = check_kawasaki(vertex.sector_angles, tolerance=vertex.tolerance)
        assert via_helper.satisfied == via_vertex.satisfied
        assert via_helper.alternating_sums == pytest.approx(via_vertex.alternating_sums)

    def test_helper_reports_detail_string(self) -> None:
        result = check_kawasaki((90.0, 90.0, 90.0, 90.0), tolerance=1e-6)
        assert isinstance(result.detail, str)
        assert result.detail
