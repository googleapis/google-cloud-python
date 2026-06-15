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

def run_worker(target_module):
    """Performs ONE import and returns metrics."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    modules_before = set(sys.modules.keys())
    
    # --- TARGET IMPORT ---
    importlib.import_module(target_module)
    # ---------------------
    
    end_time = time.perf_counter()
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
                    with open(file_path, 'r', encoding='utf-8') as f:
                        loaded_lines += sum(1 for _ in f)
                except Exception as e:
                    logging.warning(f"Failed to read lines from {file_path}: {e}")
    
    # Output to stdout for the Master to capture
    print(json.dumps({
        "time_ms": (end_time - start_time) * 1000,
        "peak_ram_mb": peak / (1024 * 1024),
        "loaded_modules": len(new_modules),
        "loaded_lines": loaded_lines
    }))

def _run_worker_and_parse(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    try:
        lines = result.stdout.strip().splitlines()
        if not lines:
            raise ValueError("Worker produced no output on stdout.")
        data = json.loads(lines[-1])
        for key in ("time_ms", "peak_ram_mb", "loaded_modules", "loaded_lines"):
            if key not in data:
                raise KeyError(f"Missing key '{key}' in worker output")
        return data
    except (json.JSONDecodeError, IndexError, KeyError, ValueError) as parse_err:
        print(f"Error parsing worker output: {parse_err}", file=sys.stderr)
        print(f"Worker stdout:\n{result.stdout}", file=sys.stderr)
        print(f"Worker stderr:\n{result.stderr}", file=sys.stderr)
        raise parse_err

def run_master(iterations, target_module, cpu="0", csv_path=None):
    """Orchestrates the benchmark."""
    if iterations < 1:
        raise ValueError("Number of iterations must be at least 1.")
    times, memories = [], []
    loaded_modules_val, loaded_lines_val = 0, 0
    
    print(f"Profiling start... Running {iterations} cold-start iterations for {target_module}.")
    if cpu.lower() != "none":
        print(f"CPU Pinning enabled: Pinning processes to core {cpu} using taskset.")
    else:
        print("CPU Pinning disabled.")
    
    for i in range(iterations):
        # Build command line
        cmd = []
        if cpu.lower() != "none":
            cmd += ["taskset", "-c", cpu]
        
        cmd += [sys.executable, __file__, "--worker", f"--module={target_module}"]
        
        try:
            data = _run_worker_and_parse(cmd)
            times.append(data["time_ms"])
            memories.append(data["peak_ram_mb"])
            loaded_modules_val = data["loaded_modules"]
            loaded_lines_val = data["loaded_lines"]
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fallback if taskset is not found or fails
            if cpu.lower() != "none" and i == 0:
                print("WARNING: taskset CPU pinning failed or is not available. Falling back to unpinned execution...")
                # Try running without taskset
                cmd = [sys.executable, __file__, "--worker", f"--module={target_module}"]
                try:
                    data = _run_worker_and_parse(cmd)
                    times.append(data["time_ms"])
                    memories.append(data["peak_ram_mb"])
                    loaded_modules_val = data["loaded_modules"]
                    loaded_lines_val = data["loaded_lines"]
                    cpu = "none" # Disable cpu pinning for remaining iterations
                except subprocess.CalledProcessError as err:
                    print(f"Error in worker process:\n{err.stderr}", file=sys.stderr)
                    raise err
            else:
                if isinstance(e, subprocess.CalledProcessError):
                    print(f"Error in worker process:\n{e.stderr}", file=sys.stderr)
                raise e
        
    # Write CSV if requested
    if csv_path:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Iteration", "Time (ms)", "Peak RAM (MB)"])
            for idx, (t, m) in enumerate(zip(times, memories)):
                writer.writerow([idx + 1, f"{t:.2f}", f"{m:.4f}"])
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
        
    print(f"RAM (MB):")
    print(f"  P50 (Median): {p50_mem:.4f}")
    print(f"  P90:          {p90_mem:.4f}")
    print(f"  P99:          {p99_mem:.4f}")
    print(f"  Mean:         {statistics.mean(memories):.4f}")
    print(f"  Min:          {min(memories):.4f}")
    print(f"  Max:          {max(memories):.4f}")
    if len(memories) > 1:
        print(f"  StdDev:       {statistics.stdev(memories):.4f}")

def run_trace(target_module):
    """Generates importtime trace log and writes it to a file."""
    trace_file = f"import_trace_{target_module.replace('.', '_')}.log"
    print(f"Generating importtime trace log for {target_module} -> {trace_file}...")
    
    # We run: python -X importtime -c "import <module>"
    result = subprocess.run(
        [sys.executable, "-X", "importtime", "-c", f"import {target_module}"],
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
    """Runs cProfile to capture stack traces for latency."""
    import cProfile
    import pstats
    
    prof_file = f"cprofile_{target_module.replace('.', '_')}.prof"
    print(f"Generating cProfile data for {target_module} -> {prof_file}...")
    
    # Run profiling
    pr = cProfile.Profile()
    pr.enable()
    importlib.import_module(target_module)
    pr.disable()
    
    # Save for flame charts (e.g. via snakeviz)
    pr.dump_stats(prof_file)
    print(f"cProfile stats successfully written to {prof_file}")
    
    # Print top bottlenecks
    print("\n--- Top 15 functions by cumulative time ---")
    ps = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats(15)

def run_mprofile(target_module):
    """Runs tracemalloc snapshot to see where memory is allocated."""
    print(f"Generating tracemalloc memory snapshot for {target_module}...")
    
    tracemalloc.start()
    importlib.import_module(target_module)
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    
    print("\n--- Top 15 memory allocations by line ---")
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:15]:
        print(stat)

if __name__ == "__main__":
    # Parse CLI arguments
    target_module = "google.cloud.compute"
    iterations = 50
    trace = False
    cprofile = False
    mprofile = False
    cpu = "0"
    csv_path = None
    
    for arg in sys.argv[1:]:
        if arg.startswith("--module="):
            target_module = arg.split("=")[1]
        elif arg.startswith("--iterations="):
            iterations = int(arg.split("=")[1])
        elif arg.startswith("--cpu="):
            cpu = arg.split("=")[1]
        elif arg.startswith("--csv="):
            csv_path = arg.split("=")[1]
        elif arg == "--trace":
            trace = True
        elif arg == "--cprofile":
            cprofile = True
        elif arg == "--mprofile":
            mprofile = True
            
    if "--worker" in sys.argv:
        run_worker(target_module)
    elif trace:
        run_trace(target_module)
    elif cprofile:
        run_cprofile(target_module)
    elif mprofile:
        run_mprofile(target_module)
    else:
        run_master(iterations, target_module, cpu, csv_path)