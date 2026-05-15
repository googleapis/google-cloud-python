import json
import multiprocessing
import platform
import sys
import time
import threading
import numpy as np
import psutil
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


class CPUMonitor:
    """Monitors overall CPU utilization and tracks how many cores are actively under use (>10% utility) during a benchmark run."""
    def __init__(self):
        self._stop_event = threading.Event()
        self._cpu_percentages = []
        self._per_cpu_percentages = []
        self._thread = None

    def start(self):
        self._stop_event.clear()
        self._cpu_percentages = []
        self._per_cpu_percentages = []
        # First call initializes psutil counters
        _ = psutil.cpu_percent(interval=None)
        _ = psutil.cpu_percent(interval=None, percpu=True)
        
        def sample_loop():
            while not self._stop_event.is_set():
                time.sleep(0.5)
                self._cpu_percentages.append(psutil.cpu_percent(interval=None))
                self._per_cpu_percentages.append(psutil.cpu_percent(interval=None, percpu=True))

        self._thread = threading.Thread(target=sample_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> tuple:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        if not self._cpu_percentages:
            return 0.0, 0
        
        avg_cpu = float(np.mean(self._cpu_percentages))
        per_cpu_arr = np.array(self._per_cpu_percentages)
        avg_per_core = np.mean(per_cpu_arr, axis=0)
        
        # Count how many CPU cores had > 10% average utilization
        active_cores = int(np.sum(avg_per_core > 10.0))
        
        return avg_cpu, active_cores


def run_benchmark(execute_fn, sql_query, thread_count, duration_s):
    """Launches concurrent execution loops across multiple Python threads and gathers QPS, latency, and CPU utilization metrics."""
    stop_event = threading.Event()
    latencies = []
    latency_lock = threading.Lock()
    error_count = 0
    error_lock = threading.Lock()

    # Start CPU Monitoring
    cpu_monitor = CPUMonitor()
    cpu_monitor.start()

    def worker():
        nonlocal error_count
        while not stop_event.is_set():
            start_time = time.perf_counter()
            try:
                _ = execute_fn(sql_query)
                latency = (time.perf_counter() - start_time) * 1000.0  # ms
                with latency_lock:
                    latencies.append(latency)
            except Exception:
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

    # Stop CPU Monitoring and retrieve averages
    avg_cpu_util, active_cores = cpu_monitor.stop()

    if len(latencies) == 0:
        return {
            "qps": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "p99": 0.0,
            "error_rate": 1.0,
            "total_requests": total_requests,
            "cpu_util": avg_cpu_util,
            "active_cores": active_cores,
        }

    latencies_arr = np.array(latencies)
    return {
        "qps": len(latencies) / elapsed,
        "p50": float(np.percentile(latencies_arr, 50)),
        "p95": float(np.percentile(latencies_arr, 95)),
        "p99": float(np.percentile(latencies_arr, 99)),
        "error_rate": error_count / total_requests if total_requests > 0 else 0.0,
        "total_requests": total_requests,
        "cpu_util": avg_cpu_util,
        "active_cores": active_cores,
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

    print("=" * 115)
    print("GOOGLE CLOUD SPANNER HIGH-THROUGHPUT NATIVE EXTENSION PERFORMANCE BENCHMARK")
    print("=" * 115)
    print(f"Python Version : {platform.python_version()}")
    print(f"System CPUs    : {multiprocessing.cpu_count()}")
    print(f"Platform       : {platform.platform()}")
    print(f"Target Query   : {SQL}")
    print(f"Warmup Duration: {WARMUP_S}s")
    print(f"Run Duration   : {DURATION_S}s per configuration")
    print("-" * 115)

    print("Connecting and initializing Spanner pools...")
    db = NativeSpannerDatabase(PROJECT, INSTANCE, DATABASE)

    # Warmup all channels
    print(f"Initiating {WARMUP_S}s warmup phase for Python & Rust paths...")
    _ = run_benchmark(db.execute_sql_python, SQL, thread_count=4, duration_s=WARMUP_S)
    _ = run_benchmark(db.execute_sql_native, SQL, thread_count=4, duration_s=WARMUP_S)
    _ = run_benchmark(db.execute_sql_native_multi_channel, SQL, thread_count=4, duration_s=WARMUP_S)
    print("Warmup complete. Starting benchmarks...")

    results = []

    print("\n" + "=" * 120)
    print(
        f"{'Threads':^8} | {'Method':^14} | {'QPS':^10} | {'p50 (ms)':^10} | {'p95 (ms)':^10} | {'p99 (ms)':^10} | {'CPU Util':^10} | {'Cores':^6} | {'Speedup':^8}"
    )
    print("=" * 120)

    for threads in THREAD_COUNTS:
        # 1. Python Baseline
        py_res = run_benchmark(db.execute_sql_python, SQL, thread_count=threads, duration_s=DURATION_S)
        print(
            f"{threads:^8} | {'Python':^14} | {py_res['qps']:10.1f} | {py_res['p50']:10.2f} | {py_res['p95']:10.2f} | {py_res['p99']:10.2f} | {py_res['cpu_util']:8.1f}% | {py_res['active_cores']:^6} | {'-':^8}"
        )

        # 2. Rust Native extension (Single Channel)
        rust_res = run_benchmark(db.execute_sql_native, SQL, thread_count=threads, duration_s=DURATION_S)
        speedup = rust_res["qps"] / py_res["qps"] if py_res["qps"] > 0 else 0.0
        print(
            f"{threads:^8} | {'Rust (1 Ch)':^14} | {rust_res['qps']:10.1f} | {rust_res['p50']:10.2f} | {rust_res['p95']:10.2f} | {rust_res['p99']:10.2f} | {rust_res['cpu_util']:8.1f}% | {rust_res['active_cores']:^6} | {speedup:7.2f}x"
        )

        # 3. Rust Native extension (Multi-Channel 4 Connections)
        rust_multi_res = run_benchmark(db.execute_sql_native_multi_channel, SQL, thread_count=threads, duration_s=DURATION_S)
        speedup_multi = rust_multi_res["qps"] / py_res["qps"] if py_res["qps"] > 0 else 0.0
        print(
            f"{threads:^8} | {'Rust (4 Ch)':^14} | {rust_multi_res['qps']:10.1f} | {rust_multi_res['p50']:10.2f} | {rust_multi_res['p95']:10.2f} | {rust_multi_res['p99']:10.2f} | {rust_multi_res['cpu_util']:8.1f}% | {rust_multi_res['active_cores']:^6} | {speedup_multi:7.2f}x"
        )
        print("-" * 120)

        results.append({
            "threads": threads,
            "python": py_res,
            "rust_single": rust_res,
            "rust_multi": rust_multi_res,
            "speedup_single": speedup,
            "speedup_multi": speedup_multi,
        })

    # Analyze & Summarize
    py_peak = max(r["python"]["qps"] for r in results)
    py_peak_threads = next(r["threads"] for r in results if r["python"]["qps"] == py_peak)

    rust_single_peak = max(r["rust_single"]["qps"] for r in results)
    rust_single_peak_threads = next(r["threads"] for r in results if r["rust_single"]["qps"] == rust_single_peak)

    rust_multi_peak = max(r["rust_multi"]["qps"] for r in results)
    rust_multi_peak_threads = next(r["threads"] for r in results if r["rust_multi"]["qps"] == rust_multi_peak)

    peak_speedup = max(r["speedup_multi"] for r in results)
    peak_speedup_threads = next(r["threads"] for r in results if r["speedup_multi"] == peak_speedup)

    print("\n" + "=" * 95)
    print("BENCHMARK RESULTS SUMMARY")
    print("=" * 95)
    print(f"Python Peak Throughput        : {py_peak:.1f} QPS (at {py_peak_threads} threads)")
    print(f"Rust (Single Ch) Peak QPS     : {rust_single_peak:.1f} QPS (at {rust_single_peak_threads} threads)")
    print(f"Rust (Multi-Channel) Peak QPS : {rust_multi_peak:.1f} QPS (at {rust_multi_peak_threads} threads)")
    print(f"Peak Speedup Achieved         : {peak_speedup:.2f}x (at {peak_speedup_threads} threads)")
    print("=" * 95)

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
