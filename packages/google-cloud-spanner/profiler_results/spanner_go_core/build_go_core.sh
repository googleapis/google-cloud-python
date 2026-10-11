#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Building Go Spanner Shared Core for Python ==="

export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"

if command -v go &> /dev/null; then
    echo "[*] Go version: $(go version)"
    echo "[*] Building libspanner_go.so (c-shared)..."
    go build -buildmode=c-shared -o libspanner_go.so .
    echo "[+] Built $SCRIPT_DIR/libspanner_go.so"
elif [ -f "$SCRIPT_DIR/libspanner_go.so" ]; then
    echo "[+] 'go' compiler not found in PATH; using prebuilt $SCRIPT_DIR/libspanner_go.so"
else
    echo "ERROR: Neither 'go' compiler nor prebuilt libspanner_go.so found."
    exit 1
fi

if command -v gcc &> /dev/null; then
    PY_INC="$(python3 -c 'import sysconfig; print(sysconfig.get_path("include"))' 2>/dev/null || true)"
    INC_FLAG=""
    if [ -n "$PY_INC" ] && [ -f "$PY_INC/Python.h" ]; then
        INC_FLAG="-I$PY_INC"
    fi
    echo "[*] Compiling CPython Stable ABI extension spanner_go_ext.so..."
    gcc -O3 -shared -fPIC \
        $INC_FLAG \
        "$SCRIPT_DIR/c_ext/spanner_go_ext.c" \
        -ldl \
        -Wl,-rpath,'$ORIGIN' \
        -o "$SCRIPT_DIR/spanner_go_ext.so"
    echo "[+] Built $SCRIPT_DIR/spanner_go_ext.so"
elif [ -f "$SCRIPT_DIR/spanner_go_ext.so" ]; then
    echo "[+] 'gcc' not found; using prebuilt ABI3 binary $SCRIPT_DIR/spanner_go_ext.so"
else
    echo "ERROR: Neither 'gcc' nor prebuilt spanner_go_ext.so found."
    exit 1
fi

echo "=== Go Spanner Shared Core Ready ==="
