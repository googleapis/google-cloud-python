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
