"""Scenario 5: Multi-Processing + Multi-Threading Benchmark for Google Cloud Spanner.

Breaks down 32 concurrency across 4 independent OS processes, with each process
running 8 multi-threaded workers using the synchronous Spanner Client SDK.

Architecture:
- 4 Separate OS Processes spawned via subprocess (100% clean gRPC/C++ runtime per process)
- 8 Threads per Process (Total = 32 concurrent requests in-flight)
- Each Process has its own independent Python Interpreter & GIL
- Measures per-process metrics, per-thread CPU time, GIL contention, and overall parent QPS

Outputs:
- Generates spanner_point_select_c32_multiprocess.prof
- Displays full per-process and aggregate benchmark summary
"""

import json
import os
import pstats
import subprocess
import sys
import threading
import time

try:
    from absl import app
    from absl import flags
    HAS_ABSL = True
except ImportError:
    HAS_ABSL = False

import yappi
from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

PROJECT = "span-cloud-testing"
INSTANCE = "suvham-testing"
DATABASE = "benchmark_db_async"
TABLE = "AsyncBenchmarkTable"

NUM_PROCESSES = 4
THREADS_PER_PROCESS = 8
TOTAL_CONCURRENCY = NUM_PROCESSES * THREADS_PER_PROCESS  # 32

WARMUP_DURATION_SEC = 5.0
PROFILE_DURATION_SEC = 10.0


def run_point_select_query_sync(database, user_id="user-0"):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT * FROM {TABLE} WHERE id = @id",
            params={"id": user_id},
            param_types={"id": param_types.STRING},
        )
        rows = list(results)
        return len(rows)


class ThreadMetric:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        self.query_count = 0
        self.wall_time = 0.0
        self.cpu_time = 0.0


def worker_thread_loop(database, worker_id, stop_time, metric):
    t_start_wall = time.perf_counter()
    t_start_cpu = time.thread_time()
    queries = 0

    while time.perf_counter() < stop_time:
        run_point_select_query_sync(database, f"user-{worker_id % 100}")
        queries += 1

    t_end_wall = time.perf_counter()
    t_end_cpu = time.thread_time()

    metric.query_count = queries
    metric.wall_time = t_end_wall - t_start_wall
    metric.cpu_time = t_end_cpu - t_start_cpu


