import sys
import json
import time
import subprocess
import statistics
import tracemalloc
import importlib
import importlib.util
import csv
import os
import logging
import shutil
import pathlib

def clean_bytecode():
    """Recursively deletes all __pycache__ directories and .pyc files to ensure disk-level cold starts."""
    print("Sweeping directory to delete __pycache__ and force bytecode recompilation...")
    count = 0
    for p in pathlib.Path('.').rglob('__pycache__'):
        if p.is_dir():
            shutil.rmtree(p)
            count += 1
    for p in pathlib.Path('.').rglob('*.pyc'):
        if p.is_file():
            p.unlink()
            count += 1
    print(f"Cleared {count} cached bytecode locations.")

def get_rss_mb():
    """Gets current Resident Set Size (physical memory) in MB. Linux only."""
    try:
        with open('/proc/self/statm', 'r') as f:
            rss_pages = int(f.read().split()[1])
            page_size = os.sysconf('SC_PAGE_SIZE')
            return (rss_pages * page_size) / (1024 * 1024)
    except Exception:
        return 0.0

def run_worker(target_module):
    """Performs ONE import and returns metrics."""
    tracemalloc.start()
    importlib.invalidate_caches()
    sys.path_importer_cache.clear()
    rss_before = get_rss_mb()
    modules_before = set(sys.modules.keys())
    
    # We start the high-resolution timer from *inside* the already-booted worker process.
    # This explicitly isolates the pure import latency and entirely omits the 
    # 10ms-50ms Python VM interpreter startup overhead that would skew the metrics.
    start_time = time.perf_counter()
    
    # --- TARGET IMPORT ---
    importlib.import_module(target_module)
    # ---------------------
    
    end_time = time.perf_counter()
    rss_after = get_rss_mb()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    modules_after = set(sys.modules.keys())
    new_modules = modules_after - modules_before
    
    loaded_lines = 0
    for m in new_modules:
        mod = sys.modules.get(m)
        if mod and getattr(mod, '__file__', None):
            file_path = mod.__file__
            if file_path.endswith('.pyc'):
                try:
                    file_path = importlib.util.source_from_cache(file_path)
                except ValueError:
                    pass
            if file_path.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        loaded_lines += sum(1 for _ in f)
                except Exception as e:
                    logging.warning(f"Failed to read lines from {file_path}: {e}")
    
    # Output to stdout for the Master to capture
    metrics = {
        "time_ms": (end_time - start_time) * 1000,
        "peak_ram_mb": peak / (1024 * 1024),
        "rss_ram_mb": rss_after - rss_before,
        "loaded_modules": len(new_modules),
        "loaded_lines": loaded_lines
    }
    print(f"__METRICS__:{json.dumps(metrics)}")

