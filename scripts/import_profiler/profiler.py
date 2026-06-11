import sys
import json
import time
import subprocess
import statistics
import tracemalloc
import importlib
import csv
import os

def run_worker(target_module):
    """Performs ONE import and returns metrics."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # --- TARGET IMPORT ---
    importlib.import_module(target_module)
    # ---------------------
    
    end_time = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Output to stdout for the Master to capture
    print(json.dumps({
        "time_ms": (end_time - start_time) * 1000,
        "peak_ram_mb": peak / (1024 * 1024)
    }))

def run_master(iterations, target_module, cpu="0", csv_path=None):
    """Orchestrates the benchmark."""
    times, memories = [], []
    
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
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            times.append(data["time_ms"])
            memories.append(data["peak_ram_mb"])
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Fallback if taskset is not found or fails
            if cpu.lower() != "none" and i == 0:
                print("WARNING: taskset CPU pinning failed or is not available. Falling back to unpinned execution...")
                # Try running without taskset
                cmd = [sys.executable, __file__, "--worker", f"--module={target_module}"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                times.append(data["time_ms"])
                memories.append(data["peak_ram_mb"])
                cpu = "none" # Disable cpu pinning for remaining iterations
            else:
                raise e
        
    # Write CSV if requested
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Iteration", "Time (ms)", "Peak RAM (MB)"])
            for idx, (t, m) in enumerate(zip(times, memories)):
                writer.writerow([idx + 1, f"{t:.2f}", f"{m:.4f}"])
        print(f"Raw metrics successfully exported to CSV: {csv_path}")

    # Compute percentiles (P50, P90, P99)
    # statistics.quantiles returns 99 cut points for n=100
    q_time = statistics.quantiles(times, n=100)
    q_mem = statistics.quantiles(memories, n=100)
    
    p50_time, p90_time, p99_time = q_time[49], q_time[89], q_time[98]
    p50_mem, p90_mem, p99_mem = q_mem[49], q_mem[89], q_mem[98]

    print(f"\n--- Results for {target_module} ({iterations} iterations) ---")
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
    
    with open(trace_file, "w") as f:
        f.write(result.stderr)
        
    print(f"Trace log successfully written to {trace_file}")

if __name__ == "__main__":
    # Parse CLI arguments
    target_module = "google.cloud.compute"
    iterations = 50
    trace = False
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
            
    if "--worker" in sys.argv:
        run_worker(target_module)
    elif trace:
        run_trace(target_module)
    else:
        run_master(iterations, target_module, cpu, csv_path)