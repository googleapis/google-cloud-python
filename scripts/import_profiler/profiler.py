import sys
import json
import time
import subprocess
import statistics
import tracemalloc
import importlib

def run_worker(target_module):
    """Performs ONE import and returns metrics."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # --- TARGET IMPORT ---
    # Eagerly load the specified module
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

def run_master(iterations, target_module):
    """Orchestrates the benchmark."""
    times, memories = [], []
    
    print(f"Profiling start... Running {iterations} cold-start iterations for {target_module}.")
    
    for i in range(iterations):
        # Spawn 'self' as a worker using the '--worker' flag
        # sys.executable ensures we use the correct environment's python
        result = subprocess.run(
            [sys.executable, __file__, "--worker", f"--module={target_module}"],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        times.append(data["time_ms"])
        memories.append(data["peak_ram_mb"])
        
    print(f"\n--- Results for {target_module} ({iterations} iterations) ---")
    print(f"Time (ms):")
    print(f"  Median: {statistics.median(times):.2f}")
    print(f"  Mean:   {statistics.mean(times):.2f}")
    print(f"  Min:    {min(times):.2f}")
    print(f"  Max:    {max(times):.2f}")
    if len(times) > 1:
        print(f"  StdDev: {statistics.stdev(times):.2f}")
        
    print(f"RAM (MB):")
    print(f"  Median: {statistics.median(memories):.2f}")
    print(f"  Mean:   {statistics.mean(memories):.2f}")
    print(f"  Min:    {min(memories):.2f}")
    print(f"  Max:    {max(memories):.2f}")
    if len(memories) > 1:
        print(f"  StdDev: {statistics.stdev(memories):.2f}")

def run_trace(target_module):
    """Generates importtime trace log and writes it to a file."""
    trace_file = f"import_trace_{target_module.replace('.', '_')}.log"
    print(f"Generating importtime trace log for {target_module} -> {trace_file}...")
    
    # We run: python -X importtime -c "import <module>"
    # Note that -X importtime writes to stderr
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
    
    for arg in sys.argv[1:]:
        if arg.startswith("--module="):
            target_module = arg.split("=")[1]
        elif arg.startswith("--iterations="):
            iterations = int(arg.split("=")[1])
        elif arg == "--trace":
            trace = True
            
    if "--worker" in sys.argv:
        run_worker(target_module)
    elif trace:
        run_trace(target_module)
    else:
        run_master(iterations, target_module)