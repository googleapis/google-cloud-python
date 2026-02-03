# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import bigframes.core.sql.io


def test_load_data_ddl():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_load_data_ddl_overwrite():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        write_disposition="OVERWRITE",
        columns={"col1": "INT64", "col2": "STRING"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA OVERWRITE my-project.my_dataset.my_table (col1 INT64, col2 STRING) FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_load_data_ddl_with_partition_columns():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        with_partition_columns={"part1": "DATE", "part2": "STRING"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) FROM FILES (format = 'CSV', uris = ['gs://bucket/path*']) WITH PARTITION COLUMNS (part1 DATE, part2 STRING)"
    assert sql == expected


def test_load_data_ddl_connection():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        connection_name="my-connection",
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) FROM FILES (format = 'CSV', uris = ['gs://bucket/path*']) WITH CONNECTION `my-connection`"
    assert sql == expected


def test_load_data_ddl_partition_by():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        partition_by=["date_col"],
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) PARTITION BY date_col FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_load_data_ddl_cluster_by():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        cluster_by=["cluster_col"],
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) CLUSTER BY cluster_col FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_load_data_ddl_table_options():
    sql = bigframes.core.sql.io.load_data_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        table_options={"description": "my table"},
        from_files_options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "LOAD DATA INTO my-project.my_dataset.my_table (col1 INT64, col2 STRING) OPTIONS (description = 'my table') FROM FILES (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected
