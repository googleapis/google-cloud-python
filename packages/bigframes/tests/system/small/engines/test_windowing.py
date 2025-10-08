# Copyright 2025 Google LLC
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

from google.cloud import bigquery
import pytest

from bigframes.core import (
    agg_expressions,
    array_value,
    events,
    expression,
    identifiers,
    nodes,
    window_spec,
)
import bigframes.operations.aggregations as agg_ops
from bigframes.session import direct_gbq_execution, polars_executor
from bigframes.testing.engine_utils import assert_equivalence_execution

pytest.importorskip("polars")

# Polars used as reference as its fast and local. Generally though, prefer gbq engine where they disagree.
REFERENCE_ENGINE = polars_executor.PolarsExecutor()


@pytest.mark.parametrize("engine", ["polars", "bq", "bq-sqlglot"], indirect=True)
def test_engines_with_offsets(
    scalars_array_value: array_value.ArrayValue,
    engine,
):
    result, _ = scalars_array_value.promote_offsets()
    assert_equivalence_execution(result.node, REFERENCE_ENGINE, engine)


@pytest.mark.parametrize("never_skip_nulls", [True, False])
@pytest.mark.parametrize("agg_op", [agg_ops.sum_op, agg_ops.count_op])
def test_engines_with_rows_window(
    scalars_array_value: array_value.ArrayValue,
    bigquery_client: bigquery.Client,
    never_skip_nulls,
    agg_op,
):
    window = window_spec.WindowSpec(
        bounds=window_spec.RowsWindowBounds.from_window_size(3, "left"),
    )
    window_node = nodes.WindowOpNode(
        child=scalars_array_value.node,
        expression=agg_expressions.UnaryAggregation(
            agg_op, expression.deref("int64_too")
        ),
        window_spec=window,
        output_name=identifiers.ColumnId("agg_int64"),
        never_skip_nulls=never_skip_nulls,
        skip_reproject_unsafe=False,
    )

    publisher = events.Publisher()
    bq_executor = direct_gbq_execution.DirectGbqExecutor(
        bigquery_client, publisher=publisher
    )
    bq_sqlgot_executor = direct_gbq_execution.DirectGbqExecutor(
        bigquery_client, compiler="sqlglot", publisher=publisher
    )
    assert_equivalence_execution(window_node, bq_executor, bq_sqlgot_executor)
