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

import pytest

from bigframes import operations as ops
from bigframes.core import expression
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.operations.aggregations as agg_ops
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ArrayToStringOp(delimiter=".").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_index(1).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_reduce_op(repeated_types_df: bpd.DataFrame, snapshot):
    ops_map = {
        "sum_float": ops.ArrayReduceOp(agg_ops.SumOp()).as_expr("float_list_col"),
        "std_float": ops.ArrayReduceOp(agg_ops.StdOp()).as_expr("float_list_col"),
        "count_str": ops.ArrayReduceOp(agg_ops.CountOp()).as_expr("string_list_col"),
        "any_bool": ops.ArrayReduceOp(agg_ops.AnyOp()).as_expr("bool_list_col"),
    }

    sql = utils._apply_ops_to_sql(
        repeated_types_df, list(ops_map.values()), list(ops_map.keys())
    )
    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_slice(slice(1, None)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    col_name = "string_list_col"
    bf_df = repeated_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [convert_slice(slice(1, 5)).as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_to_array_op(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col", "float64_col", "string_col"]]
    # Bigquery won't allow you to materialize arrays with null, so use non-nullable
    int64_non_null = ops.coalesce_op.as_expr("int64_col", expression.const(0))
    bool_col_non_null = ops.coalesce_op.as_expr("bool_col", expression.const(False))
    float_col_non_null = ops.coalesce_op.as_expr("float64_col", expression.const(0.0))
    string_col_non_null = ops.coalesce_op.as_expr("string_col", expression.const(""))

    ops_map = {
        "bool_col": ops.ToArrayOp().as_expr(bool_col_non_null),
        "int64_col": ops.ToArrayOp().as_expr(int64_non_null),
        "strs_col": ops.ToArrayOp().as_expr(string_col_non_null, string_col_non_null),
        "numeric_col": ops.ToArrayOp().as_expr(
            int64_non_null, bool_col_non_null, float_col_non_null
        ),
    }

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")
