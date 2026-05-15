#!/bin/bash

# This script runs in a parallel terminal during benchmarks to track
# and verify that CPU load is distributed across multiple cores rather
# than being bottled up on a single core (which happens with Python due to the GIL).

LOG_FILE="cpu_during_benchmark.log"

echo "=== Spanner POC CPU Capture Started at $(date) ===" > "$LOG_FILE"

if command -v mpstat &> /dev/null; then
    echo "mpstat detected. Recording per-core CPU utilization every 2 seconds..."
    echo "Logs are writing directly to $LOG_FILE (Ctrl+C to stop)"
    mpstat -P ALL 2 >> "$LOG_FILE"
else
    echo "mpstat NOT found. Falling back to standard top output..."
    echo "Logs are writing directly to $LOG_FILE (Ctrl+C to stop)"
    while true; do
        echo "--- CPU Snapshot at $(date) ---" >> "$LOG_FILE"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS top format
            top -l 1 -n 0 | grep -E "^CPU" >> "$LOG_FILE"
        else
            # Linux top format
            top -bn1 | head -n 5 >> "$LOG_FILE"
        fi
        sleep 2
    done
fi
