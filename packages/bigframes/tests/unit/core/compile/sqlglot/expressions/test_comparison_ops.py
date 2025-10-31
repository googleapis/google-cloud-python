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
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_is_in(scalar_types_df: bpd.DataFrame, snapshot):
    int_col = "int64_col"
    float_col = "float64_col"
    bf_df = scalar_types_df[[int_col, float_col]]
    ops_map = {
        "ints": ops.IsInOp(values=(1, 2, 3)).as_expr(int_col),
        "ints_w_null": ops.IsInOp(values=(None, 123456)).as_expr(int_col),
        "floats": ops.IsInOp(values=(1.0, 2.0, 3.0), match_nulls=False).as_expr(
            int_col
        ),
        "strings": ops.IsInOp(values=("1.0", "2.0")).as_expr(int_col),
        "mixed": ops.IsInOp(values=("1.0", 2.5, 3)).as_expr(int_col),
        "empty": ops.IsInOp(values=()).as_expr(int_col),
        "ints_wo_match_nulls": ops.IsInOp(
            values=(None, 123456), match_nulls=False
        ).as_expr(int_col),
        "float_in_ints": ops.IsInOp(values=(1, 2, 3, None)).as_expr(float_col),
    }

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_eq_null_match(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]
    sql = utils._apply_binary_op(bf_df, ops.eq_null_match_op, "int64_col", "bool_col")
    snapshot.assert_match(sql, "out.sql")


def test_eq_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_ne_int"] = bf_df["int64_col"] == bf_df["int64_col"]
    bf_df["int_ne_1"] = bf_df["int64_col"] == 1

    bf_df["int_ne_bool"] = bf_df["int64_col"] == bf_df["bool_col"]
    bf_df["bool_ne_int"] = bf_df["bool_col"] == bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_gt_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_gt_int"] = bf_df["int64_col"] > bf_df["int64_col"]
    bf_df["int_gt_1"] = bf_df["int64_col"] > 1

    bf_df["int_gt_bool"] = bf_df["int64_col"] > bf_df["bool_col"]
    bf_df["bool_gt_int"] = bf_df["bool_col"] > bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_ge_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_ge_int"] = bf_df["int64_col"] >= bf_df["int64_col"]
    bf_df["int_ge_1"] = bf_df["int64_col"] >= 1

    bf_df["int_ge_bool"] = bf_df["int64_col"] >= bf_df["bool_col"]
    bf_df["bool_ge_int"] = bf_df["bool_col"] >= bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_lt_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_lt_int"] = bf_df["int64_col"] < bf_df["int64_col"]
    bf_df["int_lt_1"] = bf_df["int64_col"] < 1

    bf_df["int_lt_bool"] = bf_df["int64_col"] < bf_df["bool_col"]
    bf_df["bool_lt_int"] = bf_df["bool_col"] < bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_le_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_le_int"] = bf_df["int64_col"] <= bf_df["int64_col"]
    bf_df["int_le_1"] = bf_df["int64_col"] <= 1

    bf_df["int_le_bool"] = bf_df["int64_col"] <= bf_df["bool_col"]
    bf_df["bool_le_int"] = bf_df["bool_col"] <= bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")


def test_minimum_op(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "float64_col"]]
    sql = utils._apply_binary_op(bf_df, ops.minimum_op, "int64_col", "float64_col")

    snapshot.assert_match(sql, "out.sql")


def test_ne_numeric(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "bool_col"]]

    bf_df["int_ne_int"] = bf_df["int64_col"] != bf_df["int64_col"]
    bf_df["int_ne_1"] = bf_df["int64_col"] != 1

    bf_df["int_ne_bool"] = bf_df["int64_col"] != bf_df["bool_col"]
    bf_df["bool_ne_int"] = bf_df["bool_col"] != bf_df["int64_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")
