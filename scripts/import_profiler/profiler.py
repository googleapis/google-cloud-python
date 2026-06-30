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
import shutil
import pathlib
import multiprocessing

NO_CPU_PINNING = -1

def clean_bytecode():
    """Recursively deletes all __pycache__ directories and .pyc files to ensure disk-level cold starts."""
    print("Sweeping directory to delete __pycache__ and force bytecode recompilation...")
    count = 0
    # Walk the directory avoiding hidden directories (e.g. .git, .venv, .nox)
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            dirs.remove('__pycache__')
            count += 1
        for f in files:
            if f.endswith('.pyc'):
                os.remove(os.path.join(root, f))
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
        try:
            file_path = sys.modules[m].__file__
            if not file_path:
                continue

            if file_path.endswith('.pyc'):
                try:
                    file_path = importlib.util.source_from_cache(file_path)
                except ValueError:
                    # Raised if the .pyc path does not follow standard PEP 3147/488 conventions.
                    # We pass silently because the unresolved file_path will still end in '.pyc', 
                    # meaning the subsequent '.endswith('.py')' check will fail and safely skip 
                    # trying to count lines in a binary file.
                    pass
            if file_path.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        loaded_lines += sum(1 for _ in f)
                except OSError as e:
                    print(f"WARNING: Failed to read lines from {file_path}: {e}", file=sys.stderr)
        except KeyError:
            # Module disappeared from sys.modules during execution
            pass
        except AttributeError:
            # Module has no __file__ attribute (likely a C-extension or built-in)
            pass
    
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

def _calculate_percentiles(data_list):
    """Helper method to calculate P50, P90, P99 from a list of numbers."""
    if len(data_list) > 1:
        q = statistics.quantiles(data_list, n=100)
        return q[49], q[89], q[98]
    val = data_list[0] if data_list else 0.0
    return val, val, val

def _print_outputs(target_module, iterations, loaded_modules_val, loaded_lines_val,
                   times, p50_time, p90_time, p99_time,
                   memories, p50_mem, p90_mem, p99_mem,
                   rss_memories, p50_rss, p90_rss, p99_rss):
    """Helper method to format and print the final benchmark results."""
    def _format_stats(title, data, p50, p90, p99, fmt):
        if not data:
            return ""
        std_str = f"  StdDev:       {statistics.stdev(data):{fmt}}\n" if len(data) > 1 else ""
        return f"{title}:\n  P50 (Median): {p50:{fmt}}\n  P90:          {p90:{fmt}}\n  P99:          {p99:{fmt}}\n  Mean:         {statistics.mean(data):{fmt}}\n  Min:          {min(data):{fmt}}\n  Max:          {max(data):{fmt}}\n{std_str}"

    final_output = f"""
--- Results for {target_module} ({iterations} iterations) ---
Code Volume (Deterministic):
  Loaded Modules: {loaded_modules_val}
  Loaded Lines:   {loaded_lines_val}
{_format_stats("Time (ms)", times, p50_time, p90_time, p99_time, ".2f")}
{_format_stats("Tracemalloc RAM (MB)", memories, p50_mem, p90_mem, p99_mem, ".4f")}
{_format_stats("Physical RSS RAM (MB)", rss_memories, p50_rss, p90_rss, p99_rss, ".4f")}"""
    print(final_output.strip())

