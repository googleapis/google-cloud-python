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
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_date(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.date_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_dayofweek(scalar_types_df: bpd.DataFrame, snapshot):
    col_names = ["datetime_col", "timestamp_col", "date_col"]
    bf_df = scalar_types_df[col_names]
    ops_map = {col_name: ops.dayofweek_op.as_expr(col_name) for col_name in col_names}

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_dayofyear(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.dayofyear_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_floor_dt(scalar_types_df: bpd.DataFrame, snapshot):
    col_names = ["datetime_col", "timestamp_col", "date_col"]
    bf_df = scalar_types_df[col_names]
    ops_map = {
        "timestamp_col_us": ops.FloorDtOp("us").as_expr("timestamp_col"),
        "timestamp_col_ms": ops.FloorDtOp("ms").as_expr("timestamp_col"),
        "timestamp_col_s": ops.FloorDtOp("s").as_expr("timestamp_col"),
        "timestamp_col_min": ops.FloorDtOp("min").as_expr("timestamp_col"),
        "timestamp_col_h": ops.FloorDtOp("h").as_expr("timestamp_col"),
        "timestamp_col_D": ops.FloorDtOp("D").as_expr("timestamp_col"),
        "timestamp_col_W": ops.FloorDtOp("W").as_expr("timestamp_col"),
        "timestamp_col_M": ops.FloorDtOp("M").as_expr("timestamp_col"),
        "timestamp_col_Q": ops.FloorDtOp("Q").as_expr("timestamp_col"),
        "timestamp_col_Y": ops.FloorDtOp("Y").as_expr("timestamp_col"),
        "datetime_col_q": ops.FloorDtOp("us").as_expr("datetime_col"),
        "datetime_col_us": ops.FloorDtOp("us").as_expr("datetime_col"),
    }

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_floor_dt_op_invalid_freq(scalar_types_df: bpd.DataFrame):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    with pytest.raises(
        NotImplementedError, match="Unsupported freq paramater: invalid"
    ):
        utils._apply_ops_to_sql(
            bf_df,
            [ops.FloorDtOp(freq="invalid").as_expr(col_name)],  # type:ignore
            [col_name],
        )


def test_hour(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.hour_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_minute(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.minute_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_month(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.month_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_normalize(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.normalize_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_quarter(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.quarter_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_second(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.second_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_strftime(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "datetime_col", "date_col", "time_col"]]
    ops_map = {
        "date_col": ops.StrftimeOp("%Y-%m-%d").as_expr("date_col"),
        "datetime_col": ops.StrftimeOp("%Y-%m-%d").as_expr("datetime_col"),
        "time_col": ops.StrftimeOp("%Y-%m-%d").as_expr("time_col"),
        "timestamp_col": ops.StrftimeOp("%Y-%m-%d").as_expr("timestamp_col"),
    }

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_time(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.time_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_datetime(scalar_types_df: bpd.DataFrame, snapshot):
    col_names = ["int64_col", "string_col", "float64_col"]
    bf_df = scalar_types_df[col_names]
    ops_map = {col_name: ops.ToDatetimeOp().as_expr(col_name) for col_name in col_names}

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_to_timestamp(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col", "string_col", "float64_col"]]
    ops_map = {
        "int64_col": ops.ToTimestampOp().as_expr("int64_col"),
        "float64_col": ops.ToTimestampOp().as_expr("float64_col"),
        "int64_col_s": ops.ToTimestampOp(unit="s").as_expr("int64_col"),
        "int64_col_ms": ops.ToTimestampOp(unit="ms").as_expr("int64_col"),
        "int64_col_us": ops.ToTimestampOp(unit="us").as_expr("int64_col"),
        "int64_col_ns": ops.ToTimestampOp(unit="ns").as_expr("int64_col"),
    }

    sql = utils._apply_ops_to_sql(bf_df, list(ops_map.values()), list(ops_map.keys()))
    snapshot.assert_match(sql, "out.sql")


def test_unix_micros(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.UnixMicros().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_unix_millis(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.UnixMillis().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_unix_seconds(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.UnixSeconds().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.year_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(bf_df, [ops.iso_day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_week(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.iso_week_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_iso_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.iso_year_op.as_expr(col_name)], [col_name]
    )

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


def test_sub_timedelta(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["timestamp_col", "duration_col", "date_col"]]
    bf_df["duration_col"] = bpd.to_timedelta(bf_df["duration_col"], unit="us")

    bf_df["date_sub_timedelta"] = bf_df["date_col"] - bf_df["duration_col"]
    bf_df["timestamp_sub_timedelta"] = bf_df["timestamp_col"] - bf_df["duration_col"]
    bf_df["timestamp_sub_date"] = bf_df["date_col"] - bf_df["date_col"]
    bf_df["date_sub_timestamp"] = bf_df["timestamp_col"] - bf_df["timestamp_col"]
    bf_df["timedelta_sub_timedelta"] = bf_df["duration_col"] - bf_df["duration_col"]

    snapshot.assert_match(bf_df.sql, "out.sql")
