# Design Doc: Multi-Stream Scaling and Unfinalized Object Support in AsyncMultiRangeDownloader (MRD)

## Background
The Google Cloud Storage (GCS) Python SDK provides `AsyncMultiRangeDownloader` (MRD) to execute parallel range reads over a single bidi-gRPC (`BidiReadObject`) connection. Higher-level storage layers like `gcsfs` use MRD to service concurrent file reads, machine learning data loaders, and columnar analytics queries (Parquet/ORC).

In high-throughput environments like Google Cloud Storage RAPID (low-latency, zonal storage class), network bandwidth often exceeds what a single bidi-gRPC stream can handle. A single gRPC connection caps around 1.0 to 1.2 GB/s due to single-TCP and single-HTTP/2 flow control limits. Workloads requiring multi-gigabyte/sec throughput are throttled unless requests are multiplexed across multiple streams. Additionally, objects actively being appended (unfinalized objects) frequently fail or get rejected in range readers because their exact size is changing and full-object CRC32c checksums are unavailable.

## Objective
1. Scale throughput beyond single-stream limits to achieve over 2.0 GB/s on high-bandwidth storage classes like RAPID.
2. Provide dynamic, automatic connection scaling with load-based balancing.
3. Support seamless reading of unfinalized / actively appended objects without checksum errors.
4. Keep the public API clean, backward-compatible, and easy to configure for downstream consumers like `gcsfs`.

## Overview
We enhance `AsyncMultiRangeDownloader` with an internal stream pool (`_StreamPool`) and stream manager (`_ManagedStream`). Instead of dispatching all range requests into one multiplexer, requests are assigned to the least-loaded stream. 

When stream load exceeds a target threshold, the pool automatically spins up additional bidi-gRPC streams in the background up to a configurable maximum. Stream selection is non-blocking: incoming range reads are dispatched immediately to the stream with the lowest active load, allowing HTTP/2 flow control to manage wire-level rate limiting without internal client stalls. For unfinalized objects, MRD skips the full-object CRC32c verification while preserving per-chunk CRC32c validation.

## Detailed Design

### 1. Configuration (`MRDStreamConfig`) & Zero-Overhead Rollback
Callers configure multi-stream behavior via `stream_config=MRDStreamConfig(...)` on `AsyncMultiRangeDownloader.create_mrd`:

* `min_connections` (int, default 1): Initial number of pre-warmed streams opened during initialization.
* `max_connections` (int, default 8): Upper limit on total concurrent bidi-gRPC streams.
* `target_io_depth` (int, default 8): Target concurrent in-flight requests per stream before triggering scale-up.
* `target_bytes` (int, default 8 MB): Target in-flight bytes per stream before triggering scale-up.

**Single-Connection Rollback**: If `stream_config` is `None` or `max_connections <= 1`, `_StreamPool` is not created. Calls to `download_ranges` execute a pure direct single-stream path without any `io-ranges` or `io-bytes` tracking, locking, or pool overhead.

### 2. Load Balancing Metric and Dynamic Scaling
Each worker tracks its active `pending_ranges` and `pending_bytes`. Load is computed as:

Load = 0.5 * (pending_ranges / target_io_depth) + 0.5 * (pending_bytes / target_bytes)

* **Stream Selection (Non-Blocking)**: Incoming range requests are assigned to the worker with the lowest Load. Stream selection is instantaneous and non-blocking.
* **Scale-Up Trigger**: If the best available stream has Load >= 1.0, and total connections < `max_connections`, a background task opens an additional stream. New streams reuse the existing `read_handle` and routing token for sub-millisecond connection setup without repeating object lookups.
* **Proportional Scale-Up**: Background stream creation is triggered in direct proportion to total pool load (`desired_connections = ceil(total_load)`). During large concurrent bursts, multiple background streams are launched in parallel up to `max_connections`, preventing connection bottlenecks while immediately serving requests on existing streams.
* **Flow Control**: Backpressure is delegated to HTTP/2 and TCP window flow control (`WINDOW_UPDATE` frames) and caller-level task management, avoiding internal thread/coroutine blocking within the client library.

### 3. Unfinalized Object Handling
For objects where `is_finalized` is False:
* **Size Ratcheting**: Persisted size is dynamically updated: persisted_size = max(persisted_size, offset + length).
* **Checksum Management**: Full-object CRC32c validation is bypassed since unfinalized objects do not have a finalized full-object checksum. Per-chunk CRC32c validation remains active to protect against transport data corruption.
* **Handle Propagation**: Newly refreshed `read_handle` tokens received in read responses are shared across the pool so all subsequent stream openings connect to the latest object state.

## Empirical Benchmark & Saturation Data

All benchmarks below were executed directly against an actual 20 GiB file (`gs://princer-rapid-bucket/bench/bench_20GB.bin`) in Google Cloud Storage.

### Single-Stream Saturation Heatmap (I/O Size vs I/O Depth)

