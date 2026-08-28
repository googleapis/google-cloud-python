# Google Cloud Spanner Python Client - CPU Profiling Results (Real Network RPCs)

This directory contains real-world CPU profiling data (`.prof` files), standalone interactive HTML flame graphs, and the benchmarking harness used to analyze CPU cycle consumption, event loop dynamics, GAPIC/gRPC overhead, and GIL bottlenecks across the request lifecycle of the Cloud Spanner Python client library making actual network RPCs against Google Cloud Spanner.

---

## 1. Overview & Setup

* **Benchmark Harness:** [`spanner_cpu_profile_suite.py`](./spanner_cpu_profile_suite.py) (Pure real Spanner network calls — **NO MOCKS, NO ARTIFICIAL SLEEP**)
* **Flame Graph Exporter:** [`export_flamegraph_html.py`](./export_flamegraph_html.py) (Generates standalone HTML flame graphs with zero external pip dependencies)
* **Target Table:** `AsyncBenchmarkTable` (11 columns: `id`, `field0`..`field9`) on project `span-cloud-testing`, instance `suvham-testing`, database `benchmark_db_async`.
* **Connection Warmup:** 5 seconds pre-run before recording CPU ticks.

---

## 2. Interactive Flame Graphs (Open in Browser)

You do **not** need `snakeviz` or any third-party pip packages to view these flame graphs. Simply open the generated `.html` files in any browser:

| Scenario | Interactive Flame Graph (HTML) | Binary Profile Data (.prof) | Requests (10s) | Avg Client CPU / Query |
| :--- | :--- | :--- | :---: | :---: |
| **1. Real Point Select ($C=1$)** | [**`spanner_point_select_c1.html`**](./spanner_point_select_c1.html) | [`spanner_point_select_c1.prof`](./spanner_point_select_c1.prof) | 24 | **~10.3 s cum** |
| **2. Real Point Select ($C=32$)** | [**`spanner_point_select_c32.html`**](./spanner_point_select_c32.html) | [`spanner_point_select_c32.prof`](./spanner_point_select_c32.prof) | 733 | **~10.7 s cum** |
| **3. Real LIMIT 1000 Read (11 cols)** | [**`spanner_limit1000_c1.html`**](./spanner_limit1000_c1.html) | [`spanner_limit1000_c1.prof`](./spanner_limit1000_c1.prof) | 17 (17k rows) | **~10.1 s cum** |

---

## 3. Real Profiling Metrics Breakdown

### Scenario 1: Point Select ($C=1$, Real Network Calls)
* **Total Requests Recorded (10s):** 24 queries
* **Total Profiled CPU Time:** 10.30 s
* **Top Bottlenecks:**
  1. `_channel.py:_next` / `__next__`: **10.26 s cumulative** (gRPC C-Core socket polling & stream consumption)
  2. `method.py:__call__`: **10.22 s cumulative** (GAPIC method wrapper & retry interception)
  3. `streamed._consume_next`: **5.18 s cumulative** (Stream chunk processing)
  4. `_thread.lock.acquire`: **5.14 s cumulative** (Lock acquisition in gRPC thread synchronization)

```
ncalls    cumtime   filename:lineno(function)
    24    10.297    spanner_cpu_profile_suite.py:run_point_select_query
    72    10.256    _channel.py:__next__
    72    10.255    _channel.py:_next
    48    10.223    gapic_v1/method.py:__call__
    48    10.191    gapic_v1/timeout.py:func_with_timeout
    48     5.181    streamed.py:__iter__
    48     5.180    streamed.py:_consume_next
    48     5.175    snapshot.py:_restart_on_unavailable
    72     5.170    grpc_helpers.py:__next__
   640     5.140    _thread.lock:acquire
```

---

### Scenario 2: Point Select ($C=32$, Real Concurrent Threads)
* **Total Requests Recorded (10s):** 733 queries across 32 concurrent threads (~73 QPS)
* **Total Profiled CPU Time:** 10.66 s
* **Top Bottlenecks:**
  1. `threading.py:wait` & `join`: **63.5 s / 31.9 s cumulative** (Thread pool synchronization and worker coordination)
  2. `grpc_helpers.__next__` / `_channel.__next__`: **24.7 s / 21.1 s cumulative** (gRPC transport stream dispatch across 32 threads)
  3. `streamed._consume_next`: **11.01 s cumulative** (Chunk extraction and row decoding)
  4. `pool.py:put` / `database.__exit__`: **10.66 s cumulative** (Session pool lock acquisition and checkout/return)

```
ncalls    cumtime   filename:lineno(function)
    33    94.157    spanner_cpu_profile_suite.py:<genexpr>
    32    84.007    concurrent/futures/_base.py:result
  4779    63.514    threading.py:wait
    32    31.952    threading.py:join
  2199    24.718    grpc_helpers.py:__next__
  2199    21.136    _channel.py:__next__
  1466    11.011    streamed.py:__iter__
  1466    11.011    streamed.py:_consume_next
   733    10.661    database.py:__exit__
   733    10.658    pool.py:put
```

---

### Scenario 3: LIMIT 1000 Read (11 Columns, Real Streaming Response)
* **Total Queries Recorded (10s):** 17 queries (**17,000 rows / 187,000 cells**)
* **Total Profiled CPU Time:** 10.10 s
* **Top Bottlenecks:**
  1. `_channel._next` / `__next__`: **11.13 s cumulative** (Multi-chunk streaming HTTP/2 frame reception)
  2. `gapic_v1.method.__call__`: **9.20 s cumulative** (GAPIC streaming call pipeline)
  3. `streamed._consume_next`: **6.44 s cumulative** (Consuming streaming row chunks)
  4. `_thread.lock.acquire`: **5.56 s cumulative** (gRPC background thread lock synchronization)

```
ncalls    cumtime   filename:lineno(function)
    51    11.134    _channel.py:__next__
    51    11.134    _channel.py:_next
    17    10.102    spanner_cpu_profile_suite.py:run_limit_1000_query
    34     9.199    gapic_v1/method.py:__call__
    34     9.182    gapic_v1/timeout.py:func_with_timeout
 17017     6.460    streamed.py:__iter__
    34     6.435    streamed.py:_consume_next
    51     5.585    grpc_helpers.py:__next__
    17     5.573    client.py:execute_streaming_sql
   471     5.565    _thread.lock:acquire
```

---

## 4. How to Re-Run on Any Machine

```bash
# 1. Run the real Spanner benchmark suite (generates .prof files)
python3 spanner_cpu_profile_suite.py

# 2. Export interactive HTML flame graphs (zero pip dependencies needed)
python3 export_flamegraph_html.py
```
