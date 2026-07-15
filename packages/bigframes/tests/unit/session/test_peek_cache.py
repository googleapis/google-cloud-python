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

from __future__ import annotations

from unittest import mock

import pyarrow as pa

import bigframes
from bigframes.core import identifiers, local_data, nodes
from bigframes.session import execution_spec, executor
from bigframes.session.peek_cache import PeekCache, substitute_peek_cached_subplans
from bigframes.testing import mocks


def test_peek_cache_lru():
    cache = PeekCache(capacity=2)
    session = mocks.create_bigquery_session()

    # Create some mock nodes and data sources
    table1 = pa.Table.from_pydict({"a": [1, 2]})
    table2 = pa.Table.from_pydict({"b": [3, 4]})
    table3 = pa.Table.from_pydict({"c": [5, 6]})

    ds1 = local_data.ManagedArrowTable.from_pyarrow(table1)
    ds2 = local_data.ManagedArrowTable.from_pyarrow(table2)
    ds3 = local_data.ManagedArrowTable.from_pyarrow(table3)

    node1 = nodes.ReadLocalNode(ds1, nodes.ScanList(()), session)
    node2 = nodes.ReadLocalNode(ds2, nodes.ScanList(()), session)
    node3 = nodes.ReadLocalNode(ds3, nodes.ScanList(()), session)

    cache.put(node1, ds1)
    cache.put(node2, ds2)

    # Access node1 to make it most recently used, leaving node2 as least recently used (LRU)
    assert cache.get(node1).table == ds1

    # Put node3, which should evict node2
    cache.put(node3, ds3)

    assert cache.get(node2) is None
    assert cache.get(node1).table == ds1
    assert cache.get(node3).table == ds3


def test_substitute_peek_cached_subplans():
    session = mocks.create_bigquery_session()
    table = pa.Table.from_pydict({"a": [1, 2]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)

    # Create a simple leaf node
    leaf = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col_a"), "a"),)),
        session=session,
    )

    # Cache the leaf node
    cache = PeekCache()
    cached_table = pa.Table.from_pydict({"col_a": [100, 200]})
    cached_ds = local_data.ManagedArrowTable.from_pyarrow(cached_table)
    cache.put(leaf, cached_ds)

    # Now perform the tree substitution
    rewritten = substitute_peek_cached_subplans(leaf, cache, min_rows_required=1)

    # The leaf should be replaced by a new ReadLocalNode containing cached_ds
    assert isinstance(rewritten, nodes.ReadLocalNode)
    assert rewritten.local_data_source == cached_ds
    assert rewritten.session == session
    assert len(rewritten.scan_list.items) == 1
    assert rewritten.scan_list.items[0].id == identifiers.ColumnId("col_a")
    assert rewritten.scan_list.items[0].source_id == "col_a"


