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

| Scenario | Interactive Flame Graph (HTML) | Binary Profile Data (.prof) | Requests (10s) | Throughput (QPS) | Avg Pure Client CPU / Query | Concurrency Model |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **1. Real Point Select ($C=1$, Sync)** | [**`spanner_point_select_c1.html`**](./spanner_point_select_c1.html) | [`spanner_point_select_c1.prof`](./spanner_point_select_c1.prof) | 757 | **75.7 QPS** | **~6.87 ms** | Single-Threaded Sync |
| **2. Real Point Select ($C=32$, High-Level Async)** | [**`spanner_point_select_c32.html`**](./spanner_point_select_c32.html) | [`spanner_point_select_c32.prof`](./spanner_point_select_c32.prof) | 1,160 | **116.0 QPS** | **~6.65 ms** | **32 Async Coroutines (1 OS Thread)** |
| **3. Real LIMIT 1000 Read (11 cols, Sync)** | [**`spanner_limit1000_c1.html`**](./spanner_limit1000_c1.html) | [`spanner_limit1000_c1.prof`](./spanner_limit1000_c1.prof) | 89 (89k rows) | **8.9 QPS** *(8,900 rows/s)* | **~64.27 ms** | Single-Threaded Sync |
| **4. Real Point Select ($C=32$ Threads, Multi-Threading GIL)** | [**`spanner_point_select_c32_threads.html`**](./spanner_point_select_c32_threads.html) | [`spanner_point_select_c32_threads.prof`](./spanner_point_select_c32_threads.prof) | 1,043 | **104.3 QPS** | **~7.31 ms** | **32 Preemptive OS Threads (Multi-Threading)** |

---

## 3. Pure CPU Profiling Metrics Breakdown (YAPPI CPU Clock)

