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

import pyarrow as pa
import pytest

from bigframes.core import identifiers, local_data, nodes
from bigframes.session import substrait_executor
from bigframes.testing import mocks
import bigframes.core.expression as ex


class MockConsumer(substrait_executor.SubstraitConsumer):
    def consume(self, plan: bytes, tables: dict[str, pa.Table]) -> pa.Table:
        # Return a simple table regardless of the plan
        return pa.Table.from_pydict({"a": [1, 2, 3]})


@pytest.fixture
def object_under_test():
    return substrait_executor.SubstraitExecutor(MockConsumer())


def create_read_local_node():
    session = mocks.create_bigquery_session()
    arrow_table = pa.Table.from_pydict({"a": [1, 2, 3]})
    local_data_source = local_data.ManagedArrowTable.from_pyarrow(arrow_table)
    return nodes.ReadLocalNode(
        local_data_source=local_data_source,
        session=session,
        scan_list=nodes.ScanList(
            items=(
                nodes.ScanItem(
                    id=identifiers.ColumnId("a"),
                    source_id="a",
                ),
            )
        ),
    )


def test_substrait_executor_execute(object_under_test):
    plan = create_read_local_node()
    
    result = object_under_test.execute(plan, ordered=True)
    assert result is not None
    
    # Verify the result table
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 3
    assert result_table.column_names == ["a"]
    assert result_table.column("a").to_pylist() == [1, 2, 3]


def test_substrait_executor_unsupported_node(object_under_test):
    # ConcatNode is not supported by our skeletal compiler
    session = mocks.create_bigquery_session()
    read_node = create_read_local_node()
    plan = nodes.ConcatNode(
        children=(read_node, read_node),
        output_ids=(identifiers.ColumnId("concat"),),
    )
    
    result = object_under_test.execute(plan, ordered=True)
    assert result is None


