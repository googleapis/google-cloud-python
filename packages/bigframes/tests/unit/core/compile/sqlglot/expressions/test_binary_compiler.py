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

import typing

import pytest

from bigframes import operations as ops
import bigframes.core.expression as ex
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_binary_op(
    obj: bpd.DataFrame,
    op: ops.BinaryOp,
    l_arg: str,
    r_arg: typing.Union[str, ex.Expression],
) -> str:
    array_value = obj._block.expr
    op_expr = op.as_expr(l_arg, r_arg)
    result, col_ids = array_value.compute_values([op_expr])

    # Rename columns for deterministic golden SQL results.
    assert len(col_ids) == 1
    result = result.rename_columns({col_ids[0]: l_arg}).select_columns([l_arg])

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_add_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_binary_op(bf_df, ops.add_op, "int64_col", "int64_col")
    snapshot.assert_match(sql, "out.sql")


def test_add_numeric_w_scalar(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_binary_op(bf_df, ops.add_op, "int64_col", ex.const(1))
    snapshot.assert_match(sql, "out.sql")


def test_add_string(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_binary_op(bf_df, ops.add_op, "string_col", ex.const("a"))
    snapshot.assert_match(sql, "out.sql")


def test_json_set(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_binary_op(
        bf_df, ops.JSONSet(json_path="$.a"), "json_col", ex.const(100)
    )
    snapshot.assert_match(sql, "out.sql")
