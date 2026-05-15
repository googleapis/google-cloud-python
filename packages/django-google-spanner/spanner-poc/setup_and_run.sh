#!/bin/bash

# Safe, idempotent setup and run script for the Spanner GIL-release POC.
set -euo pipefail

echo "=== Step 1: Verifying Python Environment ==="
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ( [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ] ); then
    echo "ERROR: Python 3.9+ is required. Found: Python $PYTHON_VERSION"
    exit 1
fi
echo "Python version is compatible: Python $PYTHON_VERSION"

echo "=== Step 2: Checking Rust Toolchain ==="
if ! command -v cargo &> /dev/null; then
    echo "Rust toolchain not found. Installing rustup..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust toolchain detected: $(cargo --version)"
fi

echo "=== Step 3: Installing Maturin ==="
pip install --upgrade pip
pip install maturin numpy

echo "=== Step 4: Installing Sysstat (CPU monitoring utility) ==="
if command -v apt-get &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y sysstat || echo "Failed to install sysstat. Continuing..."
elif command -v yum &> /dev/null; then
    sudo yum install -y sysstat || echo "Failed to install sysstat. Continuing..."
elif command -v dnf &> /dev/null; then
    sudo dnf install -y sysstat || echo "Failed to install sysstat. Continuing..."
elif command -v brew &> /dev/null; then
    brew install sysstat || echo "Failed to install sysstat. Continuing..."
else
    echo "WARNING: Package manager not found. Please install sysstat manually to run capture_cpu.sh."
fi

echo "=== Step 5: Cloning Google APIs Protos ==="
if [ ! -d "/tmp/googleapis" ]; then
    echo "Cloning googleapis/googleapis to /tmp/googleapis..."
    git clone --depth=1 https://github.com/googleapis/googleapis.git /tmp/googleapis
else
    echo "/tmp/googleapis already exists, skipping clone."
fi

echo "=== Step 6: Copying Required Proto Files ==="
mkdir -p proto/google/spanner/v1
mkdir -p proto/google/api
mkdir -p proto/google/rpc

cp /tmp/googleapis/google/spanner/v1/*.proto proto/google/spanner/v1/
cp /tmp/googleapis/google/api/*.proto proto/google/api/
cp /tmp/googleapis/google/rpc/*.proto proto/google/rpc/
echo "Proto directory structure prepared under spanner-poc/proto/."

echo "=== Step 7: Verifying Benchmark Configuration ==="
if grep -q "your-project" benchmark.py; then
    echo "========================================================================"
    echo "ERROR: Please configure your GCP credentials in benchmark.py first!"
    echo "Modify the following constants in benchmark.py:"
    echo "  PROJECT = 'your-project'"
    echo "  INSTANCE = 'your-instance'"
    echo "  DATABASE = 'your-database'"
    echo "  TABLE = 'your-table'"
    echo "========================================================================"
    exit 1
fi

echo "=== Step 8: Building Rust Native Extension in Release Mode ==="
# maturin develop --release installs the compiled module into the current active venv.
# --release is mandatory to ensure benchmark accuracy.
maturin develop --release

echo "=== Step 9: Executing Performance Benchmarks ==="
python benchmark.py
