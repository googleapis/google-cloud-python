# Google Cloud Spanner Python Client - CPU Profiling Results

This directory contains CPU profiling data (`.prof` files), standalone interactive HTML flame graphs, and the benchmarking harness used to analyze CPU cycle consumption, event loop dynamics, and GIL bottlenecks across the request lifecycle of the Cloud Spanner Python client library.

---

## 1. Overview & Setup

* **Benchmark Harness:** [`spanner_cpu_profile_suite.py`](./spanner_cpu_profile_suite.py)
* **Flame Graph Exporter:** [`export_flamegraph_html.py`](./export_flamegraph_html.py) (Generates standalone HTML flame graphs with zero external dependencies)
* **Target Table:** `AsyncBenchmarkTable` (12 distinct Spanner column types: `INT64`, `STRING`, `FLOAT64`, `BOOL`, `BYTES`, `ARRAY<STRING>`, `JSON`, `TIMESTAMP`).
* **Connection Warmup:** 5 seconds pre-run before recording CPU ticks.
* **Server Latency Simulation:** 5ms mock database sleep time per RPC.

---

## 2. Interactive Flame Graphs (Open in Browser)

You do **not** need `snakeviz` or any third-party pip packages to view these flame graphs. Simply open the generated `.html` files in any browser:

| Scenario | Interactive Flame Graph (HTML) | Binary Profile Data (.prof) | Avg Client CPU / Query |
| :--- | :--- | :--- | :---: |
| **1. Point Select ($C=1$)** | [**`spanner_point_select_c1.html`**](./spanner_point_select_c1.html) | [`spanner_point_select_c1.prof`](./spanner_point_select_c1.prof) | **~1.26 ms** |
| **2. Point Select ($C=32$)** | [**`spanner_point_select_c32.html`**](./spanner_point_select_c32.html) | [`spanner_point_select_c32.prof`](./spanner_point_select_c32.prof) | **~0.97 ms** |
| **3. LIMIT 1000 Read (12 cols)** | [**`spanner_limit1000_c1.html`**](./spanner_limit1000_c1.html) | [`spanner_limit1000_c1.prof`](./spanner_limit1000_c1.prof) | **301.8 ms** |

---

## 3. Profiling Metrics Breakdown

### Scenario 1: Point Select (Concurrency = 1)
* **Total Requests Recorded (10s):** 1,565 queries (~156 QPS)
* **Total Profiled CPU Time:** 1.97 s (out of 9.99 s wall-clock time)
* **Top Bottlenecks:**
  1. `_helpers._parse_value_pb` & type unpacking: ~35% of client CPU
  2. `proto-plus` dynamic wrapping (`message.__init__`, `marshal.to_proto`): ~38% of client CPU
  3. `Snapshot.execute_sql` & retry management: ~18% of client CPU

```
ncalls    cumtime   filename:lineno(function)
  1565     9.991    run_cpu_profiler_suite.py:run_single_query
  3130     9.407    streamed.py:_consume_next
  1565     8.020    time.sleep (5ms mock DB latency)
  1565     0.721    streamed.py:_merge_values
 23475     0.652    _helpers.py:_parse_value_pb
  1565     0.544    snapshot.py:execute_sql
 10955     0.425    proto/message.py:__init__
 20345     0.371    proto/message.py:__getattr__
 28170     0.277    proto/marshal.py:to_proto
```

---

### Scenario 2: Point Select (Concurrency = 32)
* **Total Requests Recorded (10s):** 10,312 queries (~1,031 QPS)
* **Total Profiled CPU Time:** 10.01 s
* **Characteristics:** Overlapping 5ms I/O yields >1,000 QPS and keeps the CPU 100% saturated. The profile captures event loop scheduling (`base_events._run_once`, `events._run`, `_contextvars.Context.run`), which accounts for ~5–8% of CPU ticks.

```
ncalls    cumtime   filename:lineno(function)
     1    10.007    asyncio/runners.py:run
   808    10.005    asyncio/base_events.py:_run_once
 20695     9.893    asyncio/events.py:_run
 10344     9.771    run_cpu_profiler_suite.py:worker
 10312     9.425    run_cpu_profiler_suite.py:run_single_query
 20624     6.462    streamed.py:_consume_next
 10312     3.618    streamed.py:_merge_values
154680     3.265    _helpers.py:_parse_value_pb
 10312     2.784    snapshot.py:execute_sql
```

---

### Scenario 3: LIMIT 1000 Read (12 Columns)
* **Total Queries Recorded (10s):** 34 queries (**34,000 rows / 408,000 cells**)
* **Total Profiled CPU Time:** 10.26 s (100% CPU bound)
* **Average Client CPU / Query:** **301.8 ms of continuous CPU time**
* **Top Bottlenecks:**
  1. `_helpers._parse_value_pb`: **9.41 s cumulative** (92% of all CPU time)
  2. `enums.__eq__`: **4.25 s cumulative** (2.21 million calls)
  3. `datetime_helpers.from_rfc3339` / `_strptime`: **2.80 s cumulative** (68k calls)
  4. `enum.__get__` / `_comparable`: **1.26 s cumulative** (2.21 million calls)

```
ncalls    cumtime   filename:lineno(function)
    34    10.260    run_cpu_profiler_suite.py:run_single_query
   374    10.179    streamed.py:_consume_next
   340     9.899    streamed.py:_merge_values
510000     9.408    _helpers.py:_parse_value_pb
2210000    4.245    proto/enums.py:__eq__
 68000     2.798    datetime_helpers.py:from_rfc3339
 68000     1.987    _strptime.py:strptime
2210000    1.262    enum.py:__get__
```

---

## 4. Key Takeaways

1. **Large Result Sets are Purely CPU-Bound in Python:**
   * Deserializing 1,000 rows across 12 columns consumes **~302 ms of CPU time per request** under the GIL.
   * `proto-plus` dynamic field access (`get_rule`, `isinstance`, `to_python`) and dynamic type coercions (`from_rfc3339`) dominate execution.
2. **Impact of Native Shared Core:**
   * Offloading `PartialResultSet` chunk reassembly and row decoding to compiled native code (Rust/Go) avoids per-cell `PyObject` heap allocations, eliminating ~90%+ of this CPU cost.

---

## 5. How to Re-Run the Benchmark Suite

```bash
# 1. Run benchmark suite (outputs .prof files)
python3 spanner_cpu_profile_suite.py

# 2. Export interactive HTML flame graphs (pure Python, zero dependencies)
python3 export_flamegraph_html.py
```
