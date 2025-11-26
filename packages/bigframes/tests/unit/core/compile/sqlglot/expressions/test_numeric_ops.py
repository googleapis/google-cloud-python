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

import pandas as pd
import pytest

from bigframes import operations as ops
import bigframes.core.expression as ex
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_arccosh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arccosh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arccos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arccos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arcsin(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arcsin_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arcsinh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arcsinh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arctan2(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col", "bool_col"]]

    sql = utils._apply_ops_to_sql(
        bf_df,
        [
            ops.arctan2_op.as_expr("int64_col", "float64_col"),
            ops.arctan2_op.as_expr("bool_col", "float64_col"),
        ],
        ["int64_col", "bool_col"],
    )
    snapshot.assert_match(sql, "out.sql")


def test_arctan(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arctan_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_arctanh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.arctanh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_abs(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.abs_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_ceil(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.ceil_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_cos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.cos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_cosh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.cosh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_cosine_distance(repeated_types_df: bpd.DataFrame, snapshot):
    col_names = ["int_list_col", "float_list_col"]
    bf_df = repeated_types_df[col_names]

    sql = utils._apply_ops_to_sql(
        bf_df,
        [
            ops.cosine_distance_op.as_expr("int_list_col", "int_list_col"),
            ops.cosine_distance_op.as_expr("float_list_col", "float_list_col"),
        ],
        ["int_list_col", "float_list_col"],
    )
    snapshot.assert_match(sql, "out.sql")


def test_exp(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.exp_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_expm1(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.expm1_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_floor(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.floor_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_ln(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.ln_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_log10(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.log10_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_log1p(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.log1p_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_neg(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.neg_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_pos(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.pos_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_pow(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]

    bf_df["int_pow_int"] = bf_df["int64_col"] ** bf_df["int64_col"]
    bf_df["int_pow_float"] = bf_df["int64_col"] ** bf_df["float64_col"]
    bf_df["float_pow_int"] = bf_df["float64_col"] ** bf_df["int64_col"]
    bf_df["float_pow_float"] = bf_df["float64_col"] ** bf_df["float64_col"]

    bf_df["int_pow_0"] = bf_df["int64_col"] ** 0
    bf_df["float_pow_0"] = bf_df["float64_col"] ** 0
    bf_df["int_pow_1"] = bf_df["int64_col"] ** 1
    bf_df["float_pow_1"] = bf_df["float64_col"] ** 1

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_round(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]

    bf_df["int_round_0"] = bf_df["int64_col"].round(0)
    bf_df["int_round_1"] = bf_df["int64_col"].round(1)
    bf_df["int_round_m1"] = bf_df["int64_col"].round(-1)

    bf_df["float_round_0"] = bf_df["float64_col"].round(0)
    bf_df["float_round_1"] = bf_df["float64_col"].round(1)
    bf_df["float_round_m1"] = bf_df["float64_col"].round(-1)

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_sqrt(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.sqrt_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sin(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.sin_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_sinh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.sinh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_tan(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.tan_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_tanh(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "float64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.tanh_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_add_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_add_int"] = bf_df["int64_col"] + bf_df["int64_col"]
    bf_df["int_add_1"] = bf_df["int64_col"] + 1

    bf_df["int_add_bool"] = bf_df["int64_col"] + bf_df["bool_col"]
    bf_df["bool_add_int"] = bf_df["bool_col"] + bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_add_string(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["string_col"]]
    sql = utils._apply_binary_op(bf_df, ops.add_op, "string_col", ex.const("a"))

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
        utils._apply_binary_op(scalar_types_df, ops.add_op, "timestamp_col", "date_col")

    with pytest.raises(TypeError):
        utils._apply_binary_op(scalar_types_df, ops.add_op, "int64_col", "string_col")


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


def test_euclidean_distance(repeated_types_df: bpd.DataFrame, snapshot):
    col_names = ["int_list_col", "numeric_list_col"]
    bf_df = repeated_types_df[col_names]

    sql = utils._apply_ops_to_sql(
        bf_df,
        [
            ops.euclidean_distance_op.as_expr("int_list_col", "int_list_col"),
            ops.euclidean_distance_op.as_expr("numeric_list_col", "numeric_list_col"),
        ],
        ["int_list_col", "numeric_list_col"],
    )
    snapshot.assert_match(sql, "out.sql")


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


def test_manhattan_distance(repeated_types_df: bpd.DataFrame, snapshot):
    col_names = ["float_list_col", "numeric_list_col"]
    bf_df = repeated_types_df[col_names]

    sql = utils._apply_ops_to_sql(
        bf_df,
        [
            ops.manhattan_distance_op.as_expr("float_list_col", "float_list_col"),
            ops.manhattan_distance_op.as_expr("numeric_list_col", "numeric_list_col"),
        ],
        ["float_list_col", "numeric_list_col"],
    )
    snapshot.assert_match(sql, "out.sql")


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


def test_mod_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]

    bf_df["int_mod_int"] = bf_df["int64_col"] % bf_df["int64_col"]
    bf_df["int_mod_int_neg"] = bf_df["int64_col"] % -bf_df["int64_col"]
    bf_df["int_mod_1"] = bf_df["int64_col"] % 1
    bf_df["int_mod_0"] = bf_df["int64_col"] % 0

    bf_df["float_mod_float"] = bf_df["float64_col"] % bf_df["float64_col"]
    bf_df["float_mod_float_neg"] = bf_df["float64_col"] % -bf_df["float64_col"]
    bf_df["float_mod_1"] = bf_df["float64_col"] % 1
    bf_df["float_mod_0"] = bf_df["float64_col"] % 0

    snapshot.assert_match(bf_df.sql, "out.sql")


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
        utils._apply_binary_op(scalar_types_df, ops.sub_op, "string_col", "string_col")

    with pytest.raises(TypeError):
        utils._apply_binary_op(scalar_types_df, ops.sub_op, "int64_col", "string_col")


def test_unsafe_pow_op(scalar_types_df: bpd.DataFrame, snapshot):
    # Choose certain row so the sql execution won't fail even with unsafe_pow_op.
    bf_df = scalar_types_df[
        (scalar_types_df["int64_col"] >= 0) & (scalar_types_df["int64_col"] <= 10)
    ]
    bf_df = bf_df[["int64_col", "float64_col", "bool_col"]]

    int64_col_id = bf_df["int64_col"]._value_column
    float64_col_id = bf_df["float64_col"]._value_column
    bool_col_id = bf_df["bool_col"]._value_column

    sql = utils._apply_ops_to_sql(
        bf_df,
        [
            ops.unsafe_pow_op.as_expr(int64_col_id, int64_col_id),
            ops.unsafe_pow_op.as_expr(int64_col_id, float64_col_id),
            ops.unsafe_pow_op.as_expr(float64_col_id, int64_col_id),
            ops.unsafe_pow_op.as_expr(float64_col_id, float64_col_id),
            ops.unsafe_pow_op.as_expr(int64_col_id, bool_col_id),
            ops.unsafe_pow_op.as_expr(bool_col_id, int64_col_id),
        ],
        [
            "int_pow_int",
            "int_pow_float",
            "float_pow_int",
            "float_pow_float",
            "int_pow_bool",
            "bool_pow_int",
        ],
    )
    snapshot.assert_match(sql, "out.sql")
