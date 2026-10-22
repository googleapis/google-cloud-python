#!/usr/bin/env bash
# Builds the IPC flow of the Spanner Go Shared Core prototype:
#   ipc/spanner_ipc_server   - Go sidecar executable (serves ExecuteStreamingSql over AF_UNIX)
#   ipc/spanner_ipc_ext.so   - CPython abi3 client extension for the sidecar
#
# The FFI flow is NOT touched: libspanner_go.so, spanner_go_ext.so, c_ext/spanner_go_ext.c and the
# shared-core Go sources are only read. The sidecar is compiled from a temporary staged copy of the
# exact same Go sources the FFI library is built from; the only transformation is deleting the
# empty `func main() {}` stub that -buildmode=c-shared requires (verified below with diff).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IPC_DIR="$SCRIPT_DIR/ipc"
export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"

echo "=== Building Spanner Go Shared Core IPC sidecar + Python IPC extension ==="

if ! command -v go &> /dev/null; then
    echo "ERROR: 'go' compiler not found in PATH (needed to build ipc/spanner_ipc_server)."
    exit 1
fi
echo "[*] Go version: $(go version)"

BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/spanner_ipc_build.XXXXXX")"
trap 'rm -rf "$BUILD_DIR"' EXIT

# 1. Stage the unmodified shared-core sources (every non-test .go file next to main.go).
CORE_SOURCES=()
for f in "$SCRIPT_DIR"/*.go; do
    base="$(basename "$f")"
    case "$base" in
        *_test.go) continue ;;
    esac
    cp "$f" "$BUILD_DIR/$base"
    CORE_SOURCES+=("$base")
done
cp "$SCRIPT_DIR/go.mod" "$SCRIPT_DIR/go.sum" "$BUILD_DIR/"
echo "[*] Staged shared-core sources: ${CORE_SOURCES[*]}"

# 2. Remove ONLY the empty c-shared main stub from the staged main.go and prove nothing else changed.
STUB_RE='^func main\(\) \{\}[[:space:]]*$'
STUB_COUNT="$(grep -cE "$STUB_RE" "$BUILD_DIR/main.go" || true)"
if [ "$STUB_COUNT" != "1" ]; then
    echo "ERROR: expected exactly one 'func main() {}' stub in main.go, found $STUB_COUNT"
    exit 1
fi
sed -i -E "/$STUB_RE/d" "$BUILD_DIR/main.go"
DIFF_LINES="$(diff "$SCRIPT_DIR/main.go" "$BUILD_DIR/main.go" | grep -c '^[<>]' || true)"
if [ "$DIFF_LINES" != "1" ]; then
    echo "ERROR: staged main.go differs from the FFI main.go by $DIFF_LINES lines (expected 1)"
    exit 1
fi
echo "[+] Staged main.go == FFI main.go minus the empty c-shared 'func main() {}' stub"

# 3. Add the sidecar entry point and build it with the same toolchain/module graph as the FFI lib.
#    -buildmode=pie keeps the generated code position-independent like the c-shared FFI library.
cp "$IPC_DIR/spanner_ipc_server.go" "$BUILD_DIR/"
echo "[*] Building ipc/spanner_ipc_server (-buildmode=pie, -tags spanner_ipc_server)..."
(cd "$BUILD_DIR" && go build -buildmode=pie -tags spanner_ipc_server -o "$IPC_DIR/spanner_ipc_server" .)
echo "[+] Built $IPC_DIR/spanner_ipc_server"

# 4. Record which sources the IPC artifacts were built from (content hashes, checked by the benchmark).
(cd "$SCRIPT_DIR" && sha256sum "${CORE_SOURCES[@]}" go.mod go.sum ipc/spanner_ipc_server.go ipc/c_ext/spanner_ipc_ext.c) \
    > "$IPC_DIR/ipc_build_sources.sha256"

# 5. Build the CPython abi3 IPC client extension with the same compiler flags as spanner_go_ext.so.
if ! command -v gcc &> /dev/null; then
    echo "ERROR: 'gcc' not found (needed to build ipc/spanner_ipc_ext.so)."
    exit 1
fi
PY_BIN="${PYTHON:-python3}"
PY_INC="$("$PY_BIN" -c 'import sysconfig; print(sysconfig.get_path("include"))' 2>/dev/null || true)"
INC_FLAG=""
if [ -n "$PY_INC" ] && [ -f "$PY_INC/Python.h" ]; then
    INC_FLAG="-I$PY_INC"
fi
echo "[*] Compiling CPython Stable ABI extension ipc/spanner_ipc_ext.so..."
gcc -O3 -shared -fPIC \
    $INC_FLAG \
    "$IPC_DIR/c_ext/spanner_ipc_ext.c" \
    -lpthread \
    -o "$IPC_DIR/spanner_ipc_ext.so"
echo "[+] Built $IPC_DIR/spanner_ipc_ext.so"

# 6. Parity between the FFI library and the IPC sidecar.
#    a) Go toolchain + full module graph (incl. h1 hashes / replacements) + build settings
#       (excluding -buildmode, -tags and vcs.* which legitimately differ).
#    b) Function-level code identity: build a reference c-shared library from the staged (unmodified)
#       sources and compare the size of every shared-core `main.*` function in
#         committed libspanner_go.so  vs  reference build   (committed FFI lib == current sources)
#         committed libspanner_go.so  vs  spanner_ipc_server (sidecar runs the same functions)
if [ -f "$SCRIPT_DIR/libspanner_go.so" ]; then
    fingerprint() {
        go version -m "$1" | awk '
            NR == 1 { sub(/^[^:]+: /, ""); print "go " $0; next }
            $1 == "dep" || $1 == "=>" { $1 = $1; print; next }
            $1 == "build" { split($2, kv, "="); k = kv[1];
                            if (k != "-buildmode" && k != "-tags" && k !~ /^vcs/) { $1 = $1; print } }' | sort
    }
    if diff <(fingerprint "$SCRIPT_DIR/libspanner_go.so") <(fingerprint "$IPC_DIR/spanner_ipc_server") > /dev/null; then
        echo "[+] PARITY OK: same Go toolchain, module graph (h1 hashes) and build settings"
    else
        echo "[!] PARITY WARNING: Go toolchain/modules/build settings differ between libspanner_go.so and spanner_ipc_server:"
        diff <(fingerprint "$SCRIPT_DIR/libspanner_go.so") <(fingerprint "$IPC_DIR/spanner_ipc_server") || true
        echo "[!] Rebuild both with the same toolchain: bash build_go_core.sh && bash build_ipc_core.sh"
    fi

    REF_DIR="$BUILD_DIR/ref"
    mkdir -p "$REF_DIR"
    for f in "${CORE_SOURCES[@]}"; do cp "$SCRIPT_DIR/$f" "$REF_DIR/$f"; done
    cp "$SCRIPT_DIR/go.mod" "$SCRIPT_DIR/go.sum" "$REF_DIR/"
    echo "[*] Building a reference c-shared library from the staged sources for code-identity checks..."
    (cd "$REF_DIR" && go build -buildmode=c-shared -o "$REF_DIR/ref_libspanner_go.so" .)
    core_funcs() {
        # Shared-core functions only: skip the sidecar entry point, cgo-generated wrappers (their names
        # embed a per-build hash) and package init.
        go tool nm -size "$1" | awk '($3 == "T" || $3 == "t") && $4 ~ /^main\./ &&
            $4 !~ /^main\.(main|ipc|_cgo|_Cfunc|_cgoexp|cgo|init)/ { print $4, $2 }' | sort -u
    }
    core_funcs "$SCRIPT_DIR/libspanner_go.so" > "$BUILD_DIR/ffi.funcs"
    core_funcs "$REF_DIR/ref_libspanner_go.so" > "$BUILD_DIR/ref.funcs"
    core_funcs "$IPC_DIR/spanner_ipc_server" > "$BUILD_DIR/ipc.funcs"
    N_FFI="$(wc -l < "$BUILD_DIR/ffi.funcs")"
    if diff -q "$BUILD_DIR/ffi.funcs" "$BUILD_DIR/ref.funcs" > /dev/null; then
        echo "[+] CODE OK: committed libspanner_go.so matches the current shared-core sources ($N_FFI functions, identical sizes)"
    else
        echo "[!] CODE WARNING: committed libspanner_go.so does NOT match the current sources (rebuild with build_go_core.sh):"
        diff "$BUILD_DIR/ffi.funcs" "$BUILD_DIR/ref.funcs" | head -n 20 || true
    fi
    MISSING="$(join -v1 "$BUILD_DIR/ffi.funcs" "$BUILD_DIR/ipc.funcs" | wc -l)"
    SIZE_DIFF="$(join "$BUILD_DIR/ffi.funcs" "$BUILD_DIR/ipc.funcs" | awk '$2 != $3' | wc -l)"
    if [ "$MISSING" == "0" ] && [ "$SIZE_DIFF" == "0" ]; then
        echo "[+] CODE OK: spanner_ipc_server contains all $N_FFI shared-core functions of libspanner_go.so with identical sizes"
    else
        echo "[!] CODE WARNING: $MISSING shared-core functions missing / $SIZE_DIFF with different sizes in the sidecar:"
        join -a1 "$BUILD_DIR/ffi.funcs" "$BUILD_DIR/ipc.funcs" | awk 'NF < 3 || $2 != $3' | head -n 20
    fi
fi

echo "=== Spanner Go Shared Core IPC flow ready ==="
