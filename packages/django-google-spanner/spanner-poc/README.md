# Spanner Native GIL-Releasing POC

## 1. Executive Summary

This Proof of Concept (POC) demonstrates how replacing the gRPC hot path in the Python Google Cloud Spanner client library with a native Rust extension completely breaks through the ~1000 QPS (Queries Per Second) throughput ceiling. In high-concurrency Python applications, threads spend a significant portion of their execution time waiting for the Global Interpreter Lock (GIL) to perform CPU-heavy serialization and deserialization of Protobuf payloads. By delegating serialization, network dispatch, and deserialization to a compiled Rust extension that releases the GIL, this POC allows multiple threads to run completely in parallel on multi-core systems. The result is linear throughput scaling that shifts the bottleneck from artificial Python-level lock contention to actual network and database hardware capacity.

---

## 2. Prerequisites

Before executing the setup script, ensure your environment meets the following requirements:
- **Python**: 3.9 or newer, with `pip` and a virtual environment manager installed and activated.
- **System Utilities**: `curl`, `git`, and a package manager (`apt-get`, `yum`, `dnf`, or `brew`) with sudo permissions to install `sysstat` for CPU core metrics monitoring.
- **Access**: Direct network connection to a Google Cloud Spanner instance (a real database is required rather than the local emulator to ensure realistic network and transport latency).

---

## 3. Configuration

Before running the POC, you must update `benchmark.py` with your Google Cloud Spanner instance details.

Open [benchmark.py](file:///Users/suvham/workspace/cloudPython/google-cloud-python/packages/django-google-spanner/spanner-poc/benchmark.py) and update the configuration block at the top:

```python
# Configure your real GCP details here
PROJECT  = "your-project"
INSTANCE = "your-instance"
DATABASE = "your-database"
TABLE    = "your-table"
```

Ensure your active shell has appropriate Google Cloud credentials configured (e.g., via `gcloud auth application-default login` or the `GOOGLE_APPLICATION_CREDENTIALS` environment variable).

---

## 4. Running the POC

The entire installation and execution flow is fully automated:

1. Make the orchestrator script executable:
   ```bash
   chmod +x setup_and_run.sh
   ```
2. Run the script:
   ```bash
   ./setup_and_run.sh
   ```

### CPU Monitoring (Highly Recommended)
To verify that Rust actually spreads the workload across multiple CPU cores:
1. Open a parallel terminal session.
2. Make the CPU monitor executable:
   ```bash
   chmod +x capture_cpu.sh
   ```
3. Run the CPU capture script during the benchmarks:
   ```bash
   ./capture_cpu.sh
   ```
4. Inspect `cpu_during_benchmark.log` after completion to see per-core utilization.

---

## 5. Understanding the Results

Upon execution, `benchmark.py` will print a live comparison table that scales through different thread counts:

```
=====================================================================================
 Threads  |  Method  |    QPS     |  p50 (ms)  |  p95 (ms)  |  p99 (ms)  |  Speedup 
=====================================================================================
    1     |  Python  |    250.0   |     3.95   |     4.50   |     5.20   |    -     
    1     |   Rust   |    265.0   |     3.70   |     4.10   |     4.80   |   1.06x  
-------------------------------------------------------------------------------------
   ...    |   ...    |     ...    |      ...   |      ...   |      ...   |    ...   
-------------------------------------------------------------------------------------
   32     |  Python  |    950.0   |    28.50   |    34.10   |    42.00   |    -     
   32     |   Rust   |   6800.0   |     4.20   |     4.80   |     5.90   |   7.16x  
=====================================================================================
```

### Pattern to Look For
- **QPS Ceiling**: Observe how the Python client hits a hard throughput limit. While standard Python synchronous APIs hit a very low ceiling (often ~300-500 QPS due to heavy GIL lock-contention and thread-switching overhead), even Python's recently introduced asynchronous (asyncio) APIs are capped at a hard limit of ~1000 QPS due to the CPU-intensive serialization/deserialization work being serialized on a single event loop thread. Meanwhile, the Rust client scales near-linearly, breaking through all of these ceilings as thread counts grow.
- **p99 Latency**: Notice that the Python client's p99 latency increases exponentially at higher thread counts due to threads waiting in a queue for the GIL. The Rust client's p99 latency remains flat because requests are processed in parallel.
- **Speedup Factor**: A final summary will report the peak throughput speedup achieved by the Rust extension.


---

## 6. How It Works

CPython runs on a single-threaded execution model enforced by the Global Interpreter Lock (GIL). Even when using multiple threads, only one thread can serialize Python objects to Protobuf binary format or deserialize the database response back into Python objects at any one moment. This means CPU execution is strictly serialized.

```
Python Threads (Standard gRPC Call):
Thread 1: [Serialize (GIL)] ====[ Network Wait (GIL Released) ]==== [Deserialize (GIL)]
Thread 2:                  [GIL Queue...] [Serialize (GIL)] ====[ Network Wait ]==== [GIL Queue...] [Deserialize]
```

Our Rust Native Extension completely removes these CPU-heavy stages from GIL contention:

```
Python Threads (Rust Native Extension):
Thread 1: [Call Rust] (GIL Released) ===[ Rust Serializes -> gRPC -> Rust Deserializes ]=== [Return Python Object]
Thread 2:       [Call Rust] (GIL Released) ===[ Rust Serializes -> gRPC -> Rust Deserializes ]=== [Return]
```

1. **GIL Release**: Before starting any work, the Rust code calls `py.allow_threads()`, instantly giving up the CPython interpreter lock.
2. **Parallel Execution**: Rust compiles the Protobuf structures, constructs the TLS network packet, and handles the HTTP/2 request streams inside a multi-threaded Tokio async runtime. Since the GIL is released, any number of threads can do this in parallel across all available system CPU cores.
3. **GIL Reacquisition**: The Rust extension reacquires the GIL only at the very end, converting the final structured Rust arrays into standard Python list objects in a single rapid step.

---

## 7. Limitations of this POC vs Production

This is a highly optimized Proof of Concept designed strictly to prove the performance thesis. It contains several architectural shortcuts that make it unsuitable for immediate production use:
- **Session Pool Hack**: Reuses the Python session pool via a snapshot checkout trick to borrow session strings on every request. A production library would manage its own native, highly efficient session pool in Rust.
- **Read-Only**: Only supports executing simple single read-only SQL queries. It lacks full transaction capabilities, parameterized inputs, and read-write sessions.
- **Basic Errors**: Contains simplified gRPC error handling and lacks automatic retry policies for transient network drops.
- **Target Architecture**: Built primarily to run on x86_64 Linux distributions.
- **Auth Refresh**: Relies on Python to fetch and periodically update OAuth2 tokens, passing them down as simple headers.

---

## 8. Production Roadmap

A complete production-grade integration would expand on this architecture by:
1. Implementing a fully asynchronous, lock-free Spanner Session Pool in Rust, reducing checkout latency.
2. Porting the entire transaction lifecycle (Read/Write, Batch, Partitioned DML) into PyO3 bindings.
3. Supporting robust error classification and client-side retries (like Spanner's standard backoff retry policy).
4. Bundling cross-platform wheels (`manylinux`, `macos`, `windows`) using `maturin` on GitHub Actions CI.