| I/O Size | Depth 1 | Depth 2 | Depth 4 | Depth 8 | Depth 16 | Depth 32 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **128 KB** | 131.7 MB/s | 306.5 MB/s | 550.2 MB/s | 747.5 MB/s | 761.3 MB/s | 774.9 MB/s |
| **256 KB** | 252.6 MB/s | 488.5 MB/s | 901.7 MB/s | 957.7 MB/s | 980.6 MB/s | 1,017.9 MB/s |
| **512 KB** | 332.0 MB/s | 579.7 MB/s | 883.5 MB/s | 1,000.2 MB/s | 1,024.1 MB/s | 1,032.7 MB/s |
| **1 MB**   | 372.1 MB/s | 625.9 MB/s | 926.5 MB/s | 983.0 MB/s | 1,004.8 MB/s | 990.5 MB/s |
| **2 MB**   | 406.0 MB/s | 705.4 MB/s | 975.6 MB/s | 1,019.2 MB/s | 974.3 MB/s | 1,037.3 MB/s |
| **4 MB**   | 510.3 MB/s | 913.9 MB/s | 956.8 MB/s | 953.1 MB/s | 1,064.0 MB/s | 1,127.4 MB/s |
| **8 MB**   | 630.2 MB/s | 947.1 MB/s | 983.5 MB/s | 1,074.0 MB/s | 1,098.1 MB/s | 1,057.1 MB/s |
| **16 MB**  | 700.6 MB/s | 974.8 MB/s | 1,033.7 MB/s | 936.0 MB/s | 951.1 MB/s | 902.2 MB/s |

### Saturation Depth per I/O Size

| I/O Size | Depth for ~950 MB/s | Depth for >= 1.0 GB/s | In-Flight Memory at Saturation |
| :--- | :---: | :---: | :---: |
| **16 MB** | Depth 2 (975 MB/s) | Depth 4 (1,034 MB/s) | 32 MB – 64 MB |
| **8 MB**  | Depth 2 (947 MB/s) | Depth 8 (1,074 MB/s) | 16 MB – 64 MB |
| **4 MB**  | Depth 4 (957 MB/s) | Depth 16 (1,064 MB/s) | 16 MB – 64 MB |
| **2 MB**  | Depth 4 (976 MB/s) | Depth 8 (1,019 MB/s) | 8 MB – 16 MB |
| **1 MB**  | Depth 6–8 (950–983 MB/s) | Depth 16 (1,005 MB/s) | 6 MB – 16 MB |
| **512 KB**| Depth 6–8 (950–1,000 MB/s) | Depth 8 (1,000 MB/s) | 3 MB – 4 MB |
| **256 KB**| Depth 8 (958 MB/s) | Depth 32 (1,018 MB/s) | 2 MB – 8 MB |
| **128 KB**| Capped at 775 MB/s | N/A | High RPC framing overhead |

### Full 20 GiB End-to-End Download Comparison

| Configuration | I/O Size | Concurrency Depth | Elapsed Time | Sustained Throughput | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Single Stream (1)** | 1 MB | 8 | 16.27 s | **1,258.41 MB/s (1.32 GB/s)** | Peak single stream performance |
| **Single Stream (1)** | 8 MB | 8 | 18.47 s | **1,108.62 MB/s (1.16 GB/s)** | Standard large read |
| **Single Stream (1)** | 4 MB | 8 | 20.04 s | **1,021.94 MB/s (1.07 GB/s)** | Conservative read |
| **Multi-Stream (4–8)** | 8 MB | 32 | **11.24 s** | **1,821.62 MB/s (1.91 GB/s)** | **Full 20 GiB transferred in 11.2s** |
| **Multi-Stream (4–8)** | 8 MB | 32 (20GB load) | **10.09 s** | **2,030.60 MB/s (2.13 GB/s)** | **Peak aggregate throughput** |

## Alternative Solutions

| Alternative | Description | Pros | Cons / Reason Not Chosen |
| :--- | :--- | :--- | :--- |
| **External Pooling in gcsfs** | Manage multiple MRD instances in gcsfs layer. | No changes to storage package. | High overhead: duplicate open handshakes, no shared routing tokens, high memory duplication, cannot load balance sub-ranges. |
| **Static Fixed Multi-Stream** | Always open N streams upfront. | Simple implementation. | Wastes socket resources on small reads; lacks dynamic adaptation. |
| **Round-Robin Routing** | Distribute requests uniformly across streams. | Simple routing logic. | Leads to straggler stalls when range sizes differ. |
| **Dynamic Load-Aware Pool (Chosen)** | Internal stream pool with heuristic load metric and shared handles. | Zero overhead on small files, optimal throughput on heavy workloads, non-blocking dispatch. | Slight increase in internal state management. |

## Impact Checklist
* **Backward Compatibility**: Fully preserved. Existing `AsyncMultiRangeDownloader.create_mrd` signatures and behaviors are unchanged.
* **Security & Auth**: Reuses credentials and channel state from `AsyncGrpcClient`. No new permissions or tokens required.
* **Resource Usage**: Streams scale down and close cleanly when `mrd.close()` is called. In-flight requests are distributed non-blockingly.
* **Dependencies**: No external library additions. Relies entirely on `asyncio` and `grpc.aio`.

## Test Plan
1. **Unit Testing**:
   * Verify stream load metric calculation.
   * Verify scale-up triggers and least-loaded stream selection.
   * Verify parameter passthrough via `MRDStreamConfig`.
   * Verify dynamic persisted size ratcheting and checksum bypass on unfinalized objects.
   * Ensure 100% of existing unit tests pass without regression.
2. **Integration / Live Bucket Testing**:
   * Verified against live zonal bucket `gs://princer-rapid-bucket/`.
   * Verified full download of 20 GiB object (`bench/bench_20GB.bin`).
   * Benchmarked throughput across 48 combinations of I/O size and depth.
   * Confirmed clean socket teardown and zero resource leakage.

## Rollout / Rollback Plan
* **Rollout**: Ship as part of `google-cloud-storage` release. By default, `min_connections=1` ensures standard behavior unless callers opt in or heavy concurrent workloads trigger scaling. `gcsfs` can pass `MRDStreamConfig` to leverage high-bandwidth multi-stream reads.
* **Rollback**: Callers can set `max_connections=1` to immediately restrict execution to a single connection. The code can be reverted without schema or protocol migrations.
