# Open-loop benchmark: Go Shared Core FFI vs IPC vs pure-Python client

* Host: `suvham-vm-1-core` (1 vCPU), Python 3.11.2, started 2026-10-23 07:08:55 UTC
* Host wake cost: 7.7 µs CPU per 20 µs sleep/wake cycle (drives the cost of Go's sysmon polling after cgo callbacks)
* Target: `projects/span-cloud-testing/instances/suvham-testing/databases/benchmark_db_async`; heavy read: `SELECT * FROM AsyncBenchmarkTable LIMIT 1000`; RTT estimate: 3.10 ms
* Open loop: uniform arrivals, warmup 8.0 s (ramped) + window 20.0 s, 3 interleaved rep(s), fresh process per run, client order rotated
* Channels per workload/QPS (same for all clients): `{'point/10': 1, 'point/50': 1, 'point/100': 1, 'point/500': 4, 'heavy/10': 1, 'heavy/50': 1, 'heavy/100': 1, 'heavy/500': 4}`
* Max in-flight per workload/QPS: `{'point/10': 32, 'point/50': 50, 'point/100': 100, 'point/500': 256, 'heavy/10': 32, 'heavy/50': 50, 'heavy/100': 100, 'heavy/500': 128}`
* FFI/IPC build parity: OK (same Go toolchain, module graph and build settings)
* Clients: `python` = Pure Python (stock client); `ffi` = Go core FFI (unchanged); `ipc` = Go core IPC (sidecar, locked-thread calls)
* Result parity: **PASS** (heavy rows ffi/ipc/python = {'ffi': 1000, 'ipc': 1000, 'python': 1000}; IPC heavy response 1183929 B in 34 recv hops; point 1228 B in 1 hop(s))
* Flags: S = saturated, P = worker-pool cap hit, N = non-stationary. Latency percentiles include dropped requests censored at window close.

| Workload | QPS | Ch | Client | Goodput | Achieved | p50 ms | p90 ms | p99 ms | p99.9 ms | CPU cores (client+sidecar) | CPU ms/query | vol. ctx sw/query | Err | Drop | Flags |
| :-- | --: | --: | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-: |
| point | 10 | 1 | python | 10.0 | 10.0 | 7.23 | 7.86 | 9.50 | 10.81 | 0.035 | 3.46 | 30.3 | 0 | 0 | - |
| point | 10 | 1 | ffi | 10.0 | 10.0 | 5.24 | 5.92 | 7.30 | 9.42 | 0.011 | 1.09 | 16.3 | 0 | 0 | - |
| point | 10 | 1 | ipc | 10.0 | 10.0 | 5.83 | 7.08 | 10.47 | 11.65 | 0.012 (0.005+0.007) | 1.16 | 18.9 | 0 | 0 | - |
| point | 50 | 1 | python | 50.0 | 50.0 | 7.26 | 8.07 | 11.00 | 13.11 | 0.156 | 3.11 | 26.9 | 0 | 0 | - |
| point | 50 | 1 | ffi | 50.0 | 50.0 | 5.19 | 5.91 | 8.71 | 11.03 | 0.050 | 1.00 | 17.6 | 0 | 0 | - |
| point | 50 | 1 | ipc | 50.0 | 50.0 | 5.48 | 6.26 | 10.66 | 12.33 | 0.056 (0.021+0.034) | 1.13 | 21.1 | 0 | 0 | - |
| point | 100 | 1 | python | 100.0 | 100.0 | 6.17 | 6.93 | 8.11 | 10.79 | 0.260 | 2.60 | 25.8 | 0 | 0 | - |
| point | 100 | 1 | ffi | 100.0 | 100.0 | 4.86 | 5.43 | 6.09 | 7.50 | 0.082 | 0.82 | 17.2 | 0 | 0 | - |
| point | 100 | 1 | ipc | 100.0 | 100.0 | 4.56 | 5.28 | 6.18 | 9.94 | 0.084 (0.030+0.053) | 0.84 | 19.6 | 0 | 0 | - |
| point | 500 | 4 | python | 500.0 | 499.5 | 9.02 | 19.99 | 119.1 | 209.7 | 0.896 | 1.80 | 15.1 | 0 | 0 | - |
| point | 500 | 4 | ffi | 500.0 | 500.0 | 4.47 | 5.38 | 7.75 | 37.97 | 0.257 | 0.51 | 14.3 | 0 | 0 | - |
| point | 500 | 4 | ipc | 500.0 | 500.1 | 4.56 | 5.27 | 6.88 | 35.79 | 0.297 (0.101+0.196) | 0.59 | 17.3 | 0 | 0 | - |
| heavy | 10 | 1 | python | 10.0 | 10.0 | 25.58 | 59.82 | 65.56 | 67.58 | 0.199 | 19.95 | 79.7 | 0 | 0 | - |
| heavy | 10 | 1 | ffi | 10.0 | 10.0 | 22.06 | 24.17 | 40.14 | 56.85 | 0.136 | 13.58 | 94.2 | 0 | 0 | - |
| heavy | 10 | 1 | ipc | 10.0 | 10.0 | 23.86 | 26.60 | 55.91 | 59.40 | 0.142 (0.020+0.123) | 14.22 | 151.9 | 0 | 0 | - |
| heavy | 50 | 1 | python | 50.0 | 48.5 | 206.9 | 647.2 | 931.3 | 1176 | 0.973 | 20.10 | 78.7 | 0 | 0 | SPN |
| heavy | 50 | 1 | ffi | 50.0 | 50.0 | 38.72 | 68.40 | 110.9 | 140.8 | 0.630 | 12.69 | 81.1 | 0 | 0 | - |
| heavy | 50 | 1 | ipc | 50.0 | 50.0 | 30.07 | 45.03 | 112.9 | 156.8 | 0.663 (0.096+0.568) | 13.33 | 110.6 | 0 | 0 | - |
| heavy | 100 | 1 | python | 31.9 | 42.0 | 8823 | 13585 | 15831 | 16244 | 0.987 | 23.54 | 211.8 | 0 | 4075 | SPN |
| heavy | 100 | 1 | ffi | 73.7 | 76.0 | 4260 | 6391 | 7328 | 8004 | 0.861 | 11.27 | 151.1 | 0 | 1601 | SPN |
| heavy | 100 | 1 | ipc | 98.8 | 96.7 | 1145 | 1351 | 1526 | 1637 | 0.981 (0.168+0.815) | 10.15 | 83.1 | 0 | 61 | SPN |
| heavy | 500 | 4 | python | 0.0 | 36.6 | 10254 | 18249 | 20049 | 20229 | 0.984 | 26.88 | 298.7 | 0 | 29997 | SPN |
| heavy | 500 | 4 | ffi | 24.8 | 57.7 | 34937 | 43910 | 51091 | 53425 | 0.799 | 17.27 | 453.6 | 0 | 28989 | SPN |
| heavy | 500 | 4 | ipc | 0.0 | 96.8 | 10476 | 18476 | 20275 | 20455 | 0.999 (0.185+0.813) | 10.32 | 49.2 | 0 | 30000 | SPN |

## FFI vs IPC (same Go Shared Core, different boundary)

| Workload | QPS | IPC client | p50 FFI → IPC (ms) | p99 FFI → IPC (ms) | CPU ms/q FFI → IPC | IPC CPU overhead | vol. ctx sw/q FFI → IPC | top-waker thread cs/q FFI → IPC sidecar | IPC bytes/query | IPC recv hops/query | Go unmarshal µs/call FFI → IPC | Flags FFI/IPC |
| :-- | --: | :-- | --: | --: | --: | --: | --: | --: | --: | --: | --: | :-: |
| point | 10 | ipc | 5.24 → 5.83 | 7.30 → 10.47 | 1.09 → 1.16 | 6.8% | 16.3 → 18.9 | 9.6 → 9.2 | 1229 | 1.00 | 42.1 → 43.0 | -/- |
| point | 50 | ipc | 5.19 → 5.48 | 8.71 → 10.66 | 1.00 → 1.13 | 12.2% | 17.6 → 21.1 | 10.0 → 10.7 | 1229 | 1.00 | 39.0 → 42.2 | -/- |
| point | 100 | ipc | 4.86 → 4.56 | 6.09 → 6.18 | 0.82 → 0.84 | 1.8% | 17.2 → 19.6 | 9.7 → 10.0 | 1229 | 1.00 | 34.1 → 35.5 | -/- |
| point | 500 | ipc | 4.47 → 4.56 | 7.75 → 6.88 | 0.51 → 0.59 | 15.5% | 14.3 → 17.3 | 6.4 → 7.6 | 1229 | 1.00 | 26.1 → 26.3 | -/- |
| heavy | 10 | ipc | 22.06 → 23.86 | 40.14 → 55.91 | 13.58 → 14.22 | 4.7% | 94.2 → 151.9 | 70.2 → 87.6 | 1183929 | 34.00 | 6361.1 → 6486.5 | -/- |
| heavy | 50 | ipc | 38.72 → 30.07 | 110.9 → 112.9 | 12.69 → 13.33 | 5.0% | 81.1 → 110.6 | 60.1 → 58.4 | 1183929 | 33.89 | 6611.1 → 6380.6 | -/- |
| heavy | 100 | ipc | 4260 → 1145 | 7328 → 1526 | 11.27 → 10.15 | -9.9% | 151.1 → 83.1 | 36.2 → 3.4 | 1183929 | 33.97 | 5546.8 → 5051.0 | SPN/SPN |
| heavy | 500 | ipc | 34937 → 10476 | 51091 → 20275 | 17.27 → 10.32 | -40.3% | 453.6 → 49.2 | 85.3 → 2.7 | 1183929 | 33.94 | 6291.5 → 5126.4 | SPN/SPN |

Notes: CPU is whole-process (client `RUSAGE_SELF` + sidecar `getrusage`) and includes the harness's own dispatcher/worker-pool cost (measure it with `--clients null`). The top-waker column is the thread with the most voluntary context switches in the window; for FFI at low QPS this is typically Go's sysmon polling every 20 µs after each cgo callback returns (an FFI-only boundary cost). The Go unmarshal column is a thread-CPU phase timer that is only reliable when calls stay on one OS thread (`ffi`, `ipc`).