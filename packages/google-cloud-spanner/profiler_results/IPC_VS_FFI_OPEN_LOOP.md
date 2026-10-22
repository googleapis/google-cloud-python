# IPC vs FFI vs pure-Python: open-loop benchmark for the Spanner Go Shared Core

This directory contains two ways to reach the same Go Shared Core from Python, plus the stock client:

| Client (`--clients`) | Boundary | Python entry | Go code that runs |
| :-- | :-- | :-- | :-- |
| `ffi` (unchanged) | In-process cgo call | `spanner_go_ext.execute_streaming_sql(handle, session, sql, param)` | `libspanner_go.so` → `ExecuteStreamingSqlSync` → `executeStreamingSqlInternal` → `buildCBatch` |
| `ipc` (new, default) | Unix domain socket to a sidecar process | `spanner_ipc_ext.execute_streaming_sql(handle, session, sql, param)` | `spanner_ipc_server -lock-os-thread` → `executeStreamingSqlInternal` → `buildCBatch` (same code) |
| `ipc_goroutine` (optional) | Same socket protocol | same as `ipc` | `spanner_ipc_server` running calls on plain goroutines |
| `python` | none | stock `Snapshot.execute_sql` (GAPIC + grpcio + proto-plus) | – |
| `python_nometrics` (optional) | none | same as `python` with `SPANNER_DISABLE_BUILTIN_METRICS=true` | – |
| `null` (optional) | none | harness baseline: each request is a `sleep()`, no Spanner | – |

## Files

| File | Purpose |
| :-- | :-- |
| [`spanner_go_core/ipc/spanner_ipc_server.go`](spanner_go_core/ipc/spanner_ipc_server.go) | Sidecar entry point (`//go:build spanner_ipc_server`, excluded from the FFI build). |
| [`spanner_go_core/ipc/c_ext/spanner_ipc_ext.c`](spanner_go_core/ipc/c_ext/spanner_ipc_ext.c) | CPython abi3 IPC client; same call shape and row materialization as the FFI extension. |
| [`spanner_go_core/build_ipc_core.sh`](spanner_go_core/build_ipc_core.sh) | Builds the IPC artifacts and verifies toolchain, module and function-level parity with `libspanner_go.so`. |
| [`spanner_open_loop_benchmark.py`](spanner_open_loop_benchmark.py) | Open-loop benchmark, result parity check, per-thread CPU attribution. |

The FFI sources and artifacts (`main.go`, `client.go`, `decode.go`, `c_ext/spanner_go_ext.c`, `libspanner_go.so`,
`spanner_go_ext.so`) are not modified.

## Why the FFI vs IPC comparison is apples-to-apples

1. **Same Go code, verified.** `build_ipc_core.sh` compiles the sidecar from a staged copy of the exact
   FFI sources. The only change is deleting the empty `func main() {}` stub required by
   `-buildmode=c-shared`, and the script checks that the diff is exactly that one line. It then checks
   three things:
   * (a) the same Go toolchain, module graph (including h1 hashes) and build settings;
   * (b) every shared-core `main.*` function has the same size in the committed `libspanner_go.so`
     and in a fresh reference build, which proves the committed FFI library matches the current sources;
   * (c) every shared-core function has the same size in `libspanner_go.so` and in the sidecar.

   The sidecar is built as PIE, so its codegen is position-independent like the c-shared library. Two
   independent audits also found identical normalized disassembly for `executeStreamingSqlInternal`,
   `buildCBatch`, `FreeSpannerBatch`, `NewCoreClient`, the timing codec, the runtime, and the gRPC
   transport.
2. **Same Go entry points.** The sidecar's `INIT` calls `InitGoCoreClient(n)`, so the channel pool, TLS,
   auth and flow-control windows match. `EXECUTE` calls `executeStreamingSqlInternal` and then
   `FreeSpannerBatch`.
3. **No re-encoding at the boundary.** The sidecar `writev()`s the `CSpannerCell[]` array and string
   arena straight from the C heap. The client rebuilds string pointers as arena offsets. There is no JSON
   or protobuf between Python and the sidecar.
4. **Same Python-side work.** Both extensions release the GIL for the whole Spanner call. Both build
   rows with the same per-cell `PyUnicode_FromStringAndSize` / `PyFloat_FromDouble` / `PyBool_FromLong` /
   `None` calls. Both raise the same `RuntimeError` text. Both are called through one
   `Snapshot.execute_sql` hook (`go_core_snapshot_hook`), and only `execute_fn` differs.
5. **Same concurrency shape.** An FFI thread blocks in one cgo call at a time. An IPC thread blocks on
   its own persistent socket, with one request in flight at a time. Point responses arrive in a single
   greedy `recv()`. Heavy responses (1000 rows × 11 columns ≈ 1.18 MB) go into a per-connection receive
   buffer that is reused across requests, and take about 6–9 `recv()` hops.
6. **Whole-process CPU on both sides of the boundary.** FFI CPU is the client process `RUSAGE_SELF`,
   which includes the in-process Go runtime. IPC CPU is the client `RUSAGE_SELF` plus the sidecar's
   `getrusage(RUSAGE_SELF)`, sampled at the same window edges. Per-thread CPU and voluntary context
   switches are also recorded from `/proc/<pid>/task/*` for both processes (`threads` in the JSON).
7. **Result parity.** Before the matrix runs, the harness checks that FFI and IPC return identical rows
   for 20 point selects and an ordered 1000-row read. It also checks that the pure-Python client
   returns the same values after string normalization. All 11 columns are `STRING`, so the checks are
   exact.

