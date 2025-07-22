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


def test_arccosh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arccosh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arccos(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arccos_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arcsin(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arcsin_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arcsinh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arcsinh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arctan(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arctan_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_arctanh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.arctanh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_abs(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.abs_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_capitalize(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.capitalize_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_ceil(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.ceil_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_date(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.date_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_day(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.day_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_dayofweek(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.dayofweek_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_dayofyear(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.dayofyear_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_exp(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.exp_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_expm1(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.expm1_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_floor(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.floor_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


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


def test_cos(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.cos_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_cosh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.cosh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_hash(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.hash_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_hour(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.hour_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_invert(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    sql = _apply_unary_op(bf_df, ops.invert_op, "int64_col")

    snapshot.assert_match(sql, "out.sql")


def test_isalnum(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isalnum_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isalpha(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isalpha_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isdecimal(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isdecimal_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isdigit(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isdigit_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_islower(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.islower_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isnumeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isnumeric_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isspace(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isspace_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_isupper(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_unary_op(bf_df, ops.isupper_op, "string_col")

    snapshot.assert_match(sql, "out.sql")


def test_iso_day(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.iso_day_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_iso_week(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col"]]
    sql = _apply_unary_op(bf_df, ops.iso_week_op, "timestamp_col")

    snapshot.assert_match(sql, "out.sql")


def test_isnull(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.isnull_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_notnull(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.notnull_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_sin(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.sin_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_sinh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.sinh_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_tan(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.tan_op, "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_tanh(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["float64_col"]]
    sql = _apply_unary_op(bf_df, ops.tanh_op, "float64_col")

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