def test_execute_projection_literal_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    read_node = create_read_local_node()
    
    assignment_expr = ex.ScalarConstantExpression(42)
    plan = nodes.ProjectionNode(
        child=read_node,
        assignments=((assignment_expr, identifiers.ColumnId("b")),),
    )
    
    result = executor.execute(plan, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 3
    assert "b" in result_table.column_names
    # Depending on our passthrough implementation, "a" should also be there.
    # Our _compile_projection passes through child fields!
    assert "a" in result_table.column_names
    assert result_table.column("b").to_pylist() == [42, 42, 42]


def test_execute_projection_add_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    from bigframes.operations.numeric_ops import add_op
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    read_node = create_read_local_node()
    
    # a + 42
    add_expr = ex.OpExpression(
        op=add_op,
        inputs=(
            ex.DerefOp(identifiers.ColumnId("a")),
            ex.ScalarConstantExpression(42),
        ),
    )
    plan = nodes.ProjectionNode(
        child=read_node,
        assignments=((add_expr, identifiers.ColumnId("b")),),
    )
    
    result = executor.execute(plan, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 3
    assert "b" in result_table.column_names
    assert "a" in result_table.column_names
    assert result_table.column("b").to_pylist() == [43, 44, 45]


def test_execute_filter_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    from bigframes.operations.comparison_ops import gt_op
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    read_node = create_read_local_node()
    
    # a > 1
    filter_expr = ex.OpExpression(
        op=gt_op,
        inputs=(
            ex.DerefOp(identifiers.ColumnId("a")),
            ex.ScalarConstantExpression(1),
        ),
    )
    plan = nodes.FilterNode(
        child=read_node,
        predicate=filter_expr,
    )
    
    result = executor.execute(plan, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 2
    assert "a" in result_table.column_names
    assert result_table.column("a").to_pylist() == [2, 3]


def test_execute_aggregate_sum_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    from bigframes.operations.aggregations import sum_op
    from bigframes.core.agg_expressions import UnaryAggregation
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    read_node = create_read_local_node()
    
    # sum(a)
    sum_agg = UnaryAggregation(
        op=sum_op,
        arg=ex.DerefOp(identifiers.ColumnId("a")),
    )
    
    plan = nodes.AggregateNode(
        child=read_node,
        aggregations=((sum_agg, identifiers.ColumnId("sum_a")),),
        by_column_ids=(),
    )
    
    result = executor.execute(plan, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 1
    assert "sum_a" in result_table.column_names
    assert result_table.column("sum_a").to_pylist() == [6]


def test_execute_aggregate_max_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    from bigframes.operations.aggregations import max_op
    from bigframes.core.agg_expressions import UnaryAggregation
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    read_node = create_read_local_node()
    
    # max(a)
    max_agg = UnaryAggregation(
        op=max_op,
        arg=ex.DerefOp(identifiers.ColumnId("a")),
    )
    
    plan = nodes.AggregateNode(
        child=read_node,
        aggregations=((max_agg, identifiers.ColumnId("max_a")),),
        by_column_ids=(),
    )
    
    result = executor.execute(plan, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 1
    assert "max_a" in result_table.column_names
    assert result_table.column("max_a").to_pylist() == [3]


def test_execute_join_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    # Table 1: a
    session1 = mocks.create_bigquery_session()
    table1 = pa.Table.from_pydict({"a": [1, 2, 3]})
    source1 = local_data.ManagedArrowTable.from_pyarrow(table1)
    col_id_a = identifiers.ColumnId("a")
    read_node1 = nodes.ReadLocalNode(
        local_data_source=source1,
        session=session1,
        scan_list=nodes.ScanList(items=(nodes.ScanItem(id=col_id_a, source_id="a"),)),
    )
    
    # Table 2: b
    session2 = mocks.create_bigquery_session()
    table2 = pa.Table.from_pydict({"b": [2, 3, 4]})
    source2 = local_data.ManagedArrowTable.from_pyarrow(table2)
    col_id_b = identifiers.ColumnId("b")
    read_node2 = nodes.ReadLocalNode(
        local_data_source=source2,
        session=session2,
        scan_list=nodes.ScanList(items=(nodes.ScanItem(id=col_id_b, source_id="b"),)),
    )
    
    # Join on a = b
    join_node = nodes.JoinNode(
        left_child=read_node1,
        right_child=read_node2,
        conditions=((ex.DerefOp(col_id_a), ex.DerefOp(col_id_b)),),
        type="inner",
        propogate_order=False,
    )
    
    result = executor.execute(join_node, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 2
    assert "a" in result_table.column_names
    assert "b" in result_table.column_names
    assert result_table.column("a").to_pylist() == [2, 3]
    assert result_table.column("b").to_pylist() == [2, 3]


def test_execute_selection_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    from bigframes.core.nodes import AliasedRef
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    # Table with a and b
    session = mocks.create_bigquery_session()
    table = pa.Table.from_pydict({"a": [1, 2, 3], "b": [4, 5, 6]})
    source = local_data.ManagedArrowTable.from_pyarrow(table)
    col_id_a = identifiers.ColumnId("a")
    col_id_b = identifiers.ColumnId("b")
    read_node = nodes.ReadLocalNode(
        local_data_source=source,
        session=session,
        scan_list=nodes.ScanList(
            items=(
                nodes.ScanItem(id=col_id_a, source_id="a"),
                nodes.ScanItem(id=col_id_b, source_id="b"),
            )
        ),
    )
    
    # Select only a, and rename it to c
    col_id_c = identifiers.ColumnId("c")
    selection_node = nodes.SelectionNode(
        child=read_node,
        input_output_pairs=(AliasedRef(ex.DerefOp(col_id_a), col_id_c),),
    )
    
    result = executor.execute(selection_node, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 3
    assert result_table.column_names == ["c"]
    assert result_table.column("c").to_pylist() == [1, 2, 3]


def test_execute_various_types_with_datafusion():
    from bigframes.session.substrait_executor import DataFusionSubstraitConsumer
    import datetime
    import pandas as pd
    
    consumer = DataFusionSubstraitConsumer()
    executor = substrait_executor.SubstraitExecutor(consumer)
    
    session = mocks.create_bigquery_session()
    table = pa.Table.from_pydict({
        "bin": [b"a", b"b"],
        "dat": [datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)],
        "dt": [datetime.datetime(2023, 1, 1, 12, 0), datetime.datetime(2023, 1, 2, 12, 0)],
    })
    source = local_data.ManagedArrowTable.from_pyarrow(table)
    
    scan_items = []
    for name in table.column_names:
         scan_items.append(nodes.ScanItem(id=identifiers.ColumnId(name), source_id=name))
         
    read_node = nodes.ReadLocalNode(
        local_data_source=source,
        session=session,
        scan_list=nodes.ScanList(items=tuple(scan_items)),
    )
    
    result = executor.execute(read_node, ordered=True)
    assert result is not None
    
    result_table = pa.Table.from_batches(result.batches().arrow_batches)
    assert result_table.num_rows == 2
    assert result_table.column_names == ["bin", "dat", "dt"]