def test_executor_peek_cache_integration():
    from bigframes.session import semi_executor
    from bigframes.session.peek_cache_executor import PeekCacheExecutor

    # Mock target executor
    mock_target = mock.create_autospec(executor.Executor, instance=True)
    publisher = mock.AsyncMock()

    # Mock PolarsExecutor
    mock_polars_executor = mock.create_autospec(
        semi_executor.SemiExecutor, instance=True
    )

    table = pa.Table.from_pydict({"col": [1, 2, 3, 4, 5]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)
    session = mocks.create_bigquery_session()

    node = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col"), "col"),)),
        session=session,
    )
    arr_value = bigframes.core.ArrayValue(node)

    # Mock target.execute to return a mock 3-row table
    mock_bq_table = pa.Table.from_pydict({"col": [10, 20, 30]})
    mock_bq_result = executor.LocalExecuteResult(mock_bq_table, arr_value.schema)
    mock_target.execute.return_value = mock_bq_result

    # Enable peek cache options
    compute_options = bigframes.options.compute
    compute_options.enable_peek_cache = True
    compute_options.peek_cache_size = 3

    # Patch PolarsExecutor
    with mock.patch(
        "bigframes.session.polars_executor.PolarsExecutor",
        return_value=mock_polars_executor,
    ):
        peek_cache_executor = PeekCacheExecutor(mock_target, publisher=publisher)

    # Call execute with peek=1 (cache miss path)
    spec = execution_spec.ExecutionSpec(peek=1).with_compute_options(compute_options)
    result = peek_cache_executor.execute(arr_value, spec)

    # Verify target.execute was called with peek=3 (cache size)
    assert mock_target.execute.call_count == 1
    called_spec = mock_target.execute.call_args[0][1]
    assert called_spec.peek == 3

    # Verify returned result has exactly 1 row
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 1
    assert result_table["col"].to_pylist() == [10]

    # Verify peek cache has been populated with the 3-row table
    cached_entry = peek_cache_executor._peek_cache.get(node)
    assert cached_entry is not None
    assert cached_entry.table.to_pyarrow_table()["col"].to_pylist() == [10, 20, 30]

    # Mock polars executor to return a 2-row table on cache hit
    mock_polars_table = pa.Table.from_pydict({"col": [10, 20]})
    mock_polars_result = executor.LocalExecuteResult(
        mock_polars_table, arr_value.schema
    )
    mock_polars_executor.execute = mock.AsyncMock(return_value=mock_polars_result)

    # Call execute again with peek=2 (cache hit path)
    mock_target.execute.reset_mock()
    spec2 = execution_spec.ExecutionSpec(peek=2).with_compute_options(compute_options)
    result2 = peek_cache_executor.execute(arr_value, spec2)

    # Verify target.execute was NOT called
    assert mock_target.execute.call_count == 0

    # Verify polars executor was called with the rewritten node
    assert mock_polars_executor.execute.call_count == 1
    called_node = mock_polars_executor.execute.call_args[0][0]
    assert isinstance(called_node, nodes.ReadLocalNode)
    assert called_node.local_data_source.to_pyarrow_table()["col"].to_pylist() == [
        10,
        20,
        30,
    ]

    # Verify returned result has exactly 2 rows
    result_table2 = pa.Table.from_batches(result2.batches().arrow_batches)
    assert result_table2.num_rows == 2
    assert result_table2["col"].to_pylist() == [10, 20]


def test_peek_cache_thread_safety():
    import threading

    cache = PeekCache(capacity=100)
    session = mocks.create_bigquery_session()

    # Create dummy nodes and data sources
    num_items = 50
    num_threads = 10
    nodes_list = []
    for i in range(num_items):
        table = pa.Table.from_pydict({"col": [i]})
        ds = local_data.ManagedArrowTable.from_pyarrow(table)
        node = nodes.ReadLocalNode(ds, nodes.ScanList(()), session)
        nodes_list.append((node, ds))

    def worker(worker_id):
        for i in range(100):
            node, ds = nodes_list[(worker_id + i) % num_items]
            cache.put(node, ds)
            cache.get(node)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # The cache should be in a consistent state and not exceed capacity
    assert len(cache._cache) <= 100


def test_substitute_peek_cached_subplans_incompatible_ancestors():
    session = mocks.create_bigquery_session()
    table = pa.Table.from_pydict({"a": [1, 2]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)

    # Leaf node (cached)
    leaf = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col_a"), "a"),)),
        session=session,
    )

    cache = PeekCache()
    cached_table = pa.Table.from_pydict({"col_a": [100, 200]})
    cached_ds = local_data.ManagedArrowTable.from_pyarrow(cached_table)
    cache.put(leaf, cached_ds)

    # Scenario A: Path has only compatible nodes: FilterNode -> Leaf
    # FilterNode is a compatible ancestor.
    plan_compatible = nodes.FilterNode(
        child=leaf,
        predicate=bigframes.core.expression.ScalarConstantExpression(
            True
        ),  # Dummy expression
    )

    rewritten_compatible = substitute_peek_cached_subplans(
        plan_compatible, cache, min_rows_required=1
    )
    # The leaf child of FilterNode should be replaced by ReadLocalNode with cached_ds
    assert isinstance(rewritten_compatible, nodes.FilterNode)
    assert isinstance(rewritten_compatible.child, nodes.ReadLocalNode)
    assert rewritten_compatible.child.local_data_source == cached_ds

    # Scenario B: Path has an incompatible node: ReversedNode -> Leaf
    # ReversedNode is an incompatible ancestor.
    plan_incompatible = nodes.ReversedNode(child=leaf)

    rewritten_incompatible = substitute_peek_cached_subplans(
        plan_incompatible, cache, min_rows_required=1
    )
    # The leaf child should NOT be replaced by ReadLocalNode
    assert isinstance(rewritten_incompatible, nodes.ReversedNode)
    assert rewritten_incompatible.child == leaf
    assert rewritten_incompatible.child.local_data_source == ds


