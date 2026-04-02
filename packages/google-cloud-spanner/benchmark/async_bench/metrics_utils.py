import asyncio
import os
import resource
import time
from typing import Dict, List


class BenchmarkMetrics:
    """Utility class to track and report benchmark metrics."""

    def __init__(self):
        self.latencies: List[float] = []
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.start_ru = None
        self.end_ru = None

    def start(self):
        """Start tracking metrics."""
        self.start_time = time.perf_counter()
        self.start_ru = resource.getrusage(resource.RUSAGE_SELF)

    def stop(self):
        """Stop tracking metrics."""
        self.end_time = time.perf_counter()
        self.end_ru = resource.getrusage(resource.RUSAGE_SELF)

    def record_latency(self, latency_ms: float):
        """Record a single latency measurement."""
        self.latencies.append(latency_ms)

    def get_percentile(self, p: float) -> float:
        """Calculate percentile from recorded latencies."""
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        k = (len(sorted_latencies) - 1) * (p / 100.0)
        f = int(k)
        c = f + 1
        if c >= len(sorted_latencies):
            return sorted_latencies[-1]
        return sorted_latencies[f] + (k - f) * (sorted_latencies[c] - sorted_latencies[f])

    def report(self, scenario_name: str) -> Dict[str, any]:
        """Report metrics for the scenario."""
        duration = self.end_time - self.start_time
        qps = len(self.latencies) / duration if duration > 0 else 0.0

        p50 = self.get_percentile(50.0)
        p95 = self.get_percentile(95.0)
        p99 = self.get_percentile(99.0)
        p99_9 = self.get_percentile(99.9)

        # CPU usage (user + system) converted to percentage over duration
        user_cpu_time = self.end_ru.ru_utime - self.start_ru.ru_utime
        sys_cpu_time = self.end_ru.ru_stime - self.start_ru.ru_stime
        total_cpu_time = user_cpu_time + sys_cpu_time
        cpu_usage_pct = (total_cpu_time / duration) * 100.0 if duration > 0 else 0.0

        # Max RSS memory (Mac OS is in bytes, Linux is in kilobytes)
        # On Mac, it's bytes. On Linux, it's KB. We assume bytes if it looks large.
        max_rss_bytes = self.end_ru.ru_maxrss
        if os.uname().sysname == "Linux":
            max_rss_bytes *= 1024  # Linux is in KB

        results = {
            "scenario": scenario_name,
            "duration_sec": duration,
            "total_operations": len(self.latencies),
            "throughput_qps": qps,
            "latency_p50_ms": p50,
            "latency_p95_ms": p95,
            "latency_p99_ms": p99,
            "latency_p99_9_ms": p99_9,
            "avg_latency_ms": sum(self.latencies) / len(self.latencies) if self.latencies else 0.0,
            "cpu_usage_pct": cpu_usage_pct,
            "max_rss_bytes": max_rss_bytes,
        }

        print(f"\n--- Results for {scenario_name} ---")
        print(f"Duration: {duration:.2f}s")
        print(f"Throughput: {qps:.2f} QPS")
        print(f"Latency P50: {p50:.2f} ms")
        print(f"Latency P95: {p95:.2f} ms")
        print(f"Latency P99: {p99:.2f} ms")
        print(f"Latency P99.9: {p99_9:.2f} ms")
        print(f"Average CPU Usage: {cpu_usage_pct:.2f}%")
        print(f"Max RSS Memory (MB): {max_rss_bytes / (1024 * 1024):.2f}")
        print("-----------------------------------")

        return results
