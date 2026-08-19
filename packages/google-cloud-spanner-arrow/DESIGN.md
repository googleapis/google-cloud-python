# Python Spanner Apache Arrow Accelerator

## Overview
This document describes the design, architecture, and benchmark results for `google-cloud-spanner-arrow`, an optional C-extension companion package for the Google Cloud Spanner Python client. The package provides direct, accelerated conversion from incoming protobuf `PartialResultSet` stream messages into Apache Arrow record batches and tables without intermediate Python object instantiation.

Project implementation and long-term maintenance are straightforward and low-risk because the library directly follows established patterns in the Google Cloud Python client ecosystem:
- It reuses the proven companion package architecture, CI/CD build scripts, and multi-OS binary wheel distribution infrastructure of `google-crc32c`.
- It implements the standard Arrow and DataFrame query result API conventions established by `google-cloud-bigquery`.
- It maintains a complete pure-Python fallback ensuring zero breakage on unsupported platforms or environments without a C compiler.

---

## Problem Description

Data engineering, analytics, and machine learning workloads in Python (such as those using Pandas, Polars, DuckDB, and Ray) increasingly require reading large result sets from Cloud Spanner into Apache Arrow columnar formats.

Currently, applications attempting to consume Spanner data into Arrow or DataFrames face significant performance and scalability constraints:

1. **Intermediate Python Object Instantiation Overhead**:
   The standard Spanner Python client decodes gRPC messages into Python `PartialResultSet` protobuf structures, instantiating individual `google.protobuf.Value` Python objects on the heap for every column of every row. For a query returning 1,000,000 rows across 12 columns, this generates 12,000,000 intermediate Python objects, resulting in substantial CPU overhead, memory consumption (peaking at hundreds of megabytes), and garbage collection pauses.

2. **Inefficient Client-Side Conversion Paths**:
   Without native Arrow support, customers must manually iterate through row tuples, convert them to Python dictionaries or lists, and pass them to `pyarrow.Table.from_pylist()` or `pandas.DataFrame()`. This approach incurs double-conversion overhead: first decoding protobuf to Python objects, and then converting Python objects into Arrow column buffers.

3. **Global Interpreter Lock (GIL) Contention in Concurrent Workloads**:
   High-throughput workloads typically use multi-threading to parallelize reads. In pure Python, all worker threads compete for the Global Interpreter Lock (GIL) while deserializing protobuf objects and allocating heap memory. As a result, client-side ingestion throughput plateaus at approximately 28,000 to 35,000 rows/second total, failing to scale with additional CPU cores or worker threads.

To address these limitations, a solution is needed that decodes incoming gRPC stream data directly into Arrow columnar memory in native code, bypassing Python object creation and releasing the GIL during parsing.

---

## Key Requirements and Architecture

### 1. Direct Conversion to Apache Arrow
- **Direct Wire Ingestion**: The extension decodes Spanner `PartialResultSet` protobuf wire bytes directly into native Apache Arrow columnar buffers in C using the header-only `nanoarrow` library.
- **gRPC Raw Byte Interception**: In standard client execution, the gRPC transport stub configures `response_deserializer=PartialResultSet.deserialize`, which deserializes messages into Python protobuf objects. When streaming query results into Arrow, the client overrides the response deserializer (`response_deserializer=lambda raw_bytes: raw_bytes`) on the underlying `ExecuteStreamingSql` callable. This delivers raw network byte chunks directly to the C extension without invoking Python protobuf deserialization.
- **Zero Python Object Overhead**: Bypasses intermediate `google.protobuf.Value` Python object instantiation on the Python heap.
- **GIL Release**: Byte parsing and buffer construction run within `Py_BEGIN_ALLOW_THREADS` / `Py_END_ALLOW_THREADS` blocks, allowing concurrent queries across multiple threads to execute on separate CPU cores without contention on the Global Interpreter Lock (GIL).

### 2. Alignment with Google Cloud Python Architecture
This project intentionally follows established patterns in the Google Cloud Python client ecosystem rather than inventing new mechanisms:

#### A. The Companion Accelerator Pattern (`google-crc32c`)
- **Precedent**: The `google-crc32c` companion package in this monorepo provides a mature, production-tested blueprint for C-accelerated optional extensions (used by `google-cloud-storage` and `google-resumable-media`).
- **Shared Infrastructure**: Reuses the exact same build scripts, `cibuildwheel` configurations, and multi-OS wheel generation matrix (`manylinux`, macOS universal2/arm64/x86_64, Windows AMD64).
- **Release Integration**: `google-crc32c` is actively maintained as part of the monorepo's standard automated release cycle (managed by `release-please`), with regular updates tracking new Python releases (including Python 3.12, 3.13, and 3.14). The Arrow accelerator plugs directly into this existing release machinery.
- **Transparent Consumer Integration**: `google-cloud-spanner` dynamically checks for the presence of `google_cloud_spanner_arrow`. If installed, it delegates to the C extension; otherwise, it operates using the pure-Python implementation without error.

