# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Benchmark comparing multi-threaded read and exists check performance: ThreadSafe LRUCache vs Simple HashMap."""

import concurrent.futures
import threading
import time
from typing import Dict, Generic, Optional, TypeVar

from google.cloud.storage._lru_cache import LRUCache

K = TypeVar("K")
V = TypeVar("V")


class ThreadSafeLRUCache(Generic[K, V]):
    """A thread-safe wrapper around LRUCache using threading.Lock."""

    def __init__(self, capacity: int) -> None:
        self._cache: LRUCache[K, V] = LRUCache(capacity)
        self._lock = threading.Lock()

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        with self._lock:
            return self._cache.get(key, default)

    def put(self, key: K, value: V) -> None:
        with self._lock:
            self._cache.put(key, value)

    def __contains__(self, key: K) -> bool:
        with self._lock:
            return key in self._cache


def benchmark_dict_reads(data: Dict[int, str], keys: list[int], num_ops: int) -> None:
    """Perform num_ops read operations on a standard dict."""
    num_keys = len(keys)
    for i in range(num_ops):
        key = keys[i % num_keys]
        _ = data[key]


def benchmark_lru_reads(
    cache: ThreadSafeLRUCache[int, str], keys: list[int], num_ops: int
) -> None:
    """Perform num_ops read operations on a thread-safe LRU cache."""
    num_keys = len(keys)
    for i in range(num_ops):
        key = keys[i % num_keys]
        _ = cache.get(key)


def benchmark_dict_exists(data: Dict[int, str], keys: list[int], num_ops: int) -> None:
    """Perform num_ops membership ('key in dict') operations on a standard dict."""
    num_keys = len(keys)
    for i in range(num_ops):
        key = keys[i % num_keys]
        _ = key in data


def benchmark_lru_exists(
    cache: ThreadSafeLRUCache[int, str], keys: list[int], num_ops: int
) -> None:
    """Perform num_ops membership ('key in cache') operations on a thread-safe LRU cache."""
    num_keys = len(keys)
    for i in range(num_ops):
        key = keys[i % num_keys]
        _ = key in cache


def run_benchmark() -> None:
    capacity = 10  # 10 prefilled items
    total_ops = 200_000  # Total operations across all threads
    thread_counts = [1, 8, 16, 32, 64, 128, 200]

    print(f"Prefilling Simple HashMap and LRU Cache with {capacity} items...")
    simple_dict: Dict[int, str] = {}
    lru_cache: ThreadSafeLRUCache[int, str] = ThreadSafeLRUCache(capacity=capacity)
    keys = list(range(capacity))

    for k in keys:
        val = f"value-{k}"
        simple_dict[k] = val
        lru_cache.put(k, val)

    print(
        f"\nBenchmarking Reads & Exists Checks (Total Ops = {total_ops:,} per test across all threads)"
    )
    print("=" * 115)
    print(
        f"{'Threads':<8} | {'Dict Read':<12} | {'LRU Read':<12} | {'Dict Exists':<12} | {'LRU Exists':<12} | {'Dict Exists(ns)':<17} | {'LRU Exists(ns)':<17}"
    )
    print("-" * 115)

    dict_exists_times = []
    lru_exists_times = []

    for num_threads in thread_counts:
        ops_per_thread = total_ops // num_threads
        actual_total_ops = ops_per_thread * num_threads

        # 1. Dict Reads
        t0 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(benchmark_dict_reads, simple_dict, keys, ops_per_thread)
                for _ in range(num_threads)
            ]
            concurrent.futures.wait(futures)
        dict_read_t = time.perf_counter() - t0

        # 2. LRU Reads
        t0 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(benchmark_lru_reads, lru_cache, keys, ops_per_thread)
                for _ in range(num_threads)
            ]
            concurrent.futures.wait(futures)
        lru_read_t = time.perf_counter() - t0

        # 3. Dict Exists Check
        t0 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(
                    benchmark_dict_exists, simple_dict, keys, ops_per_thread
                )
                for _ in range(num_threads)
            ]
            concurrent.futures.wait(futures)
        dict_exists_t = time.perf_counter() - t0
        dict_exists_avg_ns = (dict_exists_t / actual_total_ops) * 1e9
        dict_exists_times.append(dict_exists_avg_ns)

        # 4. LRU Exists Check
        t0 = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(benchmark_lru_exists, lru_cache, keys, ops_per_thread)
                for _ in range(num_threads)
            ]
            concurrent.futures.wait(futures)
        lru_exists_t = time.perf_counter() - t0
        lru_exists_avg_ns = (lru_exists_t / actual_total_ops) * 1e9
        lru_exists_times.append(lru_exists_avg_ns)

        print(
            f"{num_threads:<8} | {dict_read_t:<10.4f} s | {lru_read_t:<10.4f} s | {dict_exists_t:<10.4f} s | {lru_exists_t:<10.4f} s | {dict_exists_avg_ns:<14.1f} ns | {lru_exists_avg_ns:<14.1f} ns"
        )

    print("=" * 115)
    avg_overall_dict_ns = sum(dict_exists_times) / len(dict_exists_times)
    avg_overall_lru_ns = sum(lru_exists_times) / len(lru_exists_times)
    print(
        f"\nOverall Average Time per 'Exists' Check across all thread configurations:"
    )
    print(f"  Simple HashMap (dict) : {avg_overall_dict_ns:,.1f} nanoseconds per check")
    print(f"  ThreadSafe LRU Cache  : {avg_overall_lru_ns:,.1f} nanoseconds per check")


if __name__ == "__main__":
    run_benchmark()
