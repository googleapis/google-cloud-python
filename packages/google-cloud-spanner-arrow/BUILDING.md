# Building `google-cloud-spanner-arrow`

## Requirements

- Python >= 3.10
- C99 compatible compiler (`gcc`, `clang`, or MSVC on Windows)
- `setuptools >= 64.0.0`, `wheel`
- `pyarrow >= 14.0.0`

## Local Development & Installation

### Editable install with C extension:
```bash
pip install -e .
```

### Pure Python fallback build:
```bash
SPANNER_ARROW_PURE_PYTHON=1 pip install -e .
```

## Running Tests

```bash
pytest tests
```

## Multi-Platform Wheels

Multi-platform wheels are built using the scripts in `scripts/`:
- Linux: `scripts/manylinux/build.sh`
- macOS: `scripts/osx/build.sh`
- Windows: `scripts\windows\build.bat`