def run_master(iterations, target_module, cpu=0, csv_path=None, clear_cache=True):
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
        
    if cpu != NO_CPU_PINNING:
        if not sys.platform.startswith("linux"):
            print("WARNING: CPU pinning is only supported on Linux. Falling back to unpinned execution.")
            cpu = NO_CPU_PINNING
        else:
            print(f"CPU Pinning enabled: Pinning processes to core {cpu} using taskset.")
    else:
        print("CPU Pinning disabled.")
    
    for i in range(iterations):
        # Build command line
        cmd = []
        if cpu != NO_CPU_PINNING:
            cmd += ["taskset", "-c", str(cpu)]
        
        cmd += python_exe + [__file__, "--worker", f"--module={target_module}"]
        
        try:
            data = _run_worker_and_parse(cmd)
            times.append(data["time_ms"])
            memories.append(data["peak_ram_mb"])
            rss_memories.append(data["rss_ram_mb"])
            if i > 0 and loaded_modules_val != data["loaded_modules"]:
                print(f"WARNING: Non-deterministic import behavior! Iteration {i+1} loaded {data['loaded_modules']} modules (expected {loaded_modules_val}).", file=sys.stderr)
            if i > 0 and loaded_lines_val != data["loaded_lines"]:
                print(f"WARNING: Non-deterministic import behavior! Iteration {i+1} loaded {data['loaded_lines']} lines (expected {loaded_lines_val}).", file=sys.stderr)
            
            loaded_modules_val = data["loaded_modules"]
            loaded_lines_val = data["loaded_lines"]
        except FileNotFoundError as e:
            if cpu != NO_CPU_PINNING and cmd and cmd[0] == "taskset":
                print("ERROR: 'taskset' command not found. CPU pinning is enabled but taskset is not installed. "
                      "Install taskset or disable pinning by passing --cpu=-1.", file=sys.stderr)
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
    p50_time, p90_time, p99_time = _calculate_percentiles(times)
    p50_mem, p90_mem, p99_mem = _calculate_percentiles(memories)
    p50_rss, p90_rss, p99_rss = _calculate_percentiles(rss_memories)

    _print_outputs(
        target_module, iterations, loaded_modules_val, loaded_lines_val,
        times, p50_time, p90_time, p99_time,
        memories, p50_mem, p90_mem, p99_mem,
        rss_memories, p50_rss, p90_rss, p99_rss
    )

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

def _mprofile_worker(target_module):
    import tracemalloc
    tracemalloc.start()
    importlib.import_module(target_module)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    top_stats = snapshot.statistics('lineno')
    print("\n--- Top 15 memory allocations by line ---")
    for stat in top_stats[:15]:
        print(stat)

def run_mprofile(target_module):
    """Runs tracemalloc snapshot in a clean subprocess to see where memory is allocated."""
    print(f"Generating tracemalloc memory snapshot for {target_module}...")
    
    # Use 'spawn' to ensure a completely clean python process without inherited module caches
    ctx = multiprocessing.get_context("spawn")
    p = ctx.Process(target=_mprofile_worker, args=(target_module,))
    p.start()
    p.join()
    
    if p.exitcode != 0:
        print(f"Error generating memory snapshot, process exited with code {p.exitcode}", file=sys.stderr)

if __name__ == "__main__":
    import argparse

    def validate_module_name(module_name):
        """Validates that the input is a structurally valid Python module identifier to prevent arbitrary code execution."""
        if not all(part.isidentifier() for part in module_name.split('.')):
            raise argparse.ArgumentTypeError(f"'{module_name}' is not a valid Python module identifier.")
        return module_name

    parser = argparse.ArgumentParser(description="Python SDK Import Profiler")
    parser.add_argument("--module", type=validate_module_name, default="google.cloud.compute_v1", help="Target module to profile")
    parser.add_argument("--iterations", type=int, default=50, help="Number of iterations")
    default_cpu = 0 if sys.platform.startswith("linux") else NO_CPU_PINNING
    parser.add_argument("--cpu", type=int, default=default_cpu, help="CPU core to pin to (or -1 for no pinning)")
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
        if not args.keep_pycache: clean_bytecode()
        run_trace(args.module)
    elif args.cprofile:
        if not args.keep_pycache: clean_bytecode()
        run_cprofile(args.module)
    elif args.mprofile:
        if not args.keep_pycache: clean_bytecode()
        run_mprofile(args.module)
    else:
        run_master(args.iterations, args.module, args.cpu, args.csv, not args.keep_pycache)