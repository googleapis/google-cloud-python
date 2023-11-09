# Copyright 2023 Google LLC
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

import ibis.expr.types as ibis_types
import pandas

import bigframes.core as core
import bigframes.core.ordering
import bigframes.operations as ops
import bigframes.operations.aggregations as agg_ops

from . import resources


def test_arrayvalue_constructor_from_ibis_table_adds_all_columns():
    session = resources.create_pandas_session(
        {
            "test_table": pandas.DataFrame(
                {
                    "col1": [1, 2, 3],
                    "not_included": [True, False, True],
                    "col2": ["a", "b", "c"],
                    "col3": [0.1, 0.2, 0.3],
                }
            )
        }
    )
    ibis_table = session.ibis_client.table("test_table")
    columns = (ibis_table["col1"], ibis_table["col2"], ibis_table["col3"])
    ordering = bigframes.core.ordering.ExpressionOrdering(
        tuple([core.OrderingColumnReference("col1")]),
        total_ordering_columns=frozenset(["col1"]),
    )
    actual = core.ArrayValue.from_ibis(
        session=session,
        table=ibis_table,
        columns=columns,
        ordering=ordering,
        hidden_ordering_columns=(),
    )
    assert actual._compile_ordered()._table is ibis_table
    assert len(actual.column_ids) == 3


def test_arrayvalue_with_get_column_type():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    col1_type = value.get_column_type("col1")
    col2_type = value.get_column_type("col2")
    col3_type = value.get_column_type("col3")
    assert isinstance(col1_type, pandas.Int64Dtype)
    assert isinstance(col2_type, pandas.StringDtype)
    assert isinstance(col3_type, pandas.Float64Dtype)


def test_arrayvalue_with_get_column():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    col1 = value._compile_ordered()._get_ibis_column("col1")
    assert isinstance(col1, ibis_types.Value)
    assert col1.get_name() == "col1"
    assert col1.type().is_int64()


def test_arrayvalues_to_ibis_expr_with_get_column():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value._compile_ordered()._get_ibis_column("col1")
    assert expr.get_name() == "col1"
    assert expr.type().is_int64()


def test_arrayvalues_to_ibis_expr_with_concat():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.concat([value])
    actual = expr._compile_ordered()._to_ibis_expr(ordering_mode="unordered")
    assert len(actual.columns) == 3
    # TODO(ashleyxu, b/299631930): test out the union expression
    assert actual.columns[0] == "column_0"
    assert actual.columns[1] == "column_1"
    assert actual.columns[2] == "column_2"


def test_arrayvalues_to_ibis_expr_with_project_unary_op():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.project_unary_op("col1", ops.AsTypeOp("string"))._compile_ordered()
    assert value._compile_ordered().columns[0].type().is_int64()
    assert expr.columns[0].type().is_string()


def test_arrayvalues_to_ibis_expr_with_project_binary_op():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.2, 0.3, 0.4],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.project_binary_op(
        "col2", "col3", ops.add_op, "col4"
    )._compile_ordered()
    assert expr.columns[3].type().is_float64()
    actual = expr._to_ibis_expr(ordering_mode="unordered")
    assert len(expr.columns) == 4
    assert actual.columns[3] == "col4"


def test_arrayvalues_to_ibis_expr_with_project_ternary_op():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": [0.2, 0.3, 0.4],
                "col3": [True, False, False],
                "col4": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.project_ternary_op(
        "col2", "col3", "col4", ops.where_op, "col5"
    )._compile_ordered()
    assert expr.columns[4].type().is_float64()
    actual = expr._to_ibis_expr(ordering_mode="unordered")
    assert len(expr.columns) == 5
    assert actual.columns[4] == "col5"


def test_arrayvalue_to_ibis_expr_with_aggregate():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.aggregate(
        aggregations=(("col1", agg_ops.sum_op, "col4"),),
        by_column_ids=["col1"],
        dropna=False,
    )._compile_ordered()
    actual = expr._to_ibis_expr(ordering_mode="unordered")
    assert len(expr.columns) == 2
    assert actual.columns[0] == "col1"
    assert actual.columns[1] == "col4"
    assert expr.columns[1].type().is_int64()


def test_arrayvalue_to_ibis_expr_with_corr_aggregate():
    value = resources.create_arrayvalue(
        pandas.DataFrame(
            {
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [0.1, 0.2, 0.3],
            }
        ),
        total_ordering_columns=["col1"],
    )
    expr = value.corr_aggregate(
        corr_aggregations=[("col1", "col3", "col4")]
    )._compile_ordered()
    actual = expr._to_ibis_expr(ordering_mode="unordered")
    assert len(expr.columns) == 1
    assert actual.columns[0] == "col4"
    assert expr.columns[0].type().is_float64()
