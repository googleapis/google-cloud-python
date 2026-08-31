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

| Scenario | Interactive Flame Graph (HTML) | Binary Profile Data (.prof) | Requests (10s) | Avg Pure Client CPU / Query |
| :--- | :--- | :--- | :--- | :---: |
| **1. Real Point Select ($C=1$, Sync)** | [**`spanner_point_select_c1.html`**](./spanner_point_select_c1.html) | [`spanner_point_select_c1.prof`](./spanner_point_select_c1.prof) | 24 | **~7.63 ms** |
| **2. Real Point Select ($C=32$, Async Full Row Parsing)** | [**`spanner_point_select_c32.html`**](./spanner_point_select_c32.html) | [`spanner_point_select_c32.prof`](./spanner_point_select_c32.prof) | 1,462 | **~1.42 ms** |
| **3. Real LIMIT 1000 Read (11 cols, Sync)** | [**`spanner_limit1000_c1.html`**](./spanner_limit1000_c1.html) | [`spanner_limit1000_c1.prof`](./spanner_limit1000_c1.prof) | 11 (11k rows) | **~355.06 ms** |
| **4. Real Point Select ($C=32$ Threads, Multi-Threading GIL)** | [**`spanner_point_select_c32_threads.html`**](./spanner_point_select_c32_threads.html) | [`spanner_point_select_c32_threads.prof`](./spanner_point_select_c32_threads.prof) | 691 | **~10.10 ms** |

---

## 3. Pure CPU Profiling Metrics Breakdown (YAPPI CPU Clock)

