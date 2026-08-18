# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-18

### Added

- `CreaseVertex` class: accepts crease directions in degrees (floats or
  `Crease` objects), normalizes to `[0, 360)`, rejects duplicates within a
  configurable tolerance (including wraparound), sorts counterclockwise,
  and computes sector angles including the wraparound sector.
- Sector-sum check verifying sector angles total 360° within tolerance.
- Kawasaki's theorem check for an even number of creases (alternating
  sector sums each equal 180° within tolerance).
- Maekawa's theorem check for mountain/valley assignments
  (`|mountains - valleys| == 2`).
- Structured diagnostic results (`SectorSumResult`, `KawasakiResult`,
  `MaekawaResult`, `VertexAnalysisResult`) instead of bare booleans.
- Standalone helpers `check_kawasaki` and `check_maekawa`.
- Typed package (`py.typed`), zero runtime dependencies, Python 3.11+.

[Unreleased]: https://github.com/neha9029/crease-vertex/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/neha9029/crease-vertex/releases/tag/v0.1.0
