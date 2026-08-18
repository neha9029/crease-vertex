# crease-vertex

[![CI](https://github.com/neha9029/crease-vertex/actions/workflows/ci.yml/badge.svg)](https://github.com/neha9029/crease-vertex/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A small, dependency-free Python library for analyzing a **single** origami crease vertex: sector geometry, Kawasaki's theorem, and Maekawa's theorem, with structured diagnostics.

## Install

```bash
pip install crease-vertex
```

Or from source:

```bash
git clone https://github.com/neha9029/crease-vertex.git
cd crease-vertex
python -m pip install -e ".[dev]"
```

Requires Python 3.11+. No runtime dependencies.

## Quick start

```python
from crease_vertex import Assignment, CreaseVertex

vertex = CreaseVertex(
    [0, 90, 180, 270],
    assignments=[
        Assignment.MOUNTAIN,
        Assignment.VALLEY,
        Assignment.MOUNTAIN,
        Assignment.MOUNTAIN,
    ],
)

report = vertex.analyze()
print(report.sector_sum.satisfied)  # True — sectors total 360°
print(report.kawasaki.satisfied)    # True — alternating sums are 180°/180°
print(report.maekawa.satisfied)     # True — |3 mountains − 1 valley| == 2
print(report.kawasaki.detail)       # human-readable explanation
```

Angles are given in degrees and may be negative or above 360; they are
normalized to `[0, 360)` and sorted counterclockwise. Duplicate directions
(within `tolerance`, including across the 0°/360° boundary) raise
`DuplicateCreaseError`.

## API overview

Construction:

```python
CreaseVertex(creases, *, assignments=None, tolerance=1e-6)
```

- `creases` — a sequence of angles in degrees, or of `Crease` objects
  (which can carry their own `Assignment`)
- `assignments` — optional mountain/valley labels, parallel to `creases`
  when angles are given as floats
- `tolerance` — degrees; used for duplicate detection and theorem residuals

Properties: `angles`, `assignments`, `sector_angles`, `tolerance`

Checks return structured results, not bare booleans:

| Method | Returns | Key fields |
|--------|---------|------------|
| `check_sector_sum()` | `SectorSumResult` | `total`, `residual`, `satisfied`, `detail` |
| `check_kawasaki()` | `KawasakiResult` | `applicable`, `alternating_sums`, `residuals`, `satisfied` |
| `check_maekawa()` | `MaekawaResult` | `mountain_count`, `valley_count`, `difference`, `satisfied` |
| `analyze()` | `VertexAnalysisResult` | all of the above |

Standalone helpers `check_kawasaki(sector_angles, *, tolerance)` and
`check_maekawa(assignments)` are also exported.

### The theorems, briefly

- **Kawasaki**: at a flat-foldable vertex with an even number of creases,
  the alternating sums of sector angles each equal 180°. Odd crease counts
  are reported as `applicable=False`.
- **Maekawa**: at a flat-foldable vertex, the number of mountain and valley
  creases differs by exactly 2. Requires an assignment on every crease.

## Scope

Single-vertex analysis only. Multi-vertex crease patterns, folding
simulation, SVG parsing, and FOLD file support are intentionally out of
scope for now.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes are tracked in
[CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
