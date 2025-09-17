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


def test_date(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.date_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_dayofweek(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.dayofweek_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_dayofyear(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.dayofyear_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_floor_dt(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.FloorDtOp("D").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_hour(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.hour_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_minute(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.minute_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_month(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.month_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_normalize(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.normalize_op.as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_quarter(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.quarter_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_second(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.second_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_strftime(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.StrftimeOp("%Y-%m-%d").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_time(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.time_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_to_datetime(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.ToDatetimeOp().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_to_timestamp(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "int64_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.ToTimestampOp().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_unix_micros(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.UnixMicros().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_unix_millis(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.UnixMillis().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_unix_seconds(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(
        bf_df, [ops.UnixSeconds().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.year_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_day(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.iso_day_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_week(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.iso_week_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")


def test_iso_year(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "timestamp_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_unary_ops(bf_df, [ops.iso_year_op.as_expr(col_name)], [col_name])

    snapshot.assert_match(sql, "out.sql")
