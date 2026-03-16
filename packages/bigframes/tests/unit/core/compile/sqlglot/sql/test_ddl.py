# Copyright 2026 Google LLC
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

import bigframes.core.compile.sqlglot.sql as sql

pytest.importorskip("pytest_snapshot")


def test_load_data_minimal(snapshot):
    expr = sql.load_data(
        "my-project.my_dataset.my_table",
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    snapshot.assert_match(sql.to_sql(expr), "out.sql")


def test_load_data_all_options(snapshot):
    expr = sql.load_data(
        "my-project.my_dataset.my_table",
        write_disposition="OVERWRITE",
        columns={"col1": "INT64", "col2": "STRING"},
        partition_by=["date_col"],
        cluster_by=["cluster_col"],
        table_options={"description": "my table"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
        with_partition_columns={"part1": "DATE", "part2": "STRING"},
        connection_name="my-connection",
    )
    snapshot.assert_match(sql.to_sql(expr), "out.sql")
