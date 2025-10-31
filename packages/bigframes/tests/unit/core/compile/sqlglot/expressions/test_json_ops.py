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
import bigframes.core.expression as ex
import bigframes.pandas as bpd
from bigframes.testing import utils

pytest.importorskip("pytest_snapshot")


def test_json_extract(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONExtract(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONExtractArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_extract_string_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONExtractStringArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_query(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONQuery(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_query_array(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONQueryArray(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_value(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.JSONValue(json_path="$").as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_parse_json(scalar_types_df: bpd.DataFrame, snapshot):
    col_name = "string_col"
    bf_df = scalar_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ParseJSON().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_to_json_string(json_types_df: bpd.DataFrame, snapshot):
    col_name = "json_col"
    bf_df = json_types_df[[col_name]]
    sql = utils._apply_ops_to_sql(
        bf_df, [ops.ToJSONString().as_expr(col_name)], [col_name]
    )

    snapshot.assert_match(sql, "out.sql")


def test_json_set(json_types_df: bpd.DataFrame, snapshot):
    bf_df = json_types_df[["json_col"]]
    sql = utils._apply_binary_op(
        bf_df, ops.JSONSet(json_path="$.a"), "json_col", ex.const(100)
    )

    snapshot.assert_match(sql, "out.sql")