### Scenario 1: Point Select ($C=1$, Sync, Full Row Parsing)
* **Total Requests Recorded (10s):** 24 queries
* **Total Pure CPU Time:** 0.1830 s (Avg: **7.63 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `streamed.py:_consume_next` / `__iter__`: **0.167 s cumulative** (Stream chunk processing & row parsing)
  2. `snapshot.py:_restart_on_unavailable`: **0.163 s cumulative** (GAPIC snapshot wrapper)
  3. `threading.py:Thread.start` / `Event.wait`: **0.124 s / 0.115 s cumulative** (gRPC worker coordination)
  4. `client.py:execute_streaming_sql`: **0.113 s cumulative** (SQL execution dispatch)
  5. `_channel.py:create`: **0.081 s cumulative** (RPC call creation)

---

### Scenario 2: Point Select ($C=32$, Spanner Async Client, Full Row Parsing)
* **Total Requests Recorded (10s):** 1,462 queries across 32 concurrent coroutines
* **Total Pure CPU Time:** 2.0797 s (Avg: **1.42 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `base_events._run_once`: **5.924 s cumulative / 0.106 s tottime** (AsyncIO event loop task dispatch)
  2. `events.Handle._run`: **5.141 s cumulative / 0.043 s tottime** (Task coroutine execution)
  3. `_call.UnaryStreamCall._send_unary_request`: **3.350 s cumulative / 0.183 s tottime** (gRPC AsyncIO unary request serialization)
  4. `threading.Thread.start` / `Event.wait`: **2.964 s / 2.833 s cumulative** (gRPC C-Core background thread signaling)
  5. `run_single_async_query_with_parsing`: **1.474 s cumulative / 0.097 s tottime** (Query wrapper & row decoding)
  6. `selectors.EpollSelector.select`: **0.588 s cumulative / 0.046 s tottime** (epoll event dispatch compute)
  7. `grpc_helpers_async.error_remapped_callable`: **0.452 s cumulative / 0.030 s tottime** (Error interceptor)
  8. `_helpers._parse_value_pb`: **0.200 s cumulative / 0.069 s tottime** (**16,082 calls** decoding cells)

```
ncalls  tottime  cumtime  filename:lineno(function)
  9503    0.106    5.924  base_events.py:1970(_UnixSelectorEventLoop._run_once)
 19081    0.043    5.141  events.py:87(Handle._run)
  1462    0.183    3.350  _call.py:639(UnaryStreamCall._send_unary_request)
  1462    0.008    2.964  threading.py:978(Thread.start)
  1462    0.007    2.833  threading.py:660(Event.wait)
  1462    0.018    2.815  threading.py:346(Condition.wait)
    32    0.075    1.556  spanner_cpu_profile_suite.py:152(async_worker_loop_gapic)
  1462    0.097    1.474  spanner_cpu_profile_suite.py:117(run_single_async_query_with_parsing)
  9504    0.046    0.588  selectors.py:435(EpollSelector.select)
  1462    0.030    0.452  grpc_helpers_async.py:161(error_remapped_callable)
 16082    0.069    0.200  _helpers.py:244(_parse_value_pb)
```

---

### Scenario 3: LIMIT 1000 Read (11 Columns, Sync, Full Row Parsing)
* **Total Queries Recorded (10s):** 11 queries (**11,000 rows / 121,000 field values**)
* **Total Pure CPU Time:** 3.9057 s (Avg: **355.06 ms pure CPU per query**)
* **What Exploded:**
  * `_parse_value_pb` and `TypeCode.__eq__` exploded to **3.280 s cumulative (84.0% of total client CPU time)**!
  * Over 121,000 protobuf values were unpacked, invoking 121,000 enum property lookups and comparisons in Python.

```
ncalls  tottime  cumtime  filename:lineno(function)
    11    0.020    4.504  spanner_cpu_profile_suite.py:71(run_limit_1000_query_sync)
 11011    0.055    4.430  streamed.py:145(StreamedResultSet.__iter__)
    22    0.024    4.327  streamed.py:118(StreamedResultSet._consume_next)
    11    0.676    4.227  streamed.py:96(StreamedResultSet._merge_values)
121000    0.980    3.280  _helpers.py:244(_parse_value_pb)
121000    0.978    2.075  enums.py:125(TypeCode.__eq__)
121000    0.455    0.761  enum.py:199(property.__get__)
121000    0.337    0.337  enums.py:118(TypeCode._comparable)
121000    0.306    0.306  enum.py:1337(TypeCode.value)
    22    0.000    0.106  method.py:81(_GapicCallable.__call__)
```

---

### Scenario 4: Point Select with 32 OS Threads (Multi-Threading & GIL Contention)
* **Total Requests Recorded (10s):** 691 queries across 32 OS threads
* **Total Pure CPU Time (All 32 Threads):** 6.982 s (Avg: **10.10 ms pure CPU per query**)
* **Total GIL Wait Time (All 32 Threads):** **6.763 s** (Avg: **0.211 s / thread**)
* **GIL Contention Ratio:** **49.2% of active compute phases**

```
ncalls  tottime  cumtime  filename:lineno(function)
  1437    0.002    7.791  threading.py:1006(Thread.run)
    32    0.004    6.987  spanner_cpu_profile_suite.py:285(worker_thread_loop)
   691    0.005    6.956  spanner_cpu_profile_suite.py:63(run_point_select_query_sync)
  1404    0.015    5.021  method.py:81(_GapicCallable.__call__)
  1404    0.029    4.839  timeout.py:87(func_with_timeout)
  1382    0.005    4.186  streamed.py:145(StreamedResultSet.__iter__)
  1382    0.001    4.180  streamed.py:118(StreamedResultSet._consume_next)
  1382    0.022    4.136  snapshot.py:51(_restart_on_unavailable)
   691    0.021    3.002  client.py:1363(SpannerClient.execute_streaming_sql)
   691    0.005    2.681  grpc_helpers.py:126(error_remapped_callable)
 14068    0.005    2.410  threading.py:322(Condition.__enter__)
   691    0.003    2.302  database.py:1237(SnapshotCheckout.__enter__)
   691    0.001    2.295  pool.py:303(BurstyPool.get)
   669    0.005    2.218  session.py:152(Session.exists)
```

---

## 4. How to Re-Run on Any Machine

```bash
# 1. Run the real Spanner benchmark suite (generates all 4 .prof files)
python3 spanner_cpu_profile_suite.py

# 2. Export interactive HTML flame graphs (zero pip dependencies needed)
python3 export_flamegraph_html.py
```