def test_substitute_peek_cached_subplans_insufficient_rows():
    session = mocks.create_bigquery_session()
    table = pa.Table.from_pydict({"a": [1, 2]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)

    # Leaf node (cached with a 2-row sample)
    leaf = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col_a"), "a"),)),
        session=session,
    )

    cache = PeekCache()
    cache.put(leaf, ds)

    # Request min_rows_required = 2 -> Should substitute
    rewritten_ok = substitute_peek_cached_subplans(leaf, cache, min_rows_required=2)
    assert isinstance(rewritten_ok, nodes.ReadLocalNode)
    assert rewritten_ok.local_data_source == ds

    # Request min_rows_required = 3 -> Should NOT substitute (insufficient rows)
    rewritten_ng = substitute_peek_cached_subplans(leaf, cache, min_rows_required=3)
    assert rewritten_ng == leaf


def test_executor_peek_cache_populates_from_full_execution():
    from bigframes.session.peek_cache_executor import PeekCacheExecutor

    # Mock target executor
    mock_target = mock.create_autospec(executor.Executor, instance=True)
    publisher = mock.AsyncMock()

    table = pa.Table.from_pydict({"col": [1, 2, 3, 4, 5]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)
    session = mocks.create_bigquery_session()

    node = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col"), "col"),)),
        session=session,
    )
    arr_value = bigframes.core.ArrayValue(node)

    # Mock target.execute to return a mock 5-row local result
    mock_result = executor.LocalExecuteResult(table, arr_value.schema)
    mock_target.execute.return_value = mock_result

    # Enable peek cache options with cache size = 3 (smaller than 5)
    compute_options = bigframes.options.compute
    compute_options.enable_peek_cache = True
    compute_options.peek_cache_size = 3

    # Mock PolarsExecutor to avoid ImportError if it's not installed in test env,
    # though it is not called on full execution path, but PeekCacheExecutor.__init__ tries to instantiate it.
    mock_polars_executor = mock.Mock()
    with mock.patch(
        "bigframes.session.polars_executor.PolarsExecutor",
        return_value=mock_polars_executor,
    ):
        peek_cache_executor = PeekCacheExecutor(mock_target, publisher=publisher)

    # Call execute with peek=None (full execution)
    spec = execution_spec.ExecutionSpec(peek=None).with_compute_options(compute_options)
    _ = peek_cache_executor.execute(arr_value, spec)

    # Verify target.execute was called
    assert mock_target.execute.call_count == 1

    # Verify peek cache has been populated and sliced to peek_cache_size (3)
    cached_entry = peek_cache_executor._peek_cache.get(node)
    assert cached_entry is not None
    assert not cached_entry.is_complete  # Sliced, so not complete
    assert cached_entry.table.to_pyarrow_table().num_rows == 3
    assert cached_entry.table.to_pyarrow_table()["col"].to_pylist() == [1, 2, 3]

    # Now test when full result is smaller than peek_cache_size (cache size = 10)
    compute_options.peek_cache_size = 10
    with mock.patch(
        "bigframes.session.polars_executor.PolarsExecutor",
        return_value=mock_polars_executor,
    ):
        peek_cache_executor2 = PeekCacheExecutor(mock_target, publisher=publisher)
    _ = peek_cache_executor2.execute(arr_value, spec)

    cached_entry2 = peek_cache_executor2._peek_cache.get(node)
    assert cached_entry2 is not None
    assert cached_entry2.is_complete  # Fits entirely, so complete!
    assert cached_entry2.table.to_pyarrow_table().num_rows == 5
    assert cached_entry2.table.to_pyarrow_table()["col"].to_pylist() == [1, 2, 3, 4, 5]


