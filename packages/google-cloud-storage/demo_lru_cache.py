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

"""Demonstration script for using LRUCache in a multi-threaded environment."""

import concurrent.futures
import random
import threading
import time
from typing import Generic, Optional, TypeVar

from google.cloud.storage._lru_cache import LRUCache

K = TypeVar("K")
V = TypeVar("V")


class ThreadSafeLRUCache(Generic[K, V]):
    """A thread-safe wrapper around LRUCache using threading.Lock."""

    def __init__(self, capacity: int) -> None:
        self._cache: LRUCache[K, V] = LRUCache(capacity)
        self._lock = threading.Lock()

    @property
    def capacity(self) -> int:
        with self._lock:
            return self._cache.capacity

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        with self._lock:
            return self._cache.get(key, default)

    def put(self, key: K, value: V) -> None:
        with self._lock:
            self._cache.put(key, value)

    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: K) -> bool:
        with self._lock:
            return key in self._cache

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


def worker(
    cache: ThreadSafeLRUCache[int, str], thread_id: int, iterations: int
) -> None:
    """Worker function that concurrently reads and writes to the cache."""
    for _ in range(iterations):
        key = random.randint(1, 10)
        if random.random() < 0.5:
            # Write operation
            val = f"Value-{key}-from-T{thread_id}"
            cache.put(key, val)
        else:
            # Read operation
            cache.get(key)
        time.sleep(0.001)


def main() -> None:
    capacity = 5
    num_threads = 10
    iterations = 20

    print(f"Initializing ThreadSafeLRUCache with capacity {capacity}...")
    cache: ThreadSafeLRUCache[int, str] = ThreadSafeLRUCache(capacity=capacity)

    print(f"Starting {num_threads} concurrent worker threads...")
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker, cache, i, iterations) for i in range(num_threads)
        ]
        concurrent.futures.wait(futures)

    elapsed = time.time() - start_time
    print(f"All threads completed in {elapsed:.2f} seconds.")
    print(f"Final cache size: {len(cache)} (Max capacity: {cache.capacity})")

    # Verify cache size does not exceed capacity
    assert len(cache) <= cache.capacity
    print(
        "Verification successful: Multi-threaded operations maintained capacity constraint safely."
    )


if __name__ == "__main__":
    main()
