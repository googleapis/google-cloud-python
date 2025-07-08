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

import bigframes.bigquery as bbq
import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_array_to_string(repeated_types_df: bpd.DataFrame, snapshot):
    result = bbq.array_to_string(repeated_types_df["string_list_col"], ".")

    snapshot.assert_match(result.to_frame().sql, "out.sql")


def test_array_index(repeated_types_df: bpd.DataFrame, snapshot):
    result = repeated_types_df["string_list_col"].list[1]

    snapshot.assert_match(result.to_frame().sql, "out.sql")


def test_array_slice_with_only_start(repeated_types_df: bpd.DataFrame, snapshot):
    result = repeated_types_df["string_list_col"].list[1:]

    snapshot.assert_match(result.to_frame().sql, "out.sql")


def test_array_slice_with_start_and_stop(repeated_types_df: bpd.DataFrame, snapshot):
    result = repeated_types_df["string_list_col"].list[1:5]

    snapshot.assert_match(result.to_frame().sql, "out.sql")


# JSON Ops
def test_json_extract(json_types_df: bpd.DataFrame, snapshot):
    result = bbq.json_extract(json_types_df["json_col"], "$")
    expected_sql = "JSON_EXTRACT(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql
    snapshot.assert_match(result.to_frame().sql, "out.sql")


def test_json_extract_array(json_types_df: bpd.DataFrame):
    result = bbq.json_extract_array(json_types_df["json_col"], "$")
    expected_sql = "JSON_EXTRACT_ARRAY(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql


def test_json_extract_string_array(json_types_df: bpd.DataFrame):
    result = bbq.json_extract_string_array(json_types_df["json_col"], "$")
    expected_sql = "JSON_EXTRACT_STRING_ARRAY(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql


def test_json_query(json_types_df: bpd.DataFrame):
    result = bbq.json_query(json_types_df["json_col"], "$")
    expected_sql = "JSON_QUERY(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql


def test_json_query_array(json_types_df: bpd.DataFrame):
    result = bbq.json_query_array(json_types_df["json_col"], "$")
    expected_sql = "JSON_QUERY_ARRAY(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql


def test_json_value(json_types_df: bpd.DataFrame):
    result = bbq.json_value(json_types_df["json_col"], "$")
    expected_sql = "JSON_VALUE(`bfcol_1`, '$') AS `bfcol_4`"
    assert expected_sql in result.to_frame().sql


def test_parse_json(scalar_types_df: bpd.DataFrame, snapshot):
    result = bbq.json_value(scalar_types_df["string_col"], "$")
    snapshot.assert_match(result.to_frame().sql, "out.sql")
