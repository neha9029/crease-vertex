# crease-vertex

A small, dependency-free Python library for analyzing a **single** origami crease vertex.

## Requirements

- Python 3.11+
- pytest (dev)

## Install

```bash
python -m pip install -e ".[dev]"
```

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
assert report.sector_sum.satisfied
assert report.kawasaki.satisfied
assert report.maekawa.satisfied
```

## Features

- Normalize crease angles to `[0, 360)`
- Reject duplicate directions within tolerance (including wraparound)
- Sort creases counterclockwise
- Compute sector angles (including wraparound)
- Verify sector angles sum to 360°
- Kawasaki’s theorem (even crease count; alternating sector sums ≈ 180°)
- Maekawa’s theorem (`|M − V| == 2`)
- Structured diagnostic results (not bare booleans)

Out of scope for now: multi-vertex patterns, folding simulation, SVG, FOLD files.

## Development

```bash
pytest
```

## License

MIT