### Scenario 1: Point Select ($C=1$, Sync, Full Row Parsing)
* **Total Requests Recorded (10s):** 757 queries (**75.7 QPS**)
* **Total Pure CPU Time:** 5.2016 s (Avg: **6.87 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `streamed.py:_consume_next` / `__iter__`: **4.274 s cumulative** (Stream chunk processing & row decoding)
  2. `snapshot.py:_restart_on_unavailable`: **3.992 s cumulative** (GAPIC snapshot wrapper & retry logic)
  3. `client.py:execute_streaming_sql`: **1.238 s cumulative** (SQL execution dispatch)
  4. `method.py:_GapicCallable.__call__`: **1.135 s cumulative** (GAPIC unary stream callable)
  5. `message.py:QueryOptions.__init__` / `__getattr__`: **1.621 s cumulative** (SQL query options validation)

---

### Scenario 2: Point Select ($C=32$, High-Level Spanner Async Client)
* **Total Requests Recorded (10s):** 1,160 queries across 32 concurrent coroutines (**116.0 QPS**)
* **Total Pure CPU Time:** 7.7174 s (Avg: **6.65 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `base_events._run_once` & `events.Handle._run`: **9.034 s / 8.514 s cumulative** (AsyncIO event loop task scheduling)
  2. `streamed.py:StreamedResultSet.__aiter__` / `_consume_next`: **5.073 s / 5.038 s cumulative** (Async chunk stream decoding)
  3. `snapshot.py:_restart_on_unavailable`: **4.469 s cumulative** (Async snapshot retry supervisor)
  4. `marshal.py:Marshal.to_proto` & `to_python`: **1.625 s cumulative** (Protobuf message marshaling)
  5. `message.py:QueryOptions.__init__` & `__getattr__`: **2.451 s cumulative** (Query options initialization)
  6. `_opentelemetry_tracing.py:trace_call` & `metrics_capture.py`: **1.824 s cumulative** (Observability & metrics capture)

```
ncalls  tottime  cumtime  filename:lineno(function)
  5862    0.197    9.034  base_events.py:1845(_UnixSelectorEventLoop._run_once)
 18687    0.082    8.514  events.py:78(Handle._run)
    32    0.032    7.015  spanner_cpu_profile_suite.py:173(async_worker_loop_high_level)
  1160    0.046    6.981  spanner_cpu_profile_suite.py:162(run_single_async_query_high_level)
  1160    0.032    5.119  spanner_cpu_profile_suite.py:169(<listcomp>)
  1160    0.033    5.073  streamed.py:193(StreamedResultSet.__aiter__)
  1160    0.061    5.038  streamed.py:166(StreamedResultSet._consume_next)
   0/1    0.094    4.469  snapshot.py:72(_restart_on_unavailable)
  1160    0.073    1.524  snapshot.py:339(Snapshot.execute_sql)
  8120    0.166    1.325  message.py:611(QueryOptions.__init__)
 17400    0.168    1.126  message.py:806(QueryOptions.__getattr__)
 20880    0.249    1.078  marshal.py:199(Marshal.to_proto)
  2320    0.076    0.978  _opentelemetry_tracing.py:58(trace_call)
  2320    0.031    0.846  metrics_capture.py:77(MetricsCapture.__exit__)
```

---

### Scenario 3: LIMIT 1000 Read (11 Columns, Sync, Full Row Parsing)
* **Total Queries Recorded (10s):** 89 queries (**8.9 QPS / 8,900 rows/s**) [89,000 rows / 979,000 field values]
* **Total Pure CPU Time:** 5.7203 s (Avg: **64.27 ms pure CPU per query**)
* **What Exploded:**
  * `StreamedResultSet._merge_values`: **3.589 s self-CPU time (62.7% of total client CPU time)** merging raw Protobuf values into row chunks.

```
ncalls  tottime  cumtime  filename:lineno(function)
    89    0.131    8.596  spanner_cpu_profile_suite.py:74(run_limit_1000_query_sync)
 89089    0.354    8.314  streamed.py:169(StreamedResultSet.__iter__)
    89    0.909    7.834  streamed.py:150(StreamedResultSet._consume_next)
    89    3.589    6.394  streamed.py:111(StreamedResultSet._merge_values)
   178    0.007    0.530  snapshot.py:75(_restart_on_unavailable)
   178    0.003    0.262  threading.py:964(run)
    89    0.077    0.208  _channel.py:1722(channel_spin)
```

---

### Scenario 4: Point Select with 32 OS Threads (Multi-Threading & GIL Contention)
* **Total Requests Recorded (10s):** 1,043 queries across 32 OS threads (**104.3 QPS**)
* **Total Pure CPU Time (All 32 Threads):** 7.6277 s (Avg: **7.31 ms pure CPU per query**)
* **Total GIL Wait Time (All 32 Threads):** **7.3893 s** (Avg: **0.231 s queue delay / thread**)
* **GIL Contention Ratio:** **49.21% of active compute phases**

```
ncalls  tottime  cumtime  filename:lineno(function)
  1077    0.024    9.541  threading.py:964(run)
    32    0.059    8.297  spanner_cpu_profile_suite.py:285(worker_thread_loop)
  1043    0.034    8.206  spanner_cpu_profile_suite.py:63(run_point_select_query_sync)
  2086    0.016    6.412  streamed.py:169(StreamedResultSet.__iter__)
  1043    0.037    6.394  streamed.py:150(StreamedResultSet._consume_next)
  2086    0.078    5.997  snapshot.py:75(_restart_on_unavailable)
  1043    0.041    2.002  client.py:1453(SpannerClient.execute_streaming_sql)
  1044    0.040    1.843  method.py:151(_GapicCallable.__call__)
  1044    0.015    1.614  timeout.py:101(func_with_timeout)
  1043    0.021    1.579  grpc_helpers.py:140(error_remapped_callable)
  1043    0.077    1.470  snapshot.py:415(Snapshot.execute_sql)
  7301    0.159    1.245  message.py:611(QueryOptions.__init__)
```

---

## 4. How to Re-Run on Any Machine

```bash
# 1. Run the real Spanner benchmark suite (generates all 4 .prof files)
python3 spanner_cpu_profile_suite.py

# 2. Export interactive HTML flame graphs (zero pip dependencies needed)
python3 export_flamegraph_html.py
```
