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

import datetime

import google.cloud.bigquery as bigquery
import pytest

import bigframes.pandas as bpd

pytest.importorskip("pytest_snapshot")


def test_compile_readtable(scalar_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(scalar_types_df.sql, "out.sql")


def test_compile_readtable_w_repeated_types(repeated_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(repeated_types_df.sql, "out.sql")


def test_compile_readtable_w_nested_structs_types(
    nested_structs_types_df: bpd.DataFrame, snapshot
):
    snapshot.assert_match(nested_structs_types_df.sql, "out.sql")


def test_compile_readtable_w_json_types(json_types_df: bpd.DataFrame, snapshot):
    snapshot.assert_match(json_types_df.sql, "out.sql")


def test_compile_readtable_w_ordering(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df = bf_df.sort_values("int64_col")
    snapshot.assert_match(bf_df.sql, "out.sql")


def test_compile_readtable_w_limit(scalar_types_df: bpd.DataFrame, snapshot):
    bf_df = scalar_types_df[["int64_col"]]
    bf_df = bf_df.sort_index().head(10)
    snapshot.assert_match(bf_df.sql, "out.sql")


def test_compile_readtable_w_system_time(
    compiler_session, scalar_types_table_schema, snapshot
):
    table_ref = bigquery.TableReference(
        bigquery.DatasetReference("bigframes-dev", "sqlglot_test"),
        "scalar_types",
    )
    table = bigquery.Table(table_ref, tuple(scalar_types_table_schema))
    table._properties["location"] = compiler_session._location
    compiler_session._loader._df_snapshot[str(table_ref)] = (
        datetime.datetime(2025, 11, 9, 3, 4, 5, 678901, tzinfo=datetime.timezone.utc),
        table,
    )
    bf_df = compiler_session.read_gbq_table(str(table_ref))
    snapshot.assert_match(bf_df.sql, "out.sql")


def test_compile_readtable_w_columns_filters(compiler_session, snapshot):
    columns = ["rowindex", "int64_col", "string_col"]
    filters = [("rowindex", ">", 0), ("string_col", "in", ["Hello, World!"])]
    bf_df = compiler_session._loader.read_gbq_table(
        "bigframes-dev.sqlglot_test.scalar_types",
        enable_snapshot=False,
        columns=columns,
        filters=filters,
    )
    snapshot.assert_match(bf_df.sql, "out.sql")
