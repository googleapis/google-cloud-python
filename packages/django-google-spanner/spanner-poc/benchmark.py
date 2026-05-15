import json
import multiprocessing
import platform
import sys
import time
import threading
import numpy as np
from poc_bridge import NativeSpannerDatabase

# ════════════════════════════════════════════════════════════════
# BENCHMARK CONFIGURATION — USER TO FILL THESE IN
# ════════════════════════════════════════════════════════════════
PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"


# The benchmark SQL query targets a simple single-row fetch
SQL = f"SELECT * FROM {TABLE} LIMIT 1"

WARMUP_S = 10       # Connection and connection-pool warm-up period
DURATION_S = 30     # Duration of each concurrency run in seconds
THREAD_COUNTS = [1, 2, 4, 8, 16, 32]


def run_benchmark(execute_fn, sql_query, thread_count, duration_s):
    """Launches concurrent execution loops across multiple Python threads and gathers metrics."""
    stop_event = threading.Event()
    latencies = []
    latency_lock = threading.Lock()
    error_count = 0
    error_lock = threading.Lock()

    def worker():
        nonlocal error_count
        while not stop_event.is_set():
            start_time = time.perf_counter()
            try:
                _ = execute_fn(sql_query)
                latency = (time.perf_counter() - start_time) * 1000.0  # ms
                with latency_lock:
                    latencies.append(latency)
            except Exception as e:
                with error_lock:
                    error_count += 1

    # Start worker threads
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.daemon = True
        threads.append(t)
        t.start()

    # Let benchmark run for requested duration
    start_bench = time.perf_counter()
    time.sleep(duration_s)
    stop_event.set()

    # Join all worker threads
    for t in threads:
        t.join(timeout=2.0)

    elapsed = time.perf_counter() - start_bench
    total_requests = len(latencies) + error_count

    if len(latencies) == 0:
        return {
            "qps": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "p99": 0.0,
            "error_rate": 1.0,
            "total_requests": total_requests,
        }

    latencies_arr = np.array(latencies)
    return {
        "qps": len(latencies) / elapsed,
        "p50": float(np.percentile(latencies_arr, 50)),
        "p95": float(np.percentile(latencies_arr, 95)),
        "p99": float(np.percentile(latencies_arr, 99)),
        "error_rate": error_count / total_requests if total_requests > 0 else 0.0,
        "total_requests": total_requests,
    }


def main():
    # Check if configuration placeholders are unchanged
    if any(
        val in ["your-project", "your-instance", "your-database", "your-table"]
        for val in [PROJECT, INSTANCE, DATABASE, TABLE]
    ):
        print("=" * 70)
        print("ERROR: Please edit benchmark.py to configure your actual GCP details:")
        print(f"  PROJECT  = '{PROJECT}'")
        print(f"  INSTANCE = '{INSTANCE}'")
        print(f"  DATABASE = '{DATABASE}'")
        print(f"  TABLE    = '{TABLE}'")
        print("=" * 70)
        sys.exit(1)

    print("=" * 70)
    print("GOOGLE CLOUD SPANNER HIGH-THROUGHPUT GIL-RELEASE BENCHMARK")
    print("=" * 70)
    print(f"Python Version : {platform.python_version()}")
    print(f"System CPUs    : {multiprocessing.cpu_count()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Target Query   : {SQL}")
    print(f"Warmup Duration: {WARMUP_S}s")
    print(f"Run Duration   : {DURATION_S}s per configuration")
    print("-" * 70)

    print("Connecting and initializing Spanner pool...")
    db = NativeSpannerDatabase(PROJECT, INSTANCE, DATABASE)

    # Warmup both channels
    print(f"Initiating {WARMUP_S}s warmup phase for Python & Rust paths...")
    _ = run_benchmark(db.execute_sql_python, SQL, thread_count=4, duration_s=WARMUP_S)
    _ = run_benchmark(db.execute_sql_native, SQL, thread_count=4, duration_s=WARMUP_S)
    print("Warmup complete. Starting benchmarks...")

    results = []

    print("\n" + "=" * 85)
    print(
        f"{'Threads':^8} | {'Method':^8} | {'QPS':^10} | {'p50 (ms)':^10} | {'p95 (ms)':^10} | {'p99 (ms)':^10} | {'Speedup':^8}"
    )
    print("=" * 85)

    for threads in THREAD_COUNTS:
        # 1. Python Baseline
        py_res = run_benchmark(db.execute_sql_python, SQL, thread_count=threads, duration_s=DURATION_S)
        print(
            f"{threads:^8} | {'Python':^8} | {py_res['qps']:10.1f} | {py_res['p50']:10.2f} | {py_res['p95']:10.2f} | {py_res['p99']:10.2f} | {'-':^8}"
        )

        # 2. Rust Native extension
        rust_res = run_benchmark(db.execute_sql_native, SQL, thread_count=threads, duration_s=DURATION_S)
        speedup = rust_res["qps"] / py_res["qps"] if py_res["qps"] > 0 else 0.0
        print(
            f"{threads:^8} | {'Rust':^8} | {rust_res['qps']:10.1f} | {rust_res['p50']:10.2f} | {rust_res['p95']:10.2f} | {rust_res['p99']:10.2f} | {speedup:7.2f}x"
        )
        print("-" * 85)

        results.append({
            "threads": threads,
            "python": py_res,
            "rust": rust_res,
            "speedup": speedup,
        })

    # Analyze & Summarize
    py_peak = max(r["python"]["qps"] for r in results)
    py_peak_threads = next(r["threads"] for r in results if r["python"]["qps"] == py_peak)

    rust_peak = max(r["rust"]["qps"] for r in results)
    rust_peak_threads = next(r["threads"] for r in results if r["rust"]["qps"] == rust_peak)

    peak_speedup = max(r["speedup"] for r in results)
    peak_speedup_threads = next(r["threads"] for r in results if r["speedup"] == peak_speedup)

    print("\n" + "=" * 70)
    print("BENCHMARK RESULTS SUMMARY")
    print("=" * 70)
    print(f"Python Peak Throughput: {py_peak:.1f} QPS (at {py_peak_threads} threads)")
    print(f"Rust POC Peak Throughput: {rust_peak:.1f} QPS (at {rust_peak_threads} threads)")
    print(f"Peak Speedup Achieved : {peak_speedup:.2f}x (at {peak_speedup_threads} threads)")
    print("=" * 70)

    # Write results to file
    with open("benchmark_results.json", "w") as f:
        json.dump(
            {
                "system_info": {
                    "python": platform.python_version(),
                    "cpus": multiprocessing.cpu_count(),
                    "platform": platform.platform(),
                },
                "config": {
                    "query": SQL,
                    "duration_seconds": DURATION_S,
                },
                "runs": results,
            },
            f,
            indent=2,
        )
    print("Full JSON report successfully saved to benchmark_results.json.")


if __name__ == "__main__":
    main()