### Go execution model: what `-lock-os-thread` does and does not equalize

In FFI, every query is a cgo callback from a Python thread into Go. Two separate costs follow from that:

* **Locked-thread park/handoff.** The callback goroutine is locked to the Python thread, so every
  network wait parks and wakes that specific thread. The default `ipc` client reproduces this with
  `-lock-os-thread`, which runs each call under `runtime.LockOSThread()`.
* **Callback return / sysmon.** When the callback returns to Python after having parked, the runtime
  leaves the P in `_Psyscall`. Go's sysmon thread then cannot deep-sleep and polls every 20 µs until it
  takes the P back, about 10 ms later. This cost exists only because Go is called from foreign
  threads. It is a real cost of the FFI boundary, and the IPC sidecar neither has nor emulates it.

Measured on the 24-vCPU development host, voluntary context switches per point query were:

| Client | Context switches / query |
| :-- | :-- |
| FFI | 73–85 |
| `ipc` (locked) | 27–30 (about 25 in the sidecar + 4 in the client) |
| `ipc_goroutine` | 22–24 |

An auditor's controlled reproduction attributed about 76 of FFI's switches to sysmon. The cost of that
polling depends on the host's price per sleep/wake (the report includes a calibration) and on the load
shape. At ≤50 QPS it costs FFI roughly 0.7–1.5 ms CPU per query on that host, so IPC was cheaper. In the
reproduction, FFI became cheaper again from about 100 QPS, once worker threads re-enter Go before sysmon
gives up. Treat low-QPS CPU differences as a property of the FFI runtime integration, not of sockets. The
"top-waker thread" column, the thread with the most voluntary switches, makes the mechanism visible per
run.

## Open-loop methodology

* **Fixed schedule.** Requests follow a fixed schedule (`--arrival uniform|poisson`) at 10/50/100/500 QPS,
  independent of completions. Latency is measured from the scheduled send time, so there is no
  coordinated omission. The JSON also reports service time, dispatcher lag and worker-pool wait.
* **One stream per run.** Each run is one continuous stream: an 8 s warmup that ramps from 20% to 100% of
  the rate, then a 20 s measurement window. CPU is sampled at the window edges.
* **Throughput.** Two numbers are reported. `goodput` counts requests scheduled in the window that
  succeeded; this is the primary number. `achieved` counts completions that landed inside the window.
* **Saturation honesty.** Requests never started when the window closes are cancelled (`dropped`).
  They are included in latency percentiles as censored at the window close, which is a lower bound.
  Each run gets flags:
  * `S`: saturated (requests dropped, or achieved below 95% of offered);
  * `P`: the worker-pool cap was hit, so the run was partly closed loop;
  * `N`: non-stationary (achieved more than 5% off offered, or p50 drifting between the two halves of
    the window).
* **Isolation and noise.** Every (client, workload, QPS, repetition) runs in a fresh process, with a fresh
  sidecar for IPC. Client order rotates between steps, and `--repeats N` interleaves N repetitions and
  reports medians with min–max ranges.
* **Channels.** Every client gets the same static channel count per workload and QPS. With
  `--channels auto` the count is `max(ceil(qps × 0.2 s / 25 streams), ceil(qps × bytes/query /
  (0.5 × 16 MiB / RTT)))`. The second term is the bandwidth-delay limit of the Go core's fixed 16 MiB
  HTTP/2 connection window. RTT and response sizes come from the parity run. In-region this gives
  1/1/1/4 channels for 10/50/100/500 QPS; across a 200 ms WAN, heavy reads get more. The pure-Python
  client gets the same count through a round-robin pool of independent grpcio channels
  (`grpc.use_local_subchannel_pool=1`, stock channel options and interceptors; verified to open N
  connections and spread RPCs evenly). Override with an int or a map such as
  `--channels 10:1,50:2,100:2,500:4`.
* **Concurrency cap.** Max in-flight requests (worker threads) is `clamp(ceil(qps × 1 s), 32, 256)` for
  point selects and `clamp(ceil(qps × 1 s), 32, 128)` for heavy reads, the same for every client.
  Override with `--max-inflight N`, for example on a small-memory VM.
* **Harness cost.** The dispatcher and worker-pool CPU is included for every client. Measure it with
  `--clients null`; on the development host it was about 0.4–0.5 ms per request.

## Caveats when comparing against pure Python

The Go core skips Python-side work that the stock client does:
* built-in metrics, tracing and request-id metadata;
* resume/retry wrappers;
* typed decoding (Go returns `str`/`float`/`bool`/`None`).

It also uses fixed 4/16 MiB flow-control windows without keepalive, while grpcio uses BDP-probed windows
and a 120 s keepalive. Use `python_nometrics` to see the stock client without built-in metrics.

## Running

```bash
cd packages/google-cloud-spanner/profiler_results
python3 spanner_open_loop_benchmark.py --smoke                                   # ~3-5 min sanity run
python3 spanner_open_loop_benchmark.py                                           # python, ffi, ipc x point, heavy x 10/50/100/500 QPS
python3 spanner_open_loop_benchmark.py --repeats 3 --clients python,ffi,ipc,ipc_goroutine
python3 spanner_open_loop_benchmark.py --clients ffi,ipc --workloads heavy --qps 50,100 --duration 30 --go-pprof
```

Results go to `open_loop_results/`: `open_loop_results.json` (per-run and aggregated metrics),
`open_loop_summary.md`, plus per-run JSON files and logs under `open_loop_results/runs/`.