#### B. Consistency with BigQuery's Arrow API (`google-cloud-bigquery`)
- **API Symmetry**: `google-cloud-bigquery` established the standard for returning analytical query results as Arrow and DataFrames in Google Cloud Python SDKs. The Spanner implementation matches this interface:
  - `StreamedResultSet.to_arrow()`: Returns a complete `pyarrow.Table`.
  - `StreamedResultSet.to_arrow_batches()`: Yields an iterator of `pyarrow.RecordBatch` chunks as they arrive from the network (matching BigQuery's `to_arrow_iterable()`).
  - `StreamedResultSet.to_dataframe()`: Returns a `pandas.DataFrame` created directly from Arrow record batches.
- **Downstream Tool Interoperability**:
  - **Polars & DuckDB**: Directly consume `pyarrow.Table` and batch iterators with zero memory copy via the standard Arrow C Data Interface (`polars.from_arrow()`, `duckdb.arrow()`).
  - **Ray Data**: Uses `pyarrow.Table` as its native distributed in-memory block format (`ray.data.from_arrow()`).
  - **Pandas 2.0+**: Supports backing DataFrame columns directly with Arrow storage (`dtype_backend="pyarrow"`), avoiding legacy NumPy object-array conversions.

### 3. Opt-in and Graceful Fallback
- **Opt-in Dependency**: The core `google-cloud-spanner` package does not depend on `google-cloud-spanner-arrow`. Applications opt in by installing the accelerator package explicitly or via an extra (`google-cloud-spanner[arrow]`).
- **Pure-Python Fallback**: If `google-cloud-spanner-arrow` is not installed, or if C extension compilation fails on a given platform, the library automatically falls back to the pure-Python implementation in `google_cloud_spanner_arrow.python` / `google.cloud.spanner_v1._arrow`.
- **API Parity**: The pure-Python fallback and the C-accelerated implementation implement identical function signatures and schema type mappings.

### 4. Build and Distribution Strategy
- **Minimal Dependencies**: The extension relies on `nanoarrow` and the standard C library, avoiding a compile-time dependency on the full C++ `libarrow`.
- **Wheel Matrix**: Reuses the build automation and platform scripts from `google-crc32c` (`noxfile.py` and GitHub Actions `cibuildwheel` configurations) to produce pre-compiled binary wheels for:
  - Linux (x86_64, aarch64 via manylinux)
  - macOS (x86_64, arm64)
  - Windows (AMD64)
- **Source Distribution (sdist)**: Includes a fallback in `setup.py` that allows installation to succeed as pure-Python if a C compiler is unavailable.

### 5. Interaction with Future Shared Native Core
- If a shared native core is introduced for Python and Node.js to manage gRPC transport and stream processing, wire-to-Arrow decoding will be integrated directly into that core.
- The Arrow C Data Interface (`ArrowArray` / `ArrowSchema`) will remain the handoff boundary to Python (`pyarrow.RecordBatch._import_from_c`), ensuring the public API in `google-cloud-spanner` remains backward-compatible without code changes.
- The standalone `google-cloud-spanner-arrow` package would then be superseded by the shared native core.

---

## Memory and Resilience Considerations

### Memory Utilization
- In pure-Python parsing, each row value is instantiated as a Python `Value` object, generating approximately 120–160 MB of temporary heap allocations per 100,000 rows.
- The C wire parser writes values directly to contiguous Arrow column memory buffers, eliminating intermediate Python object creation and associated garbage collection overhead.

| Workload (50,000 rows $\times$ 12 columns) | Pure-Python Conversion | Direct Wire C Extension | Reduction |
| :--- | :---: | :---: | :---: |
| **Python Heap Peak Allocation (`tracemalloc`)** | 36.28 MB | **0.00 MB** | **100% reduction** |
| **Intermediate Python Objects** | ~600,000 objects | **0 objects** | **Zero GC tracking overhead** |

### Stream Resumption and Chunk Merging State Machine
- **Chunk Merging**: When Spanner splits a large field across `PartialResultSet` boundaries (`chunked_value = true`), the C parser maintains the active column buffer offset across messages and appends subsequent chunk bytes before finalizing the Arrow element.
- **Stateful Stream Decoding**: In production, the converter operates as a stateful decoder (`SpannerArrowStreamDecoder`). It buffers incoming wire chunks and tracks `last_seen_resume_token` across message boundaries.
- **Batch Handoff and Retry**: When `max_chunk_size` is reached (e.g., 65,536 rows), the decoder finalizes the `RecordBatch` and returns it alongside the `resume_token` corresponding to that completed row boundary. If a gRPC connection breaks with an `UNAVAILABLE` error between batches, the Python client restarts the stream using that recorded token without duplicate rows or data loss.

---

## Benchmark Results

Benchmarks were executed against a provisioned Google Cloud Spanner instance (`4 node, regional-europe-north1`) using a schema of 12 diverse column types (`BOOL`, `BYTES`, `DATE`, `FLOAT32`, `FLOAT64`, `INTERVAL`, `JSON`, `INT64`, `NUMERIC`, `STRING`, `TIMESTAMP`, `UUID`).

### Comparison Implementations
The benchmarks compare three implementations:
1. **Traditional Rows**: The standard Spanner Python client row iteration (`for row in results:`), returning rows as lists/tuples of Python objects.
2. **Pure-Python Arrow**: The baseline pure-Python conversion path in `google-cloud-spanner` (`to_arrow_batches()`), converting Spanner row objects into Arrow tables in Python without C acceleration.
3. **Direct Wire C Extension (`google-cloud-spanner-arrow`)**: The proposed companion accelerator, parsing raw gRPC protobuf wire bytes directly into Apache Arrow memory buffers with the GIL released.

---

### 1. Co-located End-to-End Concurrency Benchmark
- **Environment**: GCE `n2-standard-8` VM (8 vCPUs, Debian 12) located in `europe-north1-a` (same zone as the Spanner instance, < 1 ms RTT).
- **Workload**: 30,000 rows per query, 3 iterations per concurrency tier.
- **Metric**: Full wall-clock time from `ExecuteStreamingSql` RPC dispatch to complete result set ingestion.

| Concurrency | Total Rows | Total Wire Size | Traditional Rows | Pure-Python Arrow | Direct Wire C Extension | Speedup vs Traditional | Speedup vs Pure-Python |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Thread** | 30,000 | 9.1 MB | 940.8 ms *(31.9k rows/s)* | 755.5 ms *(39.7k rows/s)* | **238.5 ms (125.8k rows/s)** | 3.94x | 3.17x |
| **4 Threads** | 120,000 | 36.5 MB | 3,961.9 ms *(30.3k rows/s)* | 3,141.3 ms *(38.2k rows/s)* | **275.8 ms (435.1k rows/s)** | 14.37x | 11.39x |
| **8 Threads** | 240,000 | 73.0 MB | 8,301.2 ms *(28.9k rows/s)* | 6,536.7 ms *(36.7k rows/s)* | **507.5 ms (472.9k rows/s)** | 16.36x | 12.88x |
| **16 Threads** | 480,000 | 146.0 MB | 16,871.3 ms *(28.5k rows/s)* | 12,220.9 ms *(39.3k rows/s)* | **987.9 ms (485.9k rows/s)** | 17.08x | 12.37x |
| **32 Threads** | 960,000 | 292.0 MB | 33,914.3 ms *(28.3k rows/s)* | 27,405.7 ms *(35.0k rows/s)* | **1,957.4 ms (490.4k rows/s)** | 17.33x | 14.00x |

*Notes on table metrics:*
- **Speedup vs Traditional**: Ratio of execution time of standard Python row iteration over the Direct Wire C Extension.
- **Speedup vs Pure-Python**: Ratio of execution time of pure-Python Arrow conversion over the Direct Wire C Extension.

---

### 2. Pure CPU Parsing Throughput
- **Environment**: GCE `n2-standard-8` VM in `europe-north1-a`.
- **Metric**: Time to decode pre-fetched protobuf wire payloads into Arrow record batches (network latency excluded).

| Workload | Pure-Python Arrow | Direct Wire C Extension | Speedup vs Pure-Python |
| :--- | :---: | :---: | :---: |
| **10,000 rows (Single Thread)** | 87.54 ms *(114k rows/s)* | **7.43 ms (1.35M rows/s)** | 11.8x |
| **50,000 rows (Single Thread)** | 447.41 ms *(112k rows/s)* | **35.69 ms (1.40M rows/s)** | 12.5x |
| **100,000 rows (Single Thread)** | 889.09 ms *(112k rows/s)* | **77.34 ms (1.29M rows/s)** | 11.5x |
| **800,000 rows (8 Threads Parallel)** | 7,236.89 ms *(111k rows/s)* | **165.70 ms (4.83M rows/s)** | 43.7x |
