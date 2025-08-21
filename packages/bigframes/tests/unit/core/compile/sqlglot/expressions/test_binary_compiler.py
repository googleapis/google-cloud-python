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

import pandas as pd
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
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_add_int"] = bf_df["int64_col"] + bf_df["int64_col"]
    bf_df["int_add_1"] = bf_df["int64_col"] + 1

    bf_df["int_add_bool"] = bf_df["int64_col"] + bf_df["bool_col"]
    bf_df["bool_add_int"] = bf_df["bool_col"] + bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_add_string(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = _apply_binary_op(bf_df, ops.add_op, "string_col", ex.const("a"))

    snapshot.assert_match(sql, "out.sql")


def test_add_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "date_col"]]
    timedelta = pd.Timedelta(1, unit="d")

    bf_df["date_add_timedelta"] = bf_df["date_col"] + timedelta
    bf_df["timestamp_add_timedelta"] = bf_df["timestamp_col"] + timedelta
    bf_df["timedelta_add_date"] = timedelta + bf_df["date_col"]
    bf_df["timedelta_add_timestamp"] = timedelta + bf_df["timestamp_col"]
    bf_df["timedelta_add_timedelta"] = timedelta + timedelta

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_add_unsupported_raises(scalar_types_df: bpd.DataFrame):
    with pytest.raises(TypeError):
        _apply_binary_op(scalar_types_df, ops.add_op, "timestamp_col", "date_col")

    with pytest.raises(TypeError):
        _apply_binary_op(scalar_types_df, ops.add_op, "int64_col", "string_col")


def test_div_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col", "float64_col"]]

    bf_df["int_div_int"] = bf_df["int64_col"] / bf_df["int64_col"]
    bf_df["int_div_1"] = bf_df["int64_col"] / 1
    bf_df["int_div_0"] = bf_df["int64_col"] / 0.0

    bf_df["int_div_float"] = bf_df["int64_col"] / bf_df["float64_col"]
    bf_df["float_div_int"] = bf_df["float64_col"] / bf_df["int64_col"]
    bf_df["float_div_0"] = bf_df["float64_col"] / 0.0

    bf_df["int_div_bool"] = bf_df["int64_col"] / bf_df["bool_col"]
    bf_df["bool_div_int"] = bf_df["bool_col"] / bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_div_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "int64_col"]]
    timedelta = pd.Timedelta(1, unit="d")
    bf_df["timedelta_div_numeric"] = timedelta / bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_eq_null_match(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]
    sql = _apply_binary_op(bf_df, ops.eq_null_match_op, "int64_col", "bool_col")
    snapshot.assert_match(sql, "out.sql")


def test_eq_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_ne_int"] = bf_df["int64_col"] == bf_df["int64_col"]
    bf_df["int_ne_1"] = bf_df["int64_col"] == 1

    bf_df["int_ne_bool"] = bf_df["int64_col"] == bf_df["bool_col"]
    bf_df["bool_ne_int"] = bf_df["bool_col"] == bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_floordiv_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col", "float64_col"]]

    bf_df["int_div_int"] = bf_df["int64_col"] // bf_df["int64_col"]
    bf_df["int_div_1"] = bf_df["int64_col"] // 1
    bf_df["int_div_0"] = bf_df["int64_col"] // 0.0

    bf_df["int_div_float"] = bf_df["int64_col"] // bf_df["float64_col"]
    bf_df["float_div_int"] = bf_df["float64_col"] // bf_df["int64_col"]
    bf_df["float_div_0"] = bf_df["float64_col"] // 0.0

    bf_df["int_div_bool"] = bf_df["int64_col"] // bf_df["bool_col"]
    bf_df["bool_div_int"] = bf_df["bool_col"] // bf_df["int64_col"]


def test_floordiv_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "date_col"]]
    timedelta = pd.Timedelta(1, unit="d")

    bf_df["timedelta_div_numeric"] = timedelta // 2

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_json_set(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = _apply_binary_op(
        bf_df, ops.JSONSet(json_path="$.a"), "json_col", ex.const(100)
    )

    snapshot.assert_match(sql, "out.sql")


def test_sub_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_add_int"] = bf_df["int64_col"] - bf_df["int64_col"]
    bf_df["int_add_1"] = bf_df["int64_col"] - 1

    bf_df["int_add_bool"] = bf_df["int64_col"] - bf_df["bool_col"]
    bf_df["bool_add_int"] = bf_df["bool_col"] - bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_sub_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "duration_col", "date_col"]]
    bf_df["duration_col"] = bpd.to_timedelta(bf_df["duration_col"], unit="us")

    bf_df["date_sub_timedelta"] = bf_df["date_col"] - bf_df["duration_col"]
    bf_df["timestamp_sub_timedelta"] = bf_df["timestamp_col"] - bf_df["duration_col"]
    bf_df["timestamp_sub_date"] = bf_df["date_col"] - bf_df["date_col"]
    bf_df["date_sub_timestamp"] = bf_df["timestamp_col"] - bf_df["timestamp_col"]
    bf_df["timedelta_sub_timedelta"] = bf_df["duration_col"] - bf_df["duration_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_sub_unsupported_raises(scalar_types_df: bpd.DataFrame):
    with pytest.raises(TypeError):
        _apply_binary_op(scalar_types_df, ops.sub_op, "string_col", "string_col")

    with pytest.raises(TypeError):
        _apply_binary_op(scalar_types_df, ops.sub_op, "int64_col", "string_col")


def test_mul_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_mul_int"] = bf_df["int64_col"] * bf_df["int64_col"]
    bf_df["int_mul_1"] = bf_df["int64_col"] * 1

    bf_df["int_mul_bool"] = bf_df["int64_col"] * bf_df["bool_col"]
    bf_df["bool_mul_int"] = bf_df["bool_col"] * bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_mul_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "int64_col", "duration_col"]]
    bf_df["duration_col"] = bpd.to_timedelta(bf_df["duration_col"], unit="us")

    bf_df["timedelta_mul_numeric"] = bf_df["duration_col"] * bf_df["int64_col"]
    bf_df["numeric_mul_timedelta"] = bf_df["int64_col"] * bf_df["duration_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_obj_make_ref(scalar_types_df: bpd.DataFrame, snapshot):
    blob_df = scalar_types_df["string_col"].str.to_blob()
    snapshot.assert_match(blob_df.to_frame().sql, "out.sql")


def test_ne_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_ne_int"] = bf_df["int64_col"] != bf_df["int64_col"]
    bf_df["int_ne_1"] = bf_df["int64_col"] != 1

    bf_df["int_ne_bool"] = bf_df["int64_col"] != bf_df["bool_col"]
    bf_df["bool_ne_int"] = bf_df["bool_col"] != bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")
