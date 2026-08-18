# Contributing

Thanks for your interest in improving crease-vertex!

## Setup

```bash
git clone https://github.com/neha9029/crease-vertex.git
cd crease-vertex
python -m pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

All changes should keep the test suite green. New behavior should come with
tests; bug fixes should include a regression test.

## Guidelines

- Python 3.11+, type hints everywhere, no runtime dependencies.
- Behavior is specified by the tests in `tests/` — when changing the public
  API, update the tests and the docstrings in `crease_vertex/__init__.py`.
- Keep the scope focused on single-vertex analysis. Multi-vertex crease
  patterns, folding simulation, and file-format support (SVG, FOLD) are
  out of scope for now.

## Reporting issues

Open an issue at
[github.com/neha9029/crease-vertex/issues](https://github.com/neha9029/crease-vertex/issues)
with a minimal reproducible example (the crease angles, tolerance, and the
result you expected).
