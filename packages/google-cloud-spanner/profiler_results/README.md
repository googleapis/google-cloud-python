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
| **1. Real Point Select ($C=1$, Sync)** | [**`spanner_point_select_c1.html`**](./spanner_point_select_c1.html) | [`spanner_point_select_c1.prof`](./spanner_point_select_c1.prof) | 23 | **~7.59 ms** |
| **2. Real Point Select ($C=32$, AsyncIO)** | [**`spanner_point_select_c32.html`**](./spanner_point_select_c32.html) | [`spanner_point_select_c32.prof`](./spanner_point_select_c32.prof) | 1,476 | **~1.16 ms** |
| **3. Real LIMIT 1000 Read (11 cols, Sync)** | [**`spanner_limit1000_c1.html`**](./spanner_limit1000_c1.html) | [`spanner_limit1000_c1.prof`](./spanner_limit1000_c1.prof) | 11 (11k rows) | **~340.27 ms** |

---

## 3. Pure CPU Profiling Metrics Breakdown (YAPPI CPU Clock)

### Scenario 1: Point Select ($C=1$, Sync, Pure CPU Clock)
* **Total Requests Recorded (10s):** 23 queries
* **Total Pure CPU Time:** 0.1746 s (Avg: **7.59 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `streamed.py:_consume_next`: **0.158 s cumulative** (Stream chunk processing)
  2. `snapshot.py:_restart_on_unavailable`: **0.156 s cumulative** (GAPIC snapshot wrapper)
  3. `threading.py:Thread.start` / `Event.wait`: **0.125 s / 0.121 s cumulative** (gRPC channel worker coordination)
  4. `client.py:execute_streaming_sql`: **0.109 s cumulative** (SQL execution dispatch)
  5. `_channel.py:create`: **0.080 s cumulative** (RPC call creation)
  6. `database.py:SnapshotCheckout.__enter__`: **0.071 s cumulative** (Session checkout from pool)

```
ncalls  tottime  cumtime  filename:lineno(function)
    46    0.000    0.158  streamed.py:118(StreamedResultSet._consume_next)
    46    0.001    0.156  snapshot.py:51(_restart_on_unavailable)
    69    0.000    0.125  threading.py:978(Thread.start)
    69    0.000    0.121  threading.py:660(Event.wait)
    23    0.000    0.109  client.py:1363(SpannerClient.execute_streaming_sql)
    23    0.000    0.105  grpc_helpers.py:126(error_remapped_callable)
    23    0.000    0.088  _channel.py:1350(_UnaryStreamMultiCallable.__call__)
    23    0.004    0.080  _channel.py:1733(create)
    23    0.001    0.071  database.py:1237(SnapshotCheckout.__enter__)
    23    0.000    0.070  session.py:152(Session.exists)
```

---

### Scenario 2: Point Select ($C=32$, Spanner Async Client, Pure CPU Clock)
* **Total Requests Recorded (10s):** 1,476 queries across 32 concurrent coroutines (~148 QPS)
* **Total Pure CPU Time:** 1.7128 s (Avg: **1.16 ms pure CPU per query**)
* **Top CPU Bottlenecks:**
  1. `base_events._run_once`: **5.338 s cumulative / 0.087 s tottime** (AsyncIO event loop task dispatch)
  2. `events.Handle._run`: **4.609 s cumulative / 0.044 s tottime** (Task coroutine execution)
  3. `_call.UnaryStreamCall._send_unary_request`: **3.194 s cumulative / 0.181 s tottime** (gRPC AsyncIO unary request serialization)
  4. `threading.Thread.start` / `Event.wait`: **2.775 s / 2.602 s cumulative** (gRPC C-Core background thread signaling)
  5. `async_worker_loop`: **1.210 s cumulative / 0.069 s tottime** (Worker coroutine driver)
  6. `run_single_async_query`: **1.127 s cumulative / 0.035 s tottime** (Query wrapper)
  7. `selectors.EpollSelector.select`: **0.553 s cumulative / 0.043 s tottime** (epoll event dispatch compute)
  8. `grpc_helpers_async.error_remapped_callable`: **0.426 s cumulative / 0.035 s tottime** (Error interceptor)
  9. `_channel.UnaryStreamMultiCallable.__call__`: **0.366 s cumulative / 0.012 s tottime** (gRPC MultiCallable)
 10. `SpannerAsyncClient.execute_streaming_sql`: **0.300 s cumulative / 0.030 s tottime** (Async client streaming method)

```
ncalls  tottime  cumtime  filename:lineno(function)
  9161    0.087    5.338  base_events.py:1970(_UnixSelectorEventLoop._run_once)
 19269    0.044    4.609  events.py:87(Handle._run)
  1476    0.181    3.194  _call.py:639(UnaryStreamCall._send_unary_request)
  1476    0.016    2.775  threading.py:978(Thread.start)
  1476    0.008    2.602  threading.py:660(Event.wait)
  1476    0.011    2.586  threading.py:346(Condition.wait)
    32    0.069    1.210  spanner_cpu_profile_suite.py:115(async_worker_loop)
  1476    0.035    1.127  spanner_cpu_profile_suite.py:103(run_single_async_query)
  9162    0.043    0.553  selectors.py:435(EpollSelector.select)
  1476    0.035    0.426  grpc_helpers_async.py:161(error_remapped_callable)
```

---

### Scenario 3: LIMIT 1000 Read (11 Columns, Sync, Pure CPU Clock)
* **Total Queries Recorded (10s):** 11 queries (**11,000 rows / 121,000 field values**)
* **Total Pure CPU Time:** 3.7430 s (Avg: **340.27 ms pure CPU per query**)
* **What Exploded:**
  * `_parse_value_pb` and `TypeCode.__eq__` exploded to **3.256 s cumulative (87.0% of total client CPU time)**!
  * Over 121,000 protobuf values were unpacked, invoking 121,000 enum property lookups and comparisons in Python.

```
ncalls  tottime  cumtime  filename:lineno(function)
    11    0.030    4.355  spanner_cpu_profile_suite.py:57(run_limit_1000_query_sync)
 11011    0.044    4.269  streamed.py:145(StreamedResultSet.__iter__)
    22    0.030    4.193  streamed.py:118(StreamedResultSet._consume_next)
    11    0.587    4.092  streamed.py:96(StreamedResultSet._merge_values)
121000    0.897    3.256  _helpers.py:244(_parse_value_pb)
121000    0.976    2.078  enums.py:125(TypeCode.__eq__)
121000    0.546    0.814  enum.py:199(property.__get__)
121000    0.288    0.288  enums.py:118(TypeCode._comparable)
121000    0.267    0.267  enum.py:1337(TypeCode.value)
    22    0.003    0.097  method.py:81(_GapicCallable.__call__)
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
