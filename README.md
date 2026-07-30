# crease-vertex

A small, dependency-free Python library for analyzing a **single** origami crease vertex.

## Status

API and tests are defined first (TDD). Core theorem logic is intentionally unimplemented until the public API is approved.

## Requirements

- Python 3.11+
- pytest (dev)

## Install (editable)

```bash
python -m pip install -e ".[dev]"
```

## Scope (v0.1)

- Normalize crease angles to `[0, 360)`
- Reject duplicate directions within tolerance
- Sort creases counterclockwise
- Compute sector angles (including wraparound)
- Verify sector angles sum to 360°
- Kawasaki’s theorem (even crease count)
- Maekawa’s theorem (mountain/valley counts)
- Structured diagnostic results

Out of scope for now: multi-vertex patterns, folding simulation, SVG, FOLD files.

## Quick start (proposed)

```python
from crease_vertex import Assignment, CreaseVertex

vertex = CreaseVertex(
    [0, 90, 180, 270],
    assignments=[
        Assignment.MOUNTAIN,
        Assignment.VALLEY,
        Assignment.MOUNTAIN,
        Assignment.VALLEY,
    ],
)

report = vertex.analyze()
print(report.sector_sum.satisfied)
print(report.kawasaki.satisfied)
print(report.maekawa.satisfied)
```

## Development

```bash
pytest
```