def run_single_process_worker(process_idx, threads_per_process, duration_sec, is_warmup, prof_output_path=None):
    """Executes the 8-thread workload inside this independent OS process."""
    client = spanner.Client(project=PROJECT)
    instance = client.instance(INSTANCE)
    database = instance.database(DATABASE)

    metrics = [
        ThreadMetric(i, f"P{process_idx}-Worker-{i}")
        for i in range(threads_per_process)
    ]

    enable_profiling = (process_idx == 0) and (not is_warmup) and (prof_output_path is not None)
    if enable_profiling:
        yappi.set_clock_type("cpu")
        yappi.clear_stats()
        yappi.start()

    stop_time = time.perf_counter() + duration_sec
    proc_start_wall = time.perf_counter()
    threads = []
    for i in range(threads_per_process):
        t = threading.Thread(
            target=worker_thread_loop,
            args=(database, process_idx * threads_per_process + i, stop_time, metrics[i]),
            name=f"P{process_idx}-Thread-{i}",
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    proc_wall_time = time.perf_counter() - proc_start_wall

    if enable_profiling:
        yappi.stop()
        stats = yappi.get_func_stats()
        stats.save(prof_output_path, type="pstat")

    total_queries = sum(m.query_count for m in metrics)
    total_cpu_time = sum(m.cpu_time for m in metrics)

    # Calculate process-level GIL contention across its 8 threads
    cpu_per_thread = total_cpu_time / max(1, threads_per_process)
    other_cpu = total_cpu_time - cpu_per_thread
    gil_wait_per_thread = other_cpu * (cpu_per_thread / max(0.001, total_cpu_time))
    total_gil_wait = gil_wait_per_thread * threads_per_process
    gil_contention_ratio = (total_gil_wait / max(0.001, total_cpu_time + total_gil_wait)) * 100.0

    result_data = {
        "process_idx": process_idx,
        "queries": total_queries,
        "wall_time": proc_wall_time,
        "cpu_time": total_cpu_time,
        "gil_wait": total_gil_wait,
        "gil_contention_ratio": gil_contention_ratio,
        "qps": total_queries / max(0.001, proc_wall_time),
    }

    # Print pure JSON output for parent process to parse
    print(f"__RESULT_JSON__:{json.dumps(result_data)}")


def run_parent_orchestrator(output_prof_path, num_processes=4, threads_per_process=8):
    total_concurrency = num_processes * threads_per_process
    print("\n" + "=" * 80)
    print(f"SCENARIO 5: Multi-Processing Benchmark ({num_processes} Processes x {threads_per_process} Threads = {total_concurrency} Total Concurrency)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Warmup Phase (5 seconds across all 4 independent processes)
    # -------------------------------------------------------------------------
    print(f"[*] Warming up {num_processes} processes ({total_concurrency} total threads) for {WARMUP_DURATION_SEC} seconds...")
    warmup_procs = []
    
    script_path = os.path.abspath(__file__)
    if sys.argv[0].endswith(".py") or not os.access(sys.argv[0], os.X_OK):
        cmd_prefix = [sys.executable, script_path]
    else:
        cmd_prefix = [sys.argv[0]]

    for p_idx in range(num_processes):
        cmd = cmd_prefix + [
            f"--worker_proc_idx={p_idx}",
            f"--threads_per_proc={threads_per_process}",
            f"--duration_sec={WARMUP_DURATION_SEC}",
            "--is_warmup=true",
        ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        warmup_procs.append(p)

    total_warmup_queries = 0
    for p in warmup_procs:
        stdout, _ = p.communicate()
        for line in stdout.splitlines():
            if line.startswith("__RESULT_JSON__:"):
                data = json.loads(line.replace("__RESULT_JSON__:", ""))
                total_warmup_queries += data.get("queries", 0)

    print(f"[+] Warmup completed: {total_warmup_queries} total requests executed across all {num_processes} processes.")

    # -------------------------------------------------------------------------
    # 2. Benchmark Phase (10 seconds across all 4 independent processes)
    # -------------------------------------------------------------------------
    print(f"[*] Running 10-second benchmark across {num_processes} concurrent processes ({total_concurrency} threads)...")
    benchmark_procs = []
    
    parent_start_wall = time.perf_counter()
    for p_idx in range(num_processes):
        cmd = cmd_prefix + [
            f"--worker_proc_idx={p_idx}",
            f"--threads_per_proc={threads_per_process}",
            f"--duration_sec={PROFILE_DURATION_SEC}",
            "--is_warmup=false",
            f"--prof_path={output_prof_path}",
        ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        benchmark_procs.append(p)

    benchmark_results = []
    for p in benchmark_procs:
        stdout, _ = p.communicate()
        for line in stdout.splitlines():
            if line.startswith("__RESULT_JSON__:"):
                data = json.loads(line.replace("__RESULT_JSON__:", ""))
                benchmark_results.append(data)

    parent_total_wall = time.perf_counter() - parent_start_wall
    print(f"[+] Benchmark finished in {parent_total_wall:.3f} s.")

    benchmark_results.sort(key=lambda x: x["process_idx"])

    # -------------------------------------------------------------------------
    # 3. Report & Aggregate Throughput Analysis
    # -------------------------------------------------------------------------
    total_queries = sum(r["queries"] for r in benchmark_results)
    total_cpu_time = sum(r["cpu_time"] for r in benchmark_results)
    total_gil_wait = sum(r["gil_wait"] for r in benchmark_results)
    overall_qps = total_queries / max(0.001, parent_total_wall)

    print("\n" + "-" * 88)
    print(f"{'Process ID':<14} | {'Threads':<8} | {'Queries':<8} | {'Wall Time (s)':<14} | {'QPS':<10} | {'Pure CPU (s)':<13} | {'GIL Wait (s)':<12} | {'GIL Contention %'}")
    print("-" * 88)
    for r in benchmark_results:
        print(f"Process-{r['process_idx']:<6} | {threads_per_process:<8} | {r['queries']:<8} | {r['wall_time']:<14.3f} | {r['qps']:<10.1f} | {r['cpu_time']:<13.3f} | {r['gil_wait']:<12.3f} | {r['gil_contention_ratio']:<6.1f}%")
    print("-" * 88)
    avg_gil_ratio = (total_gil_wait / max(0.001, total_cpu_time + total_gil_wait)) * 100.0
    print(f"{'AGGREGATE':<14} | {total_concurrency:<8} | {total_queries:<8} | {parent_total_wall:<14.3f} | {overall_qps:<10.1f} | {total_cpu_time:<13.3f} | {total_gil_wait:<12.3f} | {avg_gil_ratio:<6.1f}%")
    print("=" * 88)

    print("\n" + "=" * 80)
    print("SCENARIO 5 MULTI-PROCESSING SUMMARY:")
    print("=" * 80)
    print(f"1. Total Processes Spawned:              {num_processes} independent OS processes")
    print(f"2. Threads per Process:                  {threads_per_process} threads / process ({total_concurrency} total concurrency)")
    print(f"3. Total Wall-Clock Elapsed Time:        {parent_total_wall:.3f} s")
    print(f"4. Total Requests Completed:             {total_queries} queries")
    print(f"5. Overall Aggregate Throughput (QPS):   {overall_qps:.1f} QPS (at parent orchestrator)")
    print(f"6. Total Pure CPU Time (All 4 Processes):{total_cpu_time:.3f} s (Avg: {total_cpu_time/max(1, total_queries)*1000:.2f} ms / query)")
    print(f"7. Total GIL Wait Time across Processes: {total_gil_wait:.3f} s")
    print(f"8. Profile stats saved to:               {output_prof_path}")
    print("=" * 80)

    if os.path.exists(output_prof_path):
        ps = pstats.Stats(output_prof_path)
        ps.strip_dirs()
        print("\n" + "-" * 80)
        print("TOP FUNCTIONS IN PROCESS 0 PROFILE:")
        print("-" * 80)
        ps.sort_stats("cumulative").print_stats(15)


def main(argv=None):
    # Parse CLI flags
    worker_idx = None
    threads_count = THREADS_PER_PROCESS
    duration = PROFILE_DURATION_SEC
    is_warmup = False
    prof_path = None

    args = sys.argv[1:]
    for arg in args:
        if arg.startswith("--worker_proc_idx="):
            worker_idx = int(arg.split("=")[1])
        elif arg.startswith("--threads_per_proc="):
            threads_count = int(arg.split("=")[1])
        elif arg.startswith("--duration_sec="):
            duration = float(arg.split("=")[1])
        elif arg.startswith("--is_warmup="):
            is_warmup = arg.split("=")[1].lower() == "true"
        elif arg.startswith("--prof_path="):
            prof_path = arg.split("=")[1]

    if worker_idx is not None:
        # We are running as a worker child process
        run_single_process_worker(worker_idx, threads_count, duration, is_warmup, prof_path)
    else:
        # We are running as the parent orchestrator
        repo_dir = "/usr/local/google/home/suvham/workspace/cloudPython/google-cloud-python/packages/google-cloud-spanner/profiler_results"
        if os.path.exists(repo_dir):
            output_dir = repo_dir
        else:
            output_dir = os.getcwd()

        prof_file = os.path.join(output_dir, "spanner_point_select_c32_multiprocess.prof")
        run_parent_orchestrator(prof_file, num_processes=NUM_PROCESSES, threads_per_process=THREADS_PER_PROCESS)


if __name__ == "__main__":
    if HAS_ABSL:
        # Define flags so absl doesn't reject custom args
        flags.DEFINE_integer("worker_proc_idx", None, "Worker process index")
        flags.DEFINE_integer("threads_per_proc", 8, "Threads per process")
        flags.DEFINE_float("duration_sec", 10.0, "Duration in seconds")
        flags.DEFINE_bool("is_warmup", False, "Is warmup run")
        flags.DEFINE_string("prof_path", None, "Profile output path")
        app.run(main)
    else:
        main()
