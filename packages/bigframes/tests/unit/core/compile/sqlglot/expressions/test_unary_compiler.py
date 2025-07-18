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
from bigframes.operations._op_converters import convert_index, convert_slice
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def _apply_unary_op(obj: bpd.DataFrame, op: ops.UnaryOp, arg: str) -> str:
    array_value = obj._block.expr
    op_expr = op.as_expr(arg)
    result, col_ids = array_value.compute_values([op_expr])

    # Rename columns for deterministic golden SQL results.
    assert len(col_ids) == 1
    result = result.rename_columns({col_ids[0]: arg}).select_columns([arg])

    sql = result.session._executor.to_sql(result, enable_cache=False)
    return sql


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, ops.ArrayToStringOp(delimiter="."), "string_list_col")
    snapshot.assert_match(sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_index(1), "string_list_col")
    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_slice(slice(1, None)), "string_list_col")
    snapshot.assert_match(sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    bf_df = repeated_types_df[["string_list_col"]]
    sql = _apply_unary_op(bf_df, convert_slice(slice(1, 5)), "string_list_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_extract(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtract(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_extract_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtractArray(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_extract_string_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONExtractStringArray(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_query(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONQuery(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_query_array(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONQueryArray(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_json_value(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.JSONValue(json_path="$"), "json_col")
    snapshot.assert_match(sql, "out.sql")


def test_parse_json(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.ParseJSON(), "string_col")
    snapshot.assert_match(sql, "out.sql")


def test_to_json_string(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_unary_op(bf_df, ops.ToJSONString(), "json_col")
    snapshot.assert_match(sql, "out.sql")