def _run_worker_and_parse(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    try:
        lines = result.stdout.strip().splitlines()
        data = None
        for line in reversed(lines):
            if line.startswith("__METRICS__:"):
                data = json.loads(line[len("__METRICS__:"):])
                break
        if data is None:
            raise ValueError("Worker did not output metrics JSON.")
        for key in ("time_ms", "peak_ram_mb", "rss_ram_mb", "loaded_modules", "loaded_lines"):
            if key not in data:
                raise KeyError(f"Missing key '{key}' in worker output")
        return data
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as parse_err:
        print(f"Error parsing worker output: {parse_err}", file=sys.stderr)
        print(f"Worker stdout:\n{result.stdout}", file=sys.stderr)
        print(f"Worker stderr:\n{result.stderr}", file=sys.stderr)
        raise parse_err

def run_master(iterations, target_module, cpu="0", csv_path=None, clear_cache=True):
    """Orchestrates the benchmark."""
    if iterations < 1:
        raise ValueError("Number of iterations must be at least 1.")
    times, memories, rss_memories = [], [], []
    loaded_modules_val, loaded_lines_val = 0, 0
    
    print(f"Profiling start... Running {iterations} cold-start iterations for {target_module}.")
    
    if clear_cache:
        clean_bytecode()
        python_exe = [sys.executable, "-B"] # -B prevents writing .pyc files so every iteration reads raw .py
    else:
        python_exe = [sys.executable]
        
    if cpu.lower() != "none":
        print(f"CPU Pinning enabled: Pinning processes to core {cpu} using taskset.")
    else:
        print("CPU Pinning disabled.")
    
    for i in range(iterations):
        # Build command line
        cmd = []
        if cpu.lower() != "none":
            cmd += ["taskset", "-c", cpu]
        
        cmd += python_exe + [__file__, "--worker", f"--module={target_module}"]
        
        try:
            data = _run_worker_and_parse(cmd)
            times.append(data["time_ms"])
            memories.append(data["peak_ram_mb"])
            rss_memories.append(data["rss_ram_mb"])
            loaded_modules_val = data["loaded_modules"]
            loaded_lines_val = data["loaded_lines"]
        except FileNotFoundError as e:
            if cpu.lower() != "none" and i == 0:
                print("WARNING: taskset CPU pinning is not available. Falling back to unpinned execution...")
                cpu = "none"
                cmd = python_exe + [__file__, "--worker", f"--module={target_module}"]
                try:
                    data = _run_worker_and_parse(cmd)
                    times.append(data["time_ms"])
                    memories.append(data["peak_ram_mb"])
                    rss_memories.append(data["rss_ram_mb"])
                    loaded_modules_val = data["loaded_modules"]
                    loaded_lines_val = data["loaded_lines"]
                except subprocess.CalledProcessError as err:
                    print(f"Error in worker process:\n{err.stderr}", file=sys.stderr)
                    raise err
            else:
                raise e
        except subprocess.CalledProcessError as e:
            print(f"Error in worker process:\n{e.stderr}", file=sys.stderr)
            raise e
        
    # Write CSV if requested
    if csv_path:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Iteration", "Time (ms)", "Tracemalloc RAM (MB)", "RSS Physical RAM (MB)"])
            for idx, (t, m, r) in enumerate(zip(times, memories, rss_memories)):
                writer.writerow([idx + 1, f"{t:.2f}", f"{m:.4f}", f"{r:.4f}"])
        print(f"Raw metrics successfully exported to CSV: {csv_path}")

    # Compute percentiles (P50, P90, P99)
    # statistics.quantiles returns 99 cut points for n=100
    if len(times) > 1:
        q_time = statistics.quantiles(times, n=100)
        p50_time, p90_time, p99_time = q_time[49], q_time[89], q_time[98]
    else:
        p50_time = p90_time = p99_time = times[0] if times else 0.0

    if len(memories) > 1:
        q_mem = statistics.quantiles(memories, n=100)
        p50_mem, p90_mem, p99_mem = q_mem[49], q_mem[89], q_mem[98]
    else:
        p50_mem = p90_mem = p99_mem = memories[0] if memories else 0.0

    if len(rss_memories) > 1:
        q_rss = statistics.quantiles(rss_memories, n=100)
        p50_rss, p90_rss, p99_rss = q_rss[49], q_rss[89], q_rss[98]
    else:
        p50_rss = p90_rss = p99_rss = rss_memories[0] if rss_memories else 0.0

    print(f"\n--- Results for {target_module} ({iterations} iterations) ---")
    print(f"Code Volume (Deterministic):")
    print(f"  Loaded Modules: {loaded_modules_val}")
    print(f"  Loaded Lines:   {loaded_lines_val}")
    print(f"Time (ms):")
    print(f"  P50 (Median): {p50_time:.2f}")
    print(f"  P90:          {p90_time:.2f}")
    print(f"  P99:          {p99_time:.2f}")
    print(f"  Mean:         {statistics.mean(times):.2f}")
    print(f"  Min:          {min(times):.2f}")
    print(f"  Max:          {max(times):.2f}")
    if len(times) > 1:
        print(f"  StdDev:       {statistics.stdev(times):.2f}")
        
    print(f"Tracemalloc RAM (MB):")
    print(f"  P50 (Median): {p50_mem:.4f}")
    print(f"  P90:          {p90_mem:.4f}")
    print(f"  P99:          {p99_mem:.4f}")
    print(f"  Mean:         {statistics.mean(memories):.4f}")
    print(f"  Min:          {min(memories):.4f}")
    print(f"  Max:          {max(memories):.4f}")
    if len(memories) > 1:
        print(f"  StdDev:       {statistics.stdev(memories):.4f}")

    print(f"Physical RSS RAM (MB):")
    print(f"  P50 (Median): {p50_rss:.4f}")
    print(f"  P90:          {p90_rss:.4f}")
    print(f"  P99:          {p99_rss:.4f}")
    print(f"  Mean:         {statistics.mean(rss_memories):.4f}")
    print(f"  Min:          {min(rss_memories):.4f}")
    print(f"  Max:          {max(rss_memories):.4f}")
    if len(rss_memories) > 1:
        print(f"  StdDev:       {statistics.stdev(rss_memories):.4f}")

def run_trace(target_module):
    """Generates importtime trace log and writes it to a file."""
    trace_file = f"import_trace_{target_module.replace('.', '_')}.log"
    print(f"Generating importtime trace log for {target_module} -> {trace_file}...")
    
    # We run: python -X importtime -c "import importlib; importlib.import_module(...)"
    result = subprocess.run(
        [sys.executable, "-X", "importtime", "-c", f"import importlib; importlib.import_module({json.dumps(target_module)})"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"WARNING: Import failed with exit code {result.returncode}. The trace log may be incomplete or contain errors.", file=sys.stderr)
        if result.stdout:
            print(f"Worker stdout:\n{result.stdout}", file=sys.stderr)
        if result.stderr:
            print(f"Worker stderr:\n{result.stderr}", file=sys.stderr)
            
    with open(trace_file, "w", encoding="utf-8") as f:
        f.write(result.stderr)
        
    print(f"Trace log successfully written to {trace_file}")

def run_cprofile(target_module):
    """Runs cProfile in a clean subprocess to capture stack traces for latency."""
    import pstats
    
    prof_file = f"cprofile_{target_module.replace('.', '_')}.prof"
    print(f"Generating cProfile data for {target_module} -> {prof_file}...")
    
    # Run profiling in a clean subprocess to ensure cold-start
    result = subprocess.run(
        [sys.executable, "-m", "cProfile", "-o", prof_file, "-c", f"import importlib; importlib.import_module({json.dumps(target_module)})"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error generating cProfile data:\n{result.stderr}", file=sys.stderr)
        return

    print(f"cProfile stats successfully written to {prof_file}")
    
    # Print top bottlenecks
    print("\n--- Top 15 functions by cumulative time ---")
    ps = pstats.Stats(prof_file).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats(15)

def run_mprofile(target_module):
    """Runs tracemalloc snapshot in a clean subprocess to see where memory is allocated."""
    print(f"Generating tracemalloc memory snapshot for {target_module}...")
    
    code = (
        "import tracemalloc\n"
        "import importlib\n"
        "tracemalloc.start()\n"
        f"importlib.import_module({json.dumps(target_module)})\n"
        "snapshot = tracemalloc.take_snapshot()\n"
        "tracemalloc.stop()\n"
        "top_stats = snapshot.statistics('lineno')\n"
        "for stat in top_stats[:15]:\n"
        "    print(stat)\n"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error generating memory snapshot:\n{result.stderr}", file=sys.stderr)
    else:
        print("\n--- Top 15 memory allocations by line ---")
        print(result.stdout, end="")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python SDK Import Profiler")
    parser.add_argument("--module", default="google.cloud.compute_v1", help="Target module to profile")
    parser.add_argument("--iterations", type=int, default=50, help="Number of iterations")
    default_cpu = "0" if sys.platform.startswith("linux") else "none"
    parser.add_argument("--cpu", default=default_cpu, help="CPU core to pin to (or 'none')")
    parser.add_argument("--csv", help="Path to export CSV results")
    parser.add_argument("--trace", action="store_true", help="Generate importtime trace log")
    parser.add_argument("--cprofile", action="store_true", help="Run cProfile")
    parser.add_argument("--mprofile", action="store_true", help="Run tracemalloc memory snapshot")
    parser.add_argument("--keep-pycache", action="store_true", help="Preserve __pycache__ and allow bytecode execution (Default: False, script automatically sweeps __pycache__ for true cold-starts)")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    
    args = parser.parse_args()
    
    if args.worker:
        run_worker(args.module)
    elif args.trace:
        run_trace(args.module)
    elif args.cprofile:
        run_cprofile(args.module)
    elif args.mprofile:
        if not args.keep_pycache: clean_bytecode()
        run_mprofile(args.module)
    else:
        run_master(args.iterations, args.module, args.cpu, args.csv, not args.keep_pycache)