def test_executor_peek_cache_falls_back_on_insufficient_rows():
    from bigframes.session import semi_executor
    from bigframes.session.peek_cache_executor import PeekCacheExecutor

    # Mock target executor
    mock_target = mock.create_autospec(executor.Executor, instance=True)
    publisher = mock.AsyncMock()

    # Mock PolarsExecutor
    mock_polars_executor = mock.create_autospec(
        semi_executor.SemiExecutor, instance=True
    )

    table = pa.Table.from_pydict({"col": [1, 2, 3, 4, 5]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)
    session = mocks.create_bigquery_session()

    node = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col"), "col"),)),
        session=session,
    )
    arr_value = bigframes.core.ArrayValue(node)

    # Mock target.execute to return a mock 5-row BQ result
    mock_bq_table = pa.Table.from_pydict({"col": [10, 20, 30, 40, 50]})
    mock_bq_result = executor.LocalExecuteResult(mock_bq_table, arr_value.schema)
    mock_target.execute.return_value = mock_bq_result

    # Enable peek cache options
    compute_options = bigframes.options.compute
    compute_options.enable_peek_cache = True
    compute_options.peek_cache_size = 5

    with mock.patch(
        "bigframes.session.polars_executor.PolarsExecutor",
        return_value=mock_polars_executor,
    ):
        peek_cache_executor = PeekCacheExecutor(mock_target, publisher=publisher)

    # Populate the cache first with a different data source object to trigger rewrite
    cached_ds = local_data.ManagedArrowTable.from_pyarrow(table)
    peek_cache_executor._peek_cache.put(node, cached_ds)

    # Mock polars executor to return a 2-row table (insufficient for peek=5)
    mock_polars_table = pa.Table.from_pydict({"col": [1, 2]})
    mock_polars_result = executor.LocalExecuteResult(
        mock_polars_table, arr_value.schema
    )
    mock_polars_executor.execute = mock.AsyncMock(return_value=mock_polars_result)

    # Call execute with peek=5 (should trigger fallback because 2 < 5)
    spec = execution_spec.ExecutionSpec(peek=5).with_compute_options(compute_options)
    result = peek_cache_executor.execute(arr_value, spec)

    # Verify polars executor was called
    assert mock_polars_executor.execute.call_count == 1

    # Verify target.execute WAS called (fallback)
    assert mock_target.execute.call_count == 1
    called_spec = mock_target.execute.call_args[0][1]
    assert called_spec.peek == 5

    # Verify returned result is the BQ result
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 5
    assert result_table["col"].to_pylist() == [10, 20, 30, 40, 50]


def test_executor_complete_cache_local_execution():
    from bigframes.session import semi_executor
    from bigframes.session.peek_cache_executor import PeekCacheExecutor

    # Mock target executor
    mock_target = mock.create_autospec(executor.Executor, instance=True)
    publisher = mock.AsyncMock()

    # Mock PolarsExecutor
    mock_polars_executor = mock.create_autospec(
        semi_executor.SemiExecutor, instance=True
    )

    table = pa.Table.from_pydict({"col": [1, 2, 3, 4, 5]})
    ds = local_data.ManagedArrowTable.from_pyarrow(table)
    session = mocks.create_bigquery_session()

    node = nodes.ReadLocalNode(
        local_data_source=ds,
        scan_list=nodes.ScanList((nodes.ScanItem(identifiers.ColumnId("col"), "col"),)),
        session=session,
    )
    arr_value = bigframes.core.ArrayValue(node)

    # Enable peek cache options
    compute_options = bigframes.options.compute
    compute_options.enable_peek_cache = True

    with mock.patch(
        "bigframes.session.polars_executor.PolarsExecutor",
        return_value=mock_polars_executor,
    ):
        peek_cache_executor = PeekCacheExecutor(mock_target, publisher=publisher)

    # Populate the cache first as COMPLETE
    cached_ds = local_data.ManagedArrowTable.from_pyarrow(table)
    peek_cache_executor._peek_cache.put(node, cached_ds, is_complete=True)

    # Mock polars executor to return the full 5-row table
    mock_polars_result = executor.LocalExecuteResult(table, arr_value.schema)
    mock_polars_executor.execute = mock.AsyncMock(return_value=mock_polars_result)

    # Call execute with peek=None (full execution!)
    spec = execution_spec.ExecutionSpec(peek=None).with_compute_options(compute_options)
    result = peek_cache_executor.execute(arr_value, spec)

    # Verify polars executor was called
    assert mock_polars_executor.execute.call_count == 1

    # Verify target.execute was NOT called (no BQ query!)
    assert mock_target.execute.call_count == 0

    # Verify returned result is the local polars result
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 5
    assert result_table["col"].to_pylist() == [1, 2, 3, 4, 5]